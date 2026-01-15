<script lang="ts">
	import favicon from "$lib/assets/trail-log-logo.svg";
	import "../styles/custom.scss";
	import Navbar from "$lib/components/Navbar.svelte";
	import Footer from "$lib/components/Footer.svelte";

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
	<Navbar />
	{@render children()}
	<Footer />
{/if}

<style>
	:global(body) {
		background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
		color: #fff;
		min-height: 100vh;
		overflow-x: hidden;
	}

	:global(h1, h2, h3, h4, h5, h6) {
		color: #fff !important;
	}

	/* Force white color for elements within cards if they are on a dark bg */
	:global(.bg-dark) {
		color: #fff !important;
	}
</style>
