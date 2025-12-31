<script lang="ts">
  import { goto } from "$app/navigation";
  import { api } from "$lib/api";
  import { t } from "svelte-i18n";

  let email = "";
  let password = "";
  let error = "";
  let loading = false;

  async function handleLogin() {
    error = "";
    loading = true;
    try {
      await api.login({ username: email, password });
      goto("/upload");
    } catch (e) {
      error = e instanceof Error ? e.message : "Login failed";
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>{$t("login.title")} - {$t("app.title")}</title>
</svelte:head>

<div
  class="container d-flex align-items-center justify-content-center min-vh-100"
>
  <div
    class="card bg-dark text-white p-4 w-100"
    style="max-width: 400px; border-radius: 1rem;"
  >
    <h1 class="text-center mb-4">{$t("login.title")}</h1>

    {#if error}
      <div class="alert alert-danger" role="alert">
        {error}
      </div>
    {/if}

    <form on:submit|preventDefault={handleLogin}>
      <div class="mb-3">
        <label for="email" class="form-label">{$t("login.email")}</label>
        <input
          type="email"
          class="form-control bg-dark text-white border-secondary"
          id="email"
          bind:value={email}
          required
          placeholder="you@example.com"
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">{$t("login.password")}</label>
        <input
          type="password"
          class="form-control bg-dark text-white border-secondary"
          id="password"
          bind:value={password}
          required
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        class="btn btn-primary w-100 py-2"
        disabled={loading}
      >
        {loading ? $t("login.logging_in") : $t("login.login_button")}
      </button>
    </form>

    <p class="text-center mt-3 text-secondary">
      {$t("login.no_account")}
      <a href="/register" class="text-info text-decoration-none"
        >{$t("login.register_link")}</a
      >
    </p>
  </div>
</div>

<style>
  :global(body) {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    min-height: 100vh;
  }

  /* Override bootstrap focus to match theme */
  .form-control:focus {
    background-color: #212529;
    color: #fff;
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
  }
</style>
