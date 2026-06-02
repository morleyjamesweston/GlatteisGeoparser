<script lang="ts">
	import LocationMap from '$lib/components/location-map.svelte';
	import SelectWords from '$lib/components/select-words.svelte';
	import { onMount } from 'svelte';
	// import ScrollContainer from '$lib/primitives/scroll-container.svelte';

	let content: string | null = $state(null);

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

	let selected = $state([]);
</script>

<h2>Locations</h2>
<LocationMap />

<h2>Content</h2>
<SelectWords {content} {selected} />
<!-- </ScrollContainer> -->
<h2>Choices</h2>

<button onclick={fetch_next}>Fetch Next</button>

<style lang="scss">
	:global(.scroll-container) {
		border: 1px solid #aaa;
		height: 15rem;
	}
</style>
