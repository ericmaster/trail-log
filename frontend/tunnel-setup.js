import { spawn } from 'child_process';
import { writeFile } from 'fs/promises';
import { randomBytes } from 'crypto';

const {
    CLOUDFLARE_API_TOKEN,
    CLOUDFLARE_DOMAIN,
    CLOUDFLARE_TUNNEL_NAME,
    CLOUDFLARE_ACCOUNT_ID
} = process.env;

if (!CLOUDFLARE_API_TOKEN || !CLOUDFLARE_DOMAIN || !CLOUDFLARE_TUNNEL_NAME) {
    console.error('Missing required environment variables: CLOUDFLARE_API_TOKEN, CLOUDFLARE_DOMAIN, CLOUDFLARE_TUNNEL_NAME');
    process.exit(1);
}

const API_BASE = 'https://api.cloudflare.com/client/v4';
const HEADERS = {
    'Authorization': `Bearer ${CLOUDFLARE_API_TOKEN}`,
    'Content-Type': 'application/json'
};

async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const res = await fetch(url, { ...options, headers: { ...HEADERS, ...options.headers } });
    const data = await res.json();
    if (!data.success) {
        throw new Error(`Cloudflare API Error: ${JSON.stringify(data.errors)}`);
    }
    return data.result;
}

async function getAccountId() {
    if (CLOUDFLARE_ACCOUNT_ID) return CLOUDFLARE_ACCOUNT_ID;

    // Strategy 1: List Accounts (Requires Account:Read)
    try {
        const accounts = await fetchAPI('/accounts');
        if (accounts && accounts.length > 0) return accounts[0].id;
    } catch (e) {
        console.log('Could not list accounts directly (likely missing "Account:Read" permission). Attempting to derive from Zone...');
    }

    // Strategy 2: Derive from Domain (Requires Zone:Read)
    // We try to find the zone for the domain (or its parent) to get the account ID
    const parts = CLOUDFLARE_DOMAIN.split('.');
    for (let i = 0; i < parts.length - 1; i++) {
        const checkDomain = parts.slice(i).join('.');
        try {
            const zones = await fetchAPI(`/zones?name=${checkDomain}`);
            if (zones && zones.length > 0) {
                const match = zones.find(z => z.name === checkDomain);
                if (match && match.account && match.account.id) {
                    console.log(`Found account ID ${match.account.id} via zone ${checkDomain}`);
                    return match.account.id;
                }
            }
        } catch (e) {
            console.warn(`Failed to check zone for ${checkDomain}`, e);
        }
    }

    throw new Error('Could not automatically determine Cloudflare Account ID. Please add "Account:Read" permission to your token OR set CLOUDFLARE_ACCOUNT_ID explicitly in your .env file.');
}

async function findZoneId(domain, accountId) {
    // Try to find the zone. We might be given "sub.example.com", and the zone is "example.com"
    const parts = domain.split('.');
    let zoneId = null;

    // Iterate from full domain up to top-level to find a matching zone
    for (let i = 0; i < parts.length - 1; i++) {
        const checkDomain = parts.slice(i).join('.');
        try {
            const zones = await fetchAPI(`/zones?name=${checkDomain}&account.id=${accountId}`);
            if (zones && zones.length > 0) {
                // Pick the one that exactly matches
                const match = zones.find(z => z.name === checkDomain);
                if (match) {
                    zoneId = match.id;
                    break;
                }
            }
        } catch (e) {
            console.warn(`Failed to check zone for ${checkDomain}`, e);
        }
    }

    if (!zoneId) throw new Error(`Could not find Cloudflare zone for domain: ${domain}`);
    return zoneId;
}

