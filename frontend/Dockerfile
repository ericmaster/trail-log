# Frontend Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
# Install dependencies including curl and libc6-compat for cloudflared
RUN npm ci && \
    apk add --no-cache curl libc6-compat

# Install cloudflared
RUN curl -L --output /usr/local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && \
    chmod +x /usr/local/bin/cloudflared

# Copy application code
COPY . .

# Expose port
EXPOSE 5173

# Run via custom setup script
CMD ["node", "tunnel-setup.js"]
