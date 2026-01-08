<script lang="ts">
    import { locale } from "svelte-i18n";
</script>

<div class="dropdown">
    <button
        class="btn btn-outline-light d-flex align-items-center justify-content-center gap-2 border-secondary border-opacity-50 lang-btn"
        type="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
    >
        <img
            src="https://flagcdn.com/{$locale === 'es' ? 'es' : 'us'}.svg"
            alt={$locale === "es" ? "ES" : "US"}
            class="flag-icon rounded-1 shadow-sm"
        />
        <span class="fw-medium text-uppercase lang-label"
            >{$locale === "es" ? "es" : "en"}</span
        >
    </button>
    <ul
        class="dropdown-menu dropdown-menu-dark dropdown-menu-end shadow-lg border-secondary border-opacity-25"
    >
        <li>
            <button
                class="dropdown-item d-flex align-items-center gap-3 py-2"
                class:active={$locale === "en"}
                onclick={() => ($locale = "en")}
            >
                <img
                    src="https://flagcdn.com/us.svg"
                    alt="US"
                    class="flag-icon rounded-1 shadow-sm"
                />
                <span>English</span>
            </button>
        </li>
        <li>
            <button
                class="dropdown-item d-flex align-items-center gap-3 py-2"
                class:active={$locale === "es"}
                onclick={() => ($locale = "es")}
            >
                <img
                    src="https://flagcdn.com/es.svg"
                    alt="ES"
                    class="flag-icon rounded-1 shadow-sm"
                />
                <span>Español</span>
            </button>
        </li>
    </ul>
</div>

<style>
    .lang-btn {
        width: 72px;
    }

    .lang-label {
        width: 20px;
        text-align: left;
    }

    .flag-icon {
        width: 20px;
        height: 14px;
        object-fit: cover;
    }

    .dropdown-item.active {
        background-color: rgba(13, 110, 253, 0.25);
        color: #fff;
    }
</style>
