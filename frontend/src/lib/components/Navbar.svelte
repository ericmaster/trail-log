<script lang="ts">
    import { t } from "svelte-i18n";
    import { api, authState } from "$lib/api";
    import { goto } from "$app/navigation";
    import LanguageSwitcher from "$lib/components/LanguageSwitcher.svelte";
    import logo from "$lib/assets/trail-log-logo.svg";

    function handleLogout() {
        api.logout();
        goto("/login");
    }
</script>

<nav class="navbar navbar-expand-lg navbar-dark sticky-top glass-nav px-3 py-2">
    <div class="container-fluid">
        <a
            class="navbar-brand fw-bold fs-4 d-flex align-items-center gap-2"
            href="/"
        >
            <img
                src={logo}
                alt="Trail Log Logo"
                width="32"
                height="32"
                class="d-inline-block align-text-top"
            />
            <span class="tracking-tighter">{$t("app.title")}</span>
        </a>
        <div class="d-flex gap-2 align-items-center">
            {#if $authState}
                <a href="/upload" class="btn btn-outline-light btn-sm px-3"
                    >{$t("app.dashboard")}</a
                >
                <button
                    class="btn btn-outline-light btn-sm px-3"
                    on:click={handleLogout}>{$t("upload.logout")}</button
                >
            {:else}
                <a href="/login" class="btn btn-outline-light btn-sm px-3"
                    >{$t("app.login")}</a
                >
                <a
                    href="/register"
                    class="btn btn-safety-orange btn-sm px-3 shadow-sm"
                    >{$t("app.get_started")}</a
                >
            {/if}
            <div class="ms-2 border-start border-white border-opacity-10 ps-2">
                <LanguageSwitcher />
            </div>
        </div>
    </div>
</nav>

<style>
    .glass-nav {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1030;
    }

    .tracking-tighter {
        letter-spacing: -0.02em;
    }

    /* Ensure navbar sits on top if needed */
    :global(.navbar) {
        z-index: 1030;
    }
</style>
