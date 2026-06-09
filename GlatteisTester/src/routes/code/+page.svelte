<script lang="ts">
	import ChoiceButtons from '$lib/components/choice-buttons.svelte';
	import FeaturesBar from '$lib/components/features-bar.svelte';
	import LocationMap from '$lib/components/location-map.svelte';
	import SelectWords from '$lib/components/select-words.svelte';
	import { removeHtmlContent } from '$lib/utilities/clean-text';
	import { apiGet, apiPost } from '$lib/api';
	import { onMount } from 'svelte';
	import type { ReturnGeoDataFeature } from '$lib/interfaces';
	import Button from '$lib/components/ui/button/button.svelte';

	import * as Card from '$lib/components/ui/card/index.js';

	let articleID: string | null = $state(null);
	let content: string | null = $state(null);
	let selected = $state([]);
	let stage: 'recognize' | 'resolve' = $state('recognize');

	let resolvedFeatures: Record<string, ReturnGeoDataFeature | null> = $state({});
	let resolveFeatureIdx = $state(0);
	let selectedFeature: ReturnGeoDataFeature | null = $state(null);

	$effect(() => {
		if (selectedFeature && selectedFeature.id === null) {
			advanceResolutionTask();
		}
	});

	function advanceStage() {
		if (stage === 'recognize') {
			stage = 'resolve';
		} else if (stage === 'resolve') {
			stage = 'recognize';
			fetch_content();
		}
	}

	function fetch_content() {
		apiGet('/api/next_content')
			.then((data) => {
				content = removeHtmlContent(data.content);
				// content = 'Lausanne Genf Bern Freiberg Zürich';
				articleID = data.id;
			})
			.catch((error) => {
				console.error('Error fetching data:', error);
			});
	}

	function clearState() {
		content = null;
		selected = [];
		stage = 'recognize';
		resolvedFeatures = {};
		resolveFeatureIdx = 0;
		selectedFeature = null;
	}

	function advanceResolutionTask() {
		resolvedFeatures[selected[resolveFeatureIdx]] = selectedFeature;
		if (resolveFeatureIdx < selected.length - 1) {
			resolveFeatureIdx += 1;
			selectedFeature = null;
		} else {
			submit();
			advanceStage();
			clearState();
		}
	}

	function submitNoneFound() {
		const payload = {
			id: articleID, // replace with actual content ID if available
			resolutions: 'none_found'
		};

		apiPost('/api/submit', payload).catch((error) => {
			console.error('Error submitting:', error);
		});

		submit();
		advanceStage();
		clearState();
	}

	function submit() {
		const payload = {
			id: articleID, // replace with actual content ID if available
			resolutions: resolvedFeatures
		};

		apiPost('/api/submit', payload).catch((error) => {
			console.error('Error submitting:', error);
		});
	}

	onMount(() => {
		fetch_content();
	});
</script>

<div class="flex flex-col gap-4 p-4">
	{#if stage == 'recognize'}
		<Card.Root>
			<Card.Header>
				<Card.Title>Locations selected</Card.Title>
				<Card.Description>Card Description</Card.Description>
			</Card.Header>
			<Card.Content>
				<ChoiceButtons bind:selected />
			</Card.Content>
		</Card.Root>

		<Card.Root>
			<Card.Header>
				<Card.Title>Content</Card.Title>
				<Card.Description>
					<span class="font-light">(Article: {articleID})</span>
				</Card.Description>
			</Card.Header>
			<Card.Content class="h-120">
				<SelectWords {content} bind:selected enabled={stage == 'recognize'} />
			</Card.Content>
			<Card.Footer class="flex justify-end gap-2">
				<Button variant="outline" onclick={submitNoneFound}>No locations found</Button>
				<Button onclick={advanceStage}>All locations recorded</Button>
			</Card.Footer>
		</Card.Root>
	{:else if stage == 'resolve' && selected}
		<Card.Root>
			<Card.Header>
				<Card.Title>Locations resolved</Card.Title>
				<Card.Description
					>These are the places you identified, the next step is to connect them to the correct
					real-world location.</Card.Description
				>
			</Card.Header>
			<Card.Content>
				<FeaturesBar {selected} {resolvedFeatures} />
			</Card.Content>
		</Card.Root>
		<Card.Root>
			<Card.Header>
				<Card.Title>Location options</Card.Title>
				<Card.Description
					>Please choose the correct location from the choices below:</Card.Description
				>
			</Card.Header>
			<Card.Content>
				<LocationMap
					location={selected[resolveFeatureIdx]}
					bind:selectedGeoData={selectedFeature}
				/>
			</Card.Content>
			<Card.Footer class="flex justify-end gap-2">
				<Button onclick={advanceResolutionTask}>Submit</Button>
			</Card.Footer>
		</Card.Root>
	{/if}
</div>
