<script lang="ts">
	import 'ol/ol.css';
	import Map from 'ol/Map';
	import View from 'ol/View';
	import OSM from 'ol/source/OSM.js';
	import TileLayer from 'ol/layer/Tile.js';
	import * as Card from '$lib/components/ui/card/index.js';

	import { apiGet } from '$lib/api';

	let { selectedContentID }: { selectedContentID?: string } = $props();
	let geodata = $state('');

	// async function getGeodataForLocations(contentID: string | undefined) {
	// 	if (!contentID) return;
	// 	try {
	// 		const data = await apiGet(`/api/dashboard/loc_geodata?content_id=${contentID}`);
	// 		console.log('Geodata', data);
	// 		geodata = data;
	// 	} catch (err) {
	// 		console.error('Error fetching article geodata:', err);
	// 	}
	// }

	// $effect(() => {
	// 	getGeodataForLocations(selectedContentID);
	// });
	//
	let map: Map | null = null;

	let DEFAULT_CENTER = [965919.0, 6012370.0];
	let DEFAULT_ZOOM = 10.5;
	const setupMap = (node: HTMLElement) => {
		map = new Map({
			target: node.id,
			layers: [
				new TileLayer({
					source: new OSM()
				})
			],
			view: new View({
				center: DEFAULT_CENTER,
				zoom: DEFAULT_ZOOM
			})
		});

		return {
			destroy() {
				if (map) {
					map = null;
				}
			}
		};
	};
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Locations found</Card.Title>
		{#if selectedContentID}
			<Card.Description>These are the locations found in {selectedContentID}</Card.Description>
		{/if}
	</Card.Header>
	<Card.Content>
		<div id="mainMap" class="h-60 w-full" use:setupMap></div>
	</Card.Content>
</Card.Root>