async function setupTunnel() {
    try {
        console.log('Starting Cloudflare Tunnel Setup...');
        const accountId = await getAccountId();
        console.log(`Using Account ID: ${accountId}`);

        // Check if tunnel exists
        const tunnels = await fetchAPI(`/accounts/${accountId}/tunnels?name=${CLOUDFLARE_TUNNEL_NAME}&is_deleted=false`);
        let tunnelId;
        let tunnelToken;

        // If tunnel exists, we must delete it to generate new credentials (cannot retrieve existing secret)
        // unless we want to assume the user has mounted credentials, but the prompt implies we set it up.
        if (tunnels.length > 0) {
            console.log(`Tunnel '${CLOUDFLARE_TUNNEL_NAME}' exists. Deleting to recreate (needed for credentials)...`);
            tunnelId = tunnels[0].id;

            // Delete connections? Sometimes needed. Cleanup first.
            await fetchAPI(`/accounts/${accountId}/tunnels/${tunnelId}/connections`, { method: 'DELETE' }).catch(() => { });
            await fetchAPI(`/accounts/${accountId}/tunnels/${tunnelId}`, { method: 'DELETE' });
        }

        // Create Tunnel
        console.log('Creating new tunnel...');
        const tunnelSecret = randomBytes(32).toString('base64');
        const createRes = await fetchAPI(`/accounts/${accountId}/tunnels`, {
            method: 'POST',
            body: JSON.stringify({
                name: CLOUDFLARE_TUNNEL_NAME,
                tunnel_secret: tunnelSecret
            })
        });

        tunnelId = createRes.id;
        tunnelToken = createRes.token; // This token can be used with `cloudflared tunnel run --token`
        console.log(`Tunnel created with ID: ${tunnelId}`);

        // We don't necessarily need the credentials.json file if we have the token
        // cloudflared tunnel run --token <token> is sufficient.

        // DNS Setup
        const zoneId = await findZoneId(CLOUDFLARE_DOMAIN, accountId);
        console.log(`Using Zone ID: ${zoneId}`);

        // CNAME target
        const cnameTarget = `${tunnelId}.cfargotunnel.com`;

        // Check existing DNS
        const dnsRecords = await fetchAPI(`/zones/${zoneId}/dns_records?type=CNAME&name=${CLOUDFLARE_DOMAIN}`);
        const existingRecord = dnsRecords.find(r => r.name === CLOUDFLARE_DOMAIN);

        if (existingRecord) {
            if (existingRecord.content !== cnameTarget) {
                console.log(`Updating DNS record for ${CLOUDFLARE_DOMAIN}...`);
                await fetchAPI(`/zones/${zoneId}/dns_records/${existingRecord.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        type: 'CNAME',
                        name: CLOUDFLARE_DOMAIN,
                        content: cnameTarget,
                        proxied: true,
                        ttl: 1 // Auto
                    })
                });
            } else {
                console.log('DNS record is already correct.');
            }
        } else {
            console.log(`Creating DNS record for ${CLOUDFLARE_DOMAIN}...`);
            await fetchAPI(`/zones/${zoneId}/dns_records`, {
                method: 'POST',
                body: JSON.stringify({
                    type: 'CNAME',
                    name: CLOUDFLARE_DOMAIN,
                    content: cnameTarget,
                    proxied: true,
                    ttl: 1
                })
            });
        }

        // Start cloudflared
        console.log('Starting cloudflared...');
        // We point it to the localhost:5173
        const cloudflared = spawn('/usr/local/bin/cloudflared', [
            'tunnel', 'run',
            '--token', tunnelToken,
            '--url', 'http://localhost:5173'
        ], { stdio: 'inherit' });

        cloudflared.on('error', (err) => console.error('Failed to start cloudflared:', err));

        // Start Application
        console.log('Starting Application...');
        const app = spawn('npm', ['run', 'dev', '--', '--host', '0.0.0.0'], { stdio: 'inherit' });

        app.on('error', (err) => console.error('Failed to start app:', err));

        // Handle exits
        const cleanup = () => {
            cloudflared.kill();
            app.kill();
            process.exit();
        };
        process.on('SIGINT', cleanup);
        process.on('SIGTERM', cleanup);

    } catch (err) {
        console.error('Setup failed:', err);
        // Fallback: Just run the app without tunnel if tunnel fails?
        // Or exit? User requested setup, so exit is appropriate to debug.
        // However, if we exit, the container crashes. 
        // Let's try to run the app anyway so they can debug locally.
        console.log('Falling back to just running the app...');
        spawn('npm', ['run', 'dev', '--', '--host', '0.0.0.0'], { stdio: 'inherit' });
    }
}

setupTunnel();
