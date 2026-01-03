<script lang="ts">
    import { locale } from "svelte-i18n";
</script>

<div class="dropdown">
    <button
        class="btn btn-outline-light dropdown-toggle d-flex align-items-center gap-2 border-secondary border-opacity-50"
        type="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
    >
        <span class="fs-5">
            {$locale === "es" ? "🇪🇸" : "🇺🇸"}
        </span>
        <span class="fw-medium text-uppercase">{$locale}</span>
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
                <span class="fs-5">🇺🇸</span>
                <span>English</span>
            </button>
        </li>
        <li>
            <button
                class="dropdown-item d-flex align-items-center gap-3 py-2"
                class:active={$locale === "es"}
                onclick={() => ($locale = "es")}
            >
                <span class="fs-5">🇪🇸</span>
                <span>Español</span>
            </button>
        </li>
    </ul>
</div>

<style>
    .dropdown-item.active {
        background-color: rgba(13, 110, 253, 0.25);
        color: #fff;
    }
    .dropdown-toggle::after {
        vertical-align: middle;
    }
</style>
