<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import 'normalize.css';
	import '@fontsource/source-serif-pro';
	import '@fontsource/source-sans-pro';
	import '@fontsource-variable/geologica/wght.css';
	import '$lib/scss/global.scss';
	import { userData } from '$lib/stores/user.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if userData.isAuthenticated}
	<div>Welcome, {userData.username}!</div>
	{#if userData.isAdmin}
		<div>You have admin privileges</div>
	{/if}
{:else}
	<div>Please log in</div>
{/if}

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
