<script lang="ts">
	import { apiGet } from '$lib/api';
	import CoderProgress from './coder-progress.svelte';
	import ArticleSelector from './article-selector.svelte';
	import ArticleText from './article-text.svelte';
	import * as Card from '$lib/components/ui/card/index.js';
	import type { CodedLoc } from '$lib/interfaces';
	import CodingDisplay from './coding-display.svelte';

	let allCoded: { machine_coding: CodedLoc[]; manual_coding: CodedLoc[] } | null = $state(null);
	let selectedContentID = $state('');

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
				<Card.Title
					>Content <span class="text-muted-foreground">(ID: {selectedContentID})</span></Card.Title
				>
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

	<CodingDisplay codedLocs={allCoded?.machine_coding} />
</div>
