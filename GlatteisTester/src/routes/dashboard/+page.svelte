<script lang="ts">
	import { apiGet } from '$lib/api';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card/index.js';
	import type {
		CodedLoc,
		UnresolvedLocsPerGeoparser,
		GeoParserEvaluation,
		ResolutionRatio,
		CodedLocHuman
	} from '$lib/interfaces';

	import CoderProgress from '$lib/components/coder-progress.svelte';
	import ArticleSelector from './article-selector.svelte';
	import ArticleText from './article-text.svelte';
	import ArticleMap from './article-map.svelte';
	import CodingDisplay from './coding-display.svelte';
	import ResolvedChart from './resolved-chart.svelte';
	import UnresolvedCounts from './unresolved-counts.svelte';
	import CodingDisplayHuman from './coding-display-human.svelte';
	import GeoparserConfigs from './geoparser-configs.svelte';
	import AccuracyScores from './accuracy-scores.svelte';

	let allCoded: { machine_coding: CodedLoc[]; manual_coding: CodedLocHuman[] } | null =
		$state(null);
	let selectedContentID = $state('');

	let resolutionRatios: { [key: string]: ResolutionRatio } | null = $state(null);
	let unresolvedLocsPerGeoparser: UnresolvedLocsPerGeoparser | null = $state(null);

	async function getGeoparserEvaluation() {
		try {
			const data: GeoParserEvaluation = await apiGet('/api/dashboard/geoparser_evaluation');
			resolutionRatios = data.total_locs_per_geoparser;
			unresolvedLocsPerGeoparser = data.unresolved_locs_per_geoparser;
		} catch (err) {
			console.error('Error fetching geoparser evaluation data:', err);
		}
	}

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

	onMount(() => {
		getGeoparserEvaluation();
	});
</script>

<div class="grid w-full grow grid-cols-1 gap-4 p-4 xl:grid-cols-4">
	<div class="flex flex-col gap-4">
		<CoderProgress />
		<ResolvedChart {resolutionRatios} />
	</div>

	<div class="col-span-2 flex flex-col gap-4">
		<Card.Root>
			<Card.Header>
				{#if selectedContentID}
					<Card.Title
						>Content <span class="text-muted-foreground">(ID: {selectedContentID})</span
						></Card.Title
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

		<h1 class="font-lg mx-auto font-heading">Machine coded</h1>
		<CodingDisplay codedLocs={allCoded?.machine_coding} />
		<h1 class="font-lg mx-auto font-heading">Human coded</h1>
		<CodingDisplayHuman codedLocs={allCoded?.manual_coding} />
	</div>
	<div class="flex flex-col gap-4">
		<AccuracyScores />

		<!-- <ArticleMap {selectedContentID} /> -->
		<GeoparserConfigs />
		<UnresolvedCounts {unresolvedLocsPerGeoparser} />
	</div>
</div>
