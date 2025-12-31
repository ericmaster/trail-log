<script lang="ts">
	import favicon from "$lib/assets/favicon.svg";
	import "bootstrap/dist/css/bootstrap.min.css";

	import { onMount } from "svelte";
	import "$lib/i18n"; // Initialize i18n
	import { isLoading } from "svelte-i18n";

	let { children } = $props();

	onMount(async () => {
		// Import bootstrap JS on client-side only
		// @ts-ignore
		await import("bootstrap/dist/js/bootstrap.bundle.min.js");
	});
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
