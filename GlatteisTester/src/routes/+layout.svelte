<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import '@fontsource/source-serif-pro';
	import '@fontsource/source-sans-pro';
	import '@fontsource-variable/geologica/wght.css';
	import { userData } from '$lib/stores/user.svelte';
	import { onMount } from 'svelte';
	import MenuBar from '$lib/components/menu-bar.svelte';
	import { ModeWatcher } from 'mode-watcher';

	onMount(() => {
		userData.loadUserData();
	});

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="flex min-h-screen w-full flex-col">
	<ModeWatcher />
	<MenuBar />
	{@render children()}
</div>
