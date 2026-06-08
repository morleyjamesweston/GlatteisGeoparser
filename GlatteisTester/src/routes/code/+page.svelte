<script lang="ts">
	import ChoiceButtons from '$lib/components/choice-buttons.svelte';
	import FeaturesBar from '$lib/components/features-bar.svelte';
	import LocationMap from '$lib/components/location-map.svelte';
	import SelectWords from '$lib/components/select-words.svelte';
	import Button from '$lib/primitives/button.svelte';
	import { removeHtmlContent } from '$lib/utilities/clean-text';
	import { apiGet, apiPost } from '$lib/api';
	import { onMount } from 'svelte';

	let articleID: string | null = $state(null);
	let content: string | null = $state(null);
	let selected = $state([]);
	let stage: 'recognize' | 'resolve' = $state('recognize');

	let resolvedFeatures: Record<string, string> = $state({});
	let resolveFeatureIdx = $state(0);
	let selectedFeature = $state('');

	$effect(() => {
		if (selectedFeature === 'none_found') {
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
				content = 'Lausanne Genf Bern Freiberg Zürich';
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
		selectedFeature = '';
	}

	function advanceResolutionTask() {
		resolvedFeatures[selected[resolveFeatureIdx]] = selectedFeature;
		if (resolveFeatureIdx < selected.length - 1) {
			resolveFeatureIdx += 1;
			selectedFeature = '';
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

<div class="flex-col">
	{#if stage == 'recognize'}
		<h2>Choices</h2>
		<ChoiceButtons bind:selected />
		<h2>Content</h2>
		<SelectWords {content} bind:selected enabled={stage == 'recognize'} />

		<div class="flex-between">
			<Button variant="secondary" onclick={submitNoneFound}>No locations found</Button>
			<Button onclick={advanceStage}>Next step</Button>
		</div>
	{:else if stage == 'resolve' && selected}
		<FeaturesBar {selected} {resolvedFeatures} />
		<h2>Locations</h2>
		<LocationMap location={selected[resolveFeatureIdx]} bind:selectedFeature />
		<button onclick={advanceResolutionTask}>Submit</button>
	{/if}
</div>

<style lang="scss">
	:global(.scroll-container) {
		border: 1px solid #aaa;
		height: 15rem;
	}
</style>
