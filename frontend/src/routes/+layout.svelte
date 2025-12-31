<script lang="ts">
	import favicon from "$lib/assets/favicon.svg";
	import "bootstrap/dist/css/bootstrap.min.css";
	import "$lib/i18n"; // Initialize i18n
	import { isLoading, locale, t } from "svelte-i18n";

	let { children } = $props();

	function switchLang(lang: string) {
		locale.set(lang);
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if $isLoading}
	<div
		class="d-flex justify-content-center align-items-center min-vh-100 bg-dark text-white"
	>
		<div class="spinner-border text-primary" role="status">
			<span class="visually-hidden">Loading...</span>
		</div>
	</div>
{:else}
	{@render children()}
{/if}
