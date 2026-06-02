<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import 'normalize.css';
	import '$lib/scss/global.scss';
	let { children } = $props();
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
		height: 100dvh;
		margin: 0 auto;
		background-color: red;
		padding: $spacing-lg;
	}
</style>
