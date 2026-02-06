<script lang="ts">
  import { t } from "svelte-i18n";
  import heroBg from "$lib/assets/hero-bg.png";
</script>

<svelte:head>
  <title>{$t("landing.title")}</title>
</svelte:head>

<div class="min-vh-100 d-flex flex-column landing-page">
  <!-- Hero Section -->
  <main
    id="hero"
    class="flex-grow-1 d-flex align-items-center position-relative overflow-hidden"
  >
    <div class="hero-overlay position-absolute top-0 start-0 w-100 h-100"></div>
    <div class="container position-relative" style="z-index: 2;">
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
              class="btn btn-safety-orange btn-lg px-5 py-3 shadow-lg"
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
          <div class="card glass-card shadow-lg p-3 rotate-card">
            <div class="card-body">
              <div class="d-flex align-items-center gap-3 mb-4">
                <div
                  class="bg-primary rounded-circle p-3 bg-opacity-10 border border-primary border-opacity-25"
                >
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
          <div class="h-100 p-4 rounded-4 glass-card text-center text-md-start">
            <div class="mb-4 d-flex justify-content-center">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="icon-svg orange"
              >
                <!-- Base -->
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <!-- Upload Arrow -->
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
            </div>
            <h3 class="h4 mb-3">{$t("landing.step1_title")}</h3>
            <p class="text-white-50">
              {$t("landing.step1_desc")}
            </p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="h-100 p-4 rounded-4 glass-card text-center text-md-start">
            <div class="mb-4 d-flex justify-content-center">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="icon-svg green"
              >
                <!-- Pulse Wave -->
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                <!-- Tactical Accents -->
                <circle cx="15" cy="21" r="0.5" fill="currentColor" />
                <circle cx="9" cy="3" r="0.5" fill="currentColor" />
              </svg>
            </div>
            <h3 class="h4 mb-3">{$t("landing.step2_title")}</h3>
            <p class="text-white-50">
              {$t("landing.step2_desc")}
            </p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="h-100 p-4 rounded-4 glass-card text-center text-md-start">
            <div class="mb-4 d-flex justify-content-center">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="icon-svg cyan"
              >
                <path d="M3 17l6-6 4 4 8-8" />
                <polyline points="13 7 21 7 21 15" />
                <line x1="3" y1="21" x2="21" y2="21" opacity="0.3" />
              </svg>
            </div>
            <h3 class="h4 mb-3">{$t("landing.step3_title")}</h3>
            <p class="text-white-50">
              {$t("landing.step3_desc")}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>

<style>
  #hero {
    background-image: url($lib/assets/hero-bg.png);
    background-size: cover;
    background-position: center;
  }

  /* Only apply fixed background on devices that support hover (desktop-like) to avoid repaint issues on mobile */
  @media (hover: hover) {
    #hero {
      background-attachment: fixed;
    }
  }

  .hero-overlay {
    background: linear-gradient(
      to bottom,
      rgba(17, 24, 39, 0.4) 0%,
      rgba(17, 24, 39, 1) 100%
    );
  }

  .icon-svg {
    width: 64px;
    height: 64px;
    animation: fadeInIcon 0.8s ease-out forwards;
  }

  .icon-svg.orange {
    color: #ff5e00;
  }
  .icon-svg.green {
    color: #86efac;
  }
  .icon-svg.cyan {
    color: #0dcaf0;
  }

  @keyframes fadeInIcon {
    from {
      opacity: 0;
      transform: scale(0.9);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  .bg-gradient-text {
    background: linear-gradient(to right, #fff 0%, #ff5e00 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
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
