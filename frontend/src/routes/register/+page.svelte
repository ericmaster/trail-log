<script lang="ts">
  import { goto } from "$app/navigation";
  import { api, type RegisterData } from "$lib/api";
  import { t } from "svelte-i18n";

  let email = "";

  let password = "";
  let confirmPassword = "";
  let bodyWeight: number | undefined;
  let age: number | undefined;
  let gender = "";
  let vo2max: number | undefined;
  let error = "";
  let loading = false;

  async function handleRegister() {
    error = "";

    if (password !== confirmPassword) {
      error = "Passwords do not match";
      return;
    }

    loading = true;
    try {
      const data: RegisterData = {
        email,
        password,
        body_weight: bodyWeight,
        age,
        gender: gender || undefined,
        vo2max,
      };
      await api.register(data);
      goto("/login");
    } catch (e) {
      error = e instanceof Error ? e.message : "Registration failed";
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>{$t("register.title")} - {$t("app.title")}</title>
</svelte:head>

<div
  class="container d-flex align-items-center justify-content-center min-vh-100 py-5"
>
  <div
    class="card bg-dark text-white p-4 w-100 shadow-lg"
    style="max-width: 500px; border-radius: 1rem;"
  >
    <h1 class="text-center mb-4">{$t("register.title")}</h1>

    {#if error}
      <div class="alert alert-danger" role="alert">
        {error}
      </div>
    {/if}

    <form on:submit|preventDefault={handleRegister}>
      <div class="mb-3">
        <label for="email" class="form-label">{$t("register.email")} *</label>
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
        <label for="password" class="form-label"
          >{$t("register.password")} *</label
        >
        <input
          type="password"
          class="form-control bg-dark text-white border-secondary"
          id="password"
          bind:value={password}
          required
          minlength="8"
          placeholder="Min 8 characters"
        />
      </div>

      <div class="mb-3">
        <label for="confirmPassword" class="form-label"
          >{$t("register.confirm_password")} *</label
        >
        <input
          type="password"
          class="form-control bg-dark text-white border-secondary"
          id="confirmPassword"
          bind:value={confirmPassword}
          required
          placeholder="••••••••"
        />
      </div>

      <h5 class="border-bottom border-secondary pb-2 mb-3 mt-4">
        {$t("register.athlete_profile")}
      </h5>

      <div class="row g-3 mb-3">
        <div class="col-sm-6">
          <label for="bodyWeight" class="form-label"
            >{$t("register.body_weight")}</label
          >
          <input
            type="number"
            class="form-control bg-dark text-white border-secondary"
            id="bodyWeight"
            bind:value={bodyWeight}
            step="0.1"
            min="20"
            max="300"
            placeholder="70.5"
          />
        </div>

        <div class="col-sm-6">
          <label for="age" class="form-label">{$t("register.age")}</label>
          <input
            type="number"
            class="form-control bg-dark text-white border-secondary"
            id="age"
            bind:value={age}
            min="1"
            max="120"
            placeholder="30"
          />
        </div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-sm-6">
          <label for="gender" class="form-label">{$t("register.gender")}</label>
          <select
            class="form-select bg-dark text-white border-secondary"
            id="gender"
            bind:value={gender}
          >
            <option value="">{$t("register.gender_options.select")}</option>
            <option value="male">{$t("register.gender_options.male")}</option>
            <option value="female"
              >{$t("register.gender_options.female")}</option
            >
            <option value="other">{$t("register.gender_options.other")}</option>
            <option value="prefer_not_to_say"
              >{$t("register.gender_options.prefer_not_to_say")}</option
            >
          </select>
        </div>

        <div class="col-sm-6">
          <label for="vo2max" class="form-label">{$t("register.vo2max")}</label>
          <input
            type="number"
            class="form-control bg-dark text-white border-secondary"
            id="vo2max"
            bind:value={vo2max}
            step="0.1"
            min="10"
            max="100"
            placeholder="55.0"
          />
        </div>
      </div>

      <button
        type="submit"
        class="btn btn-primary w-100 py-2"
        disabled={loading}
      >
        {loading ? $t("register.creating") : $t("register.create_button")}
      </button>
    </form>

    <p class="text-center mt-3 text-secondary">
      {$t("register.has_account")}
      <a href="/login" class="text-info text-decoration-none"
        >{$t("register.login_link")}</a
      >
    </p>
  </div>
</div>

<style>
  .form-control:focus,
  .form-select:focus {
    background-color: #212529;
    color: #fff;
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
  }
</style>
