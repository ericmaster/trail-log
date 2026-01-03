<script lang="ts">
    import { t } from "svelte-i18n";
</script>

<svelte:head>
    <title>{$t("app.privacy_policy")} - {$t("app.title")}</title>
</svelte:head>

<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <h1 class="mb-4">{$t("app.privacy_policy")}</h1>

            <div class="card bg-dark text-white border-secondary p-4">
                <div class="card-body">
                    <p>{$t("privacy_policy_page.last_updated")}</p>

                    <h2 class="h4 mt-4 mb-3">
                        {$t("privacy_policy_page.section1_title")}
                    </h2>
                    <p class="text-white-50">
                        {$t("privacy_policy_page.section1_content")}
                    </p>
                    <ul class="text-white-50">
                        <li>{$t("privacy_policy_page.section1_list1")}</li>
                        <li>{$t("privacy_policy_page.section1_list2")}</li>
                        <li>{$t("privacy_policy_page.section1_list3")}</li>
                    </ul>

                    <h2 class="h4 mt-4 mb-3">
                        {$t("privacy_policy_page.section2_title")}
                    </h2>
                    <p class="text-white-50">
                        {$t("privacy_policy_page.section2_content")}
                    </p>

                    <h2 class="h4 mt-4 mb-3">
                        {$t("privacy_policy_page.section3_title")}
                    </h2>
                    <p class="text-white-50">
                        {$t("privacy_policy_page.section3_content")}
                    </p>

                    <h2 class="h4 mt-4 mb-3">
                        {$t("privacy_policy_page.section4_title")}
                    </h2>
                    <p class="text-white-50">
                        {$t("privacy_policy_page.section4_content")}
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
