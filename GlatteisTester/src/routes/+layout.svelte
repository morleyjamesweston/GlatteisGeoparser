<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import 'normalize.css';
	import '$lib/scss/global.scss';
	let { children } = $props();
	import { geoDataStore } from '$lib/stores/geodata.svelte';
	geoDataStore.loadGeoData();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="container">
	{@render children()}
</div>

<style lang="scss">
	.container {
		display: flex;
		flex-direction: column;
		max-width: 60rem;
		margin: 0 auto;
		padding: $spacing-lg;
	}
</style>
