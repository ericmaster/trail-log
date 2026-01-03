<script lang="ts">
    import { t } from "svelte-i18n";
</script>

<footer class="py-4 border-top border-secondary border-opacity-25 mt-auto">
    <div
        class="container text-center text-white-50 small d-flex flex-column gap-2"
    >
        <p class="mb-0">
            {$t("app.copyright")}
        </p>
        <div>
            <a
                href="/privacy-policy"
                class="text-white-50 text-decoration-none hover-white"
            >
                {$t("app.privacy_policy")}
            </a>
        </div>
    </div>
</footer>

<style>
    .hover-white:hover {
        color: #fff !important;
    }
</style>
