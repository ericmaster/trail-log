<script lang="ts">
  import { goto } from "$app/navigation";
  import { api, type RegisterData } from "$lib/api";

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
  <title>Register - Trail Fit Uploader</title>
</svelte:head>

<div
  class="container d-flex align-items-center justify-content-center min-vh-100 py-5"
>
  <div
    class="card bg-dark text-white p-4 w-100 shadow-lg"
    style="max-width: 500px; border-radius: 1rem;"
  >
    <h1 class="text-center mb-4">Create Account</h1>

    {#if error}
      <div class="alert alert-danger" role="alert">
        {error}
      </div>
    {/if}

    <form on:submit|preventDefault={handleRegister}>
      <div class="mb-3">
        <label for="email" class="form-label">Email *</label>
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
        <label for="password" class="form-label">Password *</label>
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
          >Confirm Password *</label
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
        Athlete Profile
      </h5>

      <div class="row g-3 mb-3">
        <div class="col-sm-6">
          <label for="bodyWeight" class="form-label">Body Weight (kg)</label>
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
          <label for="age" class="form-label">Age</label>
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
          <label for="gender" class="form-label">Gender</label>
          <select
            class="form-select bg-dark text-white border-secondary"
            id="gender"
            bind:value={gender}
          >
            <option value="">Select...</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="prefer_not_to_say">Prefer not to say</option>
          </select>
        </div>

        <div class="col-sm-6">
          <label for="vo2max" class="form-label">VO2max (ml/kg/min)</label>
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
        {loading ? "Creating Account..." : "Create Account"}
      </button>
    </form>

    <p class="text-center mt-3 text-secondary">
      Already have an account? <a
        href="/login"
        class="text-info text-decoration-none">Login</a
      >
    </p>
  </div>
</div>

<style>
  :global(body) {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    min-height: 100vh;
  }

  .form-control:focus,
  .form-select:focus {
    background-color: #212529;
    color: #fff;
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
  }
</style>
