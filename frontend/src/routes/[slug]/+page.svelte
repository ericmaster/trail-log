<script lang="ts">
    import { t, locale } from "svelte-i18n";
    import { page } from "$app/stores";
    import { onMount } from "svelte";
    import { loadMarkdownContent, type MarkdownContent } from "$lib/markdown";

    let content: MarkdownContent = { title: "", html: "" };
    let loading = true;
    let slug = "";

    $: slug = $page.params.slug;

    async function loadContent() {
        if (!slug) return;
        loading = true;
        try {
            content = await loadMarkdownContent(slug);
        } catch (e) {
            console.error(e);
            content = { title: "Error", html: "<p>Content not found.</p>" };
        }
        loading = false;
    }

    onMount(() => {
        loadContent();
    });

    // Reload content when locale or slug changes
    $: if ($locale || slug) {
        loadContent();
    }
</script>

<svelte:head>
    <title>{content.title} - {$t("app.title")}</title>
</svelte:head>

<div class="min-vh-100 py-5">
    <div class="container" style="max-width: 900px;">
        {#if content.title}
            <header class="mb-4 border-bottom border-secondary pb-3">
                <h1 class="h2 mb-0 text-white">{content.title}</h1>
            </header>
        {/if}

        <main>
            {#if loading}
                <div class="text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            {:else}
                <div
                    class="card bg-dark text-white border-secondary mb-4 shadow"
                >
                    <div class="card-body p-4 markdown-content">
                        {@html content.html}
                    </div>
                </div>
            {/if}
        </main>
    </div>
</div>

<style>
    :global(.markdown-content) {
        line-height: 1.8;
    }

    :global(.markdown-content h1) {
        font-size: 2rem;
        margin-bottom: 1.5rem;
        color: #fff;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }

    :global(.markdown-content h2) {
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #0d6efd;
    }

    :global(.markdown-content h3) {
        font-size: 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        color: #0dcaf0;
    }

    :global(.markdown-content h4) {
        font-size: 1.1rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        color: #ffc107;
    }

    :global(.markdown-content p) {
        margin-bottom: 1rem;
        color: rgba(255, 255, 255, 0.9);
    }

    :global(.markdown-content ul, .markdown-content ol) {
        margin-bottom: 1rem;
        padding-left: 2rem;
    }

    :global(.markdown-content li) {
        margin-bottom: 0.5rem;
        color: rgba(255, 255, 255, 0.85);
    }

    :global(.markdown-content a) {
        color: #0dcaf0;
        text-decoration: none;
    }

    :global(.markdown-content a:hover) {
        color: #3dd5f3;
        text-decoration: underline;
    }

    :global(.markdown-content table) {
        width: 100%;
        margin-bottom: 1.5rem;
        border-collapse: collapse;
    }

    :global(.markdown-content table th) {
        background-color: rgba(13, 110, 253, 0.2);
        padding: 0.75rem;
        text-align: left;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-weight: 600;
    }

    :global(.markdown-content table td) {
        padding: 0.75rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    :global(.markdown-content table tr:nth-child(even)) {
        background-color: rgba(255, 255, 255, 0.02);
    }

    :global(.markdown-content code) {
        background-color: rgba(0, 0, 0, 0.3);
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
        font-family: monospace;
        color: #ffc107;
    }

    :global(.markdown-content pre) {
        background-color: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 0.5rem;
        overflow-x: auto;
        margin-bottom: 1rem;
    }

    :global(.markdown-content pre code) {
        background-color: transparent;
        padding: 0;
    }

    :global(.markdown-content strong) {
        color: #fff;
        font-weight: 600;
    }

    :global(.markdown-content hr) {
        border: 0;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        margin: 2rem 0;
    }

    :global(.markdown-content blockquote) {
        border-left: 4px solid #0d6efd;
        padding-left: 1rem;
        margin-left: 0;
        margin-bottom: 1rem;
        font-style: italic;
        color: rgba(255, 255, 255, 0.7);
    }
</style>
