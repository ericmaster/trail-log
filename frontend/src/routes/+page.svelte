<script lang="ts">
  import { api } from "$lib/api";
  import { onMount } from "svelte";
  import { t, locale } from "svelte-i18n";

  let isAuthenticated = false;

  onMount(() => {
    isAuthenticated = api.isAuthenticated();
  });
</script>

<svelte:head>
  <title>{$t("landing.title")}</title>
</svelte:head>

<div class="min-vh-100 d-flex flex-column">
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-transparent pt-4">
    <div class="container">
      <a class="navbar-brand fw-bold fs-3" href="/">{$t("app.title")}</a>
      <div class="d-flex gap-3">
        {#if isAuthenticated}
          <a href="/upload" class="btn btn-outline-light"
            >{$t("app.dashboard")}</a
          >
        {:else}
          <a href="/login" class="btn btn-outline-light">{$t("app.login")}</a>
          <a href="/register" class="btn btn-primary">{$t("app.get_started")}</a
          >
        {/if}
        <!-- Language Switcher -->
        <div class="dropdown">
          <button
            class="btn btn-outline-light dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            🌍 {$locale?.toUpperCase()}
          </button>
          <ul class="dropdown-menu dropdown-menu-dark dropdown-menu-end">
            <li>
              <button class="dropdown-item" onclick={() => ($locale = "en")}
                >English</button
              >
            </li>
            <li>
              <button class="dropdown-item" onclick={() => ($locale = "es")}
                >Español</button
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <main class="flex-grow-1 d-flex align-items-center">
    <div class="container">
      <div class="row align-items-center py-5">
        <div class="col-lg-7 text-center text-lg-start mb-5 mb-lg-0">
          <h1 class="display-3 fw-bold mb-4 bg-gradient-text">
            {$t("landing.hero_title")}
          </h1>
          <p class="lead text-light opacity-75 mb-5 fs-4">
            {$t("landing.hero_subtitle")}
          </p>
          <div
            class="d-flex gap-3 justify-content-center justify-content-lg-start"
          >
            <a
              href="/register"
              class="btn btn-primary btn-lg px-5 py-3 fw-bold shadow-lg"
              >{$t("landing.join_study")}</a
            >
            <a
              href="#how-it-works"
              class="btn btn-outline-light btn-lg px-5 py-3"
              >{$t("landing.learn_more")}</a
            >
          </div>
        </div>
        <div class="col-lg-5">
          <div
            class="card bg-dark bg-opacity-50 border-secondary shadow-lg p-3 rotate-card"
          >
            <div class="card-body">
              <div class="d-flex align-items-center gap-3 mb-4">
                <div class="bg-primary rounded-circle p-3 bg-opacity-25">
                  <span class="fs-4">📊</span>
                </div>
                <div>
                  <h5 class="mb-1">{$t("landing.advanced_analytics")}</h5>
                  <small class="text-white-50">{$t("landing.deep_dive")}</small>
                </div>
              </div>

              <!-- Dummy Chart Visualization -->
              <div class="d-flex align-items-end gap-2" style="height: 150px;">
                <div
                  class="bg-primary bg-opacity-75 rounded w-100"
                  style="height: 40%"
                ></div>
                <div
                  class="bg-primary bg-opacity-75 rounded w-100"
                  style="height: 70%"
                ></div>
                <div
                  class="bg-info bg-opacity-75 rounded w-100"
                  style="height: 50%"
                ></div>
                <div
                  class="bg-primary bg-opacity-75 rounded w-100"
                  style="height: 85%"
                ></div>
                <div
                  class="bg-primary rounded w-100 shadow"
                  style="height: 100%"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- Features Section -->
  <section id="how-it-works" class="py-5 bg-dark bg-opacity-25">
    <div class="container py-5">
      <div class="text-center mb-5">
        <h2 class="fw-bold mb-3">{$t("landing.how_it_works")}</h2>
        <p class="text-white-50">
          {$t("landing.symbiotic_relationship")}
        </p>
      </div>

      <div class="row g-4">
        <div class="col-md-4">
          <div
            class="h-100 p-4 rounded-4 border border-secondary border-opacity-25 bg-gradient-dark"
          >
            <div class="display-5 mb-3">📂</div>
            <h3 class="h4 mb-3">{$t("landing.step1_title")}</h3>
            <p class="text-white-50">
              {$t("landing.step1_desc")}
            </p>
          </div>
        </div>
        <div class="col-md-4">
          <div
            class="h-100 p-4 rounded-4 border border-secondary border-opacity-25 bg-gradient-dark"
          >
            <div class="display-5 mb-3">🔬</div>
            <h3 class="h4 mb-3">{$t("landing.step2_title")}</h3>
            <p class="text-white-50">
              {$t("landing.step2_desc")}
            </p>
          </div>
        </div>
        <div class="col-md-4">
          <div
            class="h-100 p-4 rounded-4 border border-secondary border-opacity-25 bg-gradient-dark"
          >
            <div class="display-5 mb-3">📈</div>
            <h3 class="h4 mb-3">{$t("landing.step3_title")}</h3>
            <p class="text-white-50">
              {$t("landing.step3_desc")}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="py-4 border-top border-secondary border-opacity-25 mt-auto">
    <div class="container text-center text-white-50 small">
      <p class="mb-0">
        {$t("app.copyright")}
      </p>
    </div>
  </footer>
</div>

<style>
  :global(body) {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #fff;
    overflow-x: hidden;
  }

  .bg-gradient-text {
    background: linear-gradient(to right, #fff 0%, #a5b4fc 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .bg-gradient-dark {
    background: linear-gradient(
      180deg,
      rgba(255, 255, 255, 0.05) 0%,
      rgba(255, 255, 255, 0.02) 100%
    );
  }

  .rotate-card {
    transform: perspective(1000px) rotateY(-10deg) rotateX(5deg);
    transition: transform 0.5s ease;
  }

  .rotate-card:hover {
    transform: perspective(1000px) rotateY(0deg) rotateX(0deg);
  }

  /* Smooth scroll behavior */
  :global(html) {
    scroll-behavior: smooth;
  }
</style>
