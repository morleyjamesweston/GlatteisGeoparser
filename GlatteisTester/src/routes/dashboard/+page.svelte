<script lang="ts">
	import { apiGet } from '$lib/api';
	import Button from '$lib/primitives/button.svelte';
	// import { onMount } from 'svelte';

	let allCoded = $state(null);
	let progress = $state(null);
	let isLoading = $state(false);
	let error: string | null = $state(null);

	async function getAllCoded() {
		isLoading = true;
		error = null;
		try {
			const data = await apiGet('/api/dashboard/all_coded');
			console.log('All coded data:', data);
			allCoded = data;
		} catch (err) {
			console.error('Error fetching all coded data:', err);
			error = err instanceof Error ? err.message : 'An error occurred';
		} finally {
			isLoading = false;
		}
	}

	async function getProgress() {
		isLoading = true;
		error = null;
		try {
			const data = await apiGet('/api/dashboard/coding_progress');
			console.log('Coding progress data:', data);
			progress = data;
		} catch (err) {
			console.error('Error fetching all coded data:', err);
			error = err instanceof Error ? err.message : 'An error occurred';
		} finally {
			isLoading = false;
		}
	}
</script>

{#if error}
	<div class="error">Error: {error}</div>
{/if}

{#if isLoading}
	<div>Loading...</div>
{:else if allCoded}
	<pre>{JSON.stringify(allCoded, null, 2)}</pre>
{:else}
	<p>No data loaded yet</p>
{/if}

<pre>{JSON.stringify(progress)}</pre>

<Button onclick={getAllCoded} disabled={isLoading}>Get all coded data</Button>
<Button onclick={getProgress} disabled={isLoading}>Get coding progress</Button>

<style>
	.error {
		color: red;
		padding: 1rem;
		margin-bottom: 1rem;
	}
</style>
