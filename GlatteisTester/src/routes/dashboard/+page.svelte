<script lang="ts">
	import { apiGet } from '$lib/api';
	import { onMount } from 'svelte';
	import CoderProgress from './coder-progress.svelte';
	import ArticleSelector from './article-selector.svelte';
	import ArticleText from './article-text.svelte';
	import * as Card from '$lib/components/ui/card/index.js';

	let allCoded = $state(null);
	let selectedContentID = $state('');

	//     @app.route("/api/dashboard/coded/<content_id>", methods=["GET"])

	async function getCodedData(content_id: string) {
		try {
			const data = await apiGet(`/api/dashboard/coded/${content_id}`);
			console.log('Coded data:', data);
			allCoded = data;
		} catch (err) {
			console.error('Error fetching coded data:', err);
		}
	}

	$effect(() => {
		if (selectedContentID) {
			getCodedData(selectedContentID);
		}
	});
</script>

<div class="grid grid-cols-1 gap-4 p-4 xl:grid-cols-4">
	<CoderProgress />

	<Card.Root>
		<Card.Header>
			{#if selectedContentID}
				<Card.Title>Content {selectedContentID}</Card.Title>
			{:else}
				<Card.Title>Select an article by ID number:</Card.Title>
			{/if}
			<Card.Description></Card.Description>
			<Card.Action>
				<ArticleSelector bind:value={selectedContentID} />
			</Card.Action>
		</Card.Header>
		<Card.Content>
			<ArticleText {selectedContentID} />
		</Card.Content>
		<Card.Footer></Card.Footer>
	</Card.Root>
</div>

<!-- {#if error}
	<div class="error">Error: {error}</div>
{/if}
{#if isLoading}
	<div>Loading...</div>
{:else if allCoded}
	<pre>{JSON.stringify(allCoded, null, 2)}</pre>
{:else}
	<p>No data loaded yet</p>
{/if} -->
