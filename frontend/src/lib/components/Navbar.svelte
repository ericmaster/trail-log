<script lang="ts">
    import { t } from "svelte-i18n";
    import { api } from "$lib/api";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import LanguageSwitcher from "$lib/components/LanguageSwitcher.svelte";
    import logo from "$lib/assets/trail-log-logo.svg";

    let isAuthenticated = false;

    onMount(() => {
        isAuthenticated = api.isAuthenticated();
    });

    function handleLogout() {
        api.logout();
        isAuthenticated = false;
        goto("/login");
    }
</script>

<nav class="navbar navbar-expand-lg navbar-dark bg-transparent pt-4 mb-4">
    <div class="container">
        <a
            class="navbar-brand fw-bold fs-3 d-flex align-items-center gap-2"
            href="/"
        >
            <img
                src={logo}
                alt="Trail Log Logo"
                width="40"
                height="40"
                class="d-inline-block align-text-top"
            />
            {$t("app.title")}
        </a>
        <div class="d-flex gap-3 align-items-center">
            {#if isAuthenticated}
                <a href="/upload" class="btn btn-outline-light"
                    >{$t("app.dashboard")}</a
                >
                <button class="btn btn-outline-light" on:click={handleLogout}
                    >{$t("upload.logout")}</button
                >
            {:else}
                <a href="/login" class="btn btn-outline-light"
                    >{$t("app.login")}</a
                >
                <a href="/register" class="btn btn-primary"
                    >{$t("app.get_started")}</a
                >
            {/if}
            <LanguageSwitcher />
        </div>
    </div>
</nav>

<style>
    /* Ensure navbar sits on top if needed */
    :global(.navbar) {
        z-index: 1030;
    }
</style>
