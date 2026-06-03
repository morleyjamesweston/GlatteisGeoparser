<script lang="ts">
	import ChoiceButtons from '$lib/components/choice-buttons.svelte';
	import LocationMap from '$lib/components/location-map.svelte';
	import SelectWords from '$lib/components/select-words.svelte';
	import { onMount } from 'svelte';

	let content: string | null = $state(null);
	let selected = $state([]);

	let stage: 'recognize' | 'resolve' = $state('recognize');

	function fetch_next() {
		const endpoint = 'http://127.0.0.1:5000/api/next_content';
		fetch(endpoint)
			.then((response) => response.json())
			.then((data) => {
				console.log('Received data:', data);
				content = data.content;
			})
			.catch((error) => {
				console.error('Error fetching data:', error);
			});
	}

	onMount(() => {
		fetch_next();
	});
</script>

<h2>Content</h2>
<SelectWords {content} bind:selected enabled={stage == 'recognize'} />
<h2>Choices</h2>
<ChoiceButtons bind:selected />
<h2>Locations</h2>
<LocationMap />
<button onclick={fetch_next}>Submit</button>

<style lang="scss">
	:global(.scroll-container) {
		border: 1px solid #aaa;
		height: 15rem;
	}
</style>
