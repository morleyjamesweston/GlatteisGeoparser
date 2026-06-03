<script lang="ts">
	import ChoiceButtons from '$lib/components/choice-buttons.svelte';
	import LocationMap from '$lib/components/location-map.svelte';
	import SelectWords from '$lib/components/select-words.svelte';
	import { removeHtmlContent } from '$lib/utilities/clean-text';
	import { onMount } from 'svelte';

	let content: string | null = $state(null);
	let selected = $state([]);
	let stage: 'recognize' | 'resolve' = $state('recognize');

	function advanceStage() {
		if (stage === 'recognize') {
			stage = 'resolve';
		} else if (stage === 'resolve') {
			stage = 'recognize';
			fetch_content();
		}
	}

	function fetch_content() {
		const endpoint = 'http://127.0.0.1:5000/api/next_content';
		fetch(endpoint)
			.then((response) => response.json())
			.then((data) => {
				content = removeHtmlContent(data.content);
				// id = data.id;
			})
			.catch((error) => {
				console.error('Error fetching data:', error);
			});
	}

	onMount(() => {
		fetch_content();
	});
</script>

{#if stage == 'recognize'}
	<h2>Choices</h2>
	<ChoiceButtons bind:selected />
	<h2>Content</h2>
	<SelectWords {content} bind:selected enabled={stage == 'recognize'} />
{:else if stage == 'resolve' && selected}
	<h2>Locations</h2>
	<LocationMap location={selected[0]} />
{/if}
<button onclick={advanceStage}>Next</button>

<style lang="scss">
	:global(.scroll-container) {
		border: 1px solid #aaa;
		height: 15rem;
	}
</style>
