<script lang="ts">
	import 'ol/ol.css';
	import Map from 'ol/Map';
	import View from 'ol/View';
	import OSM from 'ol/source/OSM.js';
	import TileLayer from 'ol/layer/Tile.js';
	import { geoDataStore } from '$lib/stores/geodata.svelte';

	import './map-style.css';
	import GeoJSON from 'ol/format/GeoJSON.js';
	import VectorSource from 'ol/source/Vector.js';
	import { Fill, Stroke, Style } from 'ol/style.js';
	import VectorLayer from 'ol/layer/Vector.js';
	import { stripPunctuation } from '$lib/utilities/strip-punctuation';
	import FeatureChoices from './feature-choices.svelte';

	let { location } = $props();
	let map: Map | null = null;
	let geodata = $state(null);
	let features = $state([]);
	let hoveredFeature = $state<string | null>(null);
	let selectedFeature = $state<string>('');

	function fetch_location_choices(location: string) {
		const endpoint = 'http://localhost:5000/api/get_location_choices';
		const url = new URL(endpoint);
		url.searchParams.append('location', location);
		fetch(url)
			.then((response) => response.text())
			.then((text) => {
				let data: any = text;

				// Handle double-encoded JSON from backend
				if (typeof data === 'string') {
					try {
						data = JSON.parse(data);
					} catch (e) {
						console.error('First JSON parse failed:', e);
						return;
					}
				}

				// Try parsing again if still a string (double-encoded)
				if (typeof data === 'string') {
					try {
						data = JSON.parse(data);
					} catch (e) {
						console.error('Second JSON parse failed:', e);
						return;
					}
				}

				if (data && typeof data === 'object') {
					if (Array.isArray(data.features)) {
						geodata = data;
						features = data.features;
					}
				}
			})
			.catch((error) => {
				console.error('Error fetching location choices:', error);
			});
	}

	let DEFAULT_CENTER = [965919.0, 6012370.0];
	let DEFAULT_ZOOM = 10.5;

	$effect(() => {
		if (map && geodata) {
			const vectorSource = new VectorSource({
				features: new GeoJSON().readFeatures(geodata, {
					featureProjection: 'EPSG:3857'
				})
			});
			const style = new Style({
				fill: new Fill({
					color: 'rgba(255, 0, 0, 0.1)'
				}),
				stroke: new Stroke({
					color: 'red',
					width: 2
				})
			});
			const vectorLayer = new VectorLayer({
				source: vectorSource,
				style: style
			});
			map.addLayer(vectorLayer);
			console.log('Layer added successfully with', vectorSource.getFeatures().length, 'features');
			centerMapOnGeoData(geodata);
		}
	});

	function centerMapOnGeoData(geoData: any) {
		if (map && geoData) {
			const features = new GeoJSON().readFeatures(geoData, {
				featureProjection: 'EPSG:3857'
			});
			if (features.length > 0) {
				const extent = features[0].getGeometry()?.getExtent();
				if (extent) {
					map.getView().fit(extent, { padding: [20, 20, 20, 20] });
				}
			}
		}
	}

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

	// function addLayerFromGeodataStore() {
	// 	const geoData = geoDataStore.geoData;
	// 	if (map && geoData) {
	// 		const vectorSource = new VectorSource({
	// 			features: new GeoJSON().readFeatures(geoData, {
	// 				featureProjection: 'EPSG:3857'
	// 			})
	// 		});
	// 		const style = new Style({
	// 			fill: new Fill({
	// 				color: 'rgba(255, 0, 0, 0.5)'
	// 			}),
	// 			stroke: new Stroke({
	// 				color: 'red',
	// 				width: 2
	// 			})
	// 		});
	// 		const vectorLayer = new VectorLayer({
	// 			source: vectorSource,
	// 			style: style
	// 		});
	// 		map.addLayer(vectorLayer);
	// 		console.log('Layer added successfully with', vectorSource.getFeatures().length, 'features');
	// 	} else {
	// 		console.warn('Map or geoData not available', { map: !!map, geoData: !!geoData });
	// 	}
	// }

	$effect(() => {
		if (location) {
			fetch_location_choices(stripPunctuation('luzern'));
		}
	});

	$effect(() => {
		if (geoDataStore.dataLoaded) {
			// addLayerFromGeodataStore();
		}
	});
</script>

<div id="mainMap" use:setupMap></div>
<h2>Identify the correct feature:</h2>
<FeatureChoices {features} bind:hovered={hoveredFeature} bind:value={selectedFeature} />

{hoveredFeature}
{selectedFeature}

<!-- <script lang="ts">
	// OpenLayers
	import Map from 'ol/Map';
	import View from 'ol/View';
	import GeoJSON from 'ol/format/GeoJSON.js';
	import VectorSource from 'ol/source/Vector.js';
	import VectorLayer from 'ol/layer/Vector.js';
	import Select from 'ol/interaction/Select.js';
	import { pointerMove } from 'ol/events/condition.js';
	import { easeOut } from 'ol/easing.js';
	import { Feature } from 'ol';
	import { Fill, Stroke, Style } from 'ol/style.js';

	import simpleCantonVectors from '$lib/geodata/swiss_cantons_simplified.json';
	import simpleZurichVectors from '$lib/geodata/swiss_gemeinde_simplified.json';

	let { selectedLocation = $bindable() } = $props();

	let mapId = 'mainMap';
	let map: Map | null = null;

	let DEFAULT_CENTER = [965919.0, 6012370.0];
	let DEFAULT_ZOOM = 10.5;

	let selectedFeature: Feature | null = $state(null);

	const setupMap = (node: HTMLElement) => {
		const cantonLayer = new VectorLayer({
			source: new VectorSource({
				features: new GeoJSON().readFeatures(simpleCantonVectors)
			}),
			style: () => {
				return new Style({
					fill: new Fill({
						color: '#112'
					}),
					stroke: new Stroke({
						color: '#234',
						width: 3
					})
				});
			}
		});
		const gemeindeLayer = new VectorLayer({
			source: new VectorSource({
				features: new GeoJSON().readFeatures(simpleZurichVectors)
			}),
			style: () => {
				return new Style({
					fill: new Fill({
						color: '#111'
					}),
					stroke: new Stroke({
						color: '#456',
						width: 1
					})
				});
			}
		});

		map = new Map({
			target: node.id,
			layers: [cantonLayer, gemeindeLayer],
			view: new View({
				center: DEFAULT_CENTER,
				zoom: DEFAULT_ZOOM
			})
		});

		const pointerHover = new Select({
			condition: pointerMove,
			layers: [gemeindeLayer],
			style: () => {
				return new Style({
					fill: new Fill({
						color: '#8ac'
					}),
					stroke: new Stroke({
						color: '#777',
						width: 1
					})
				});
			}
		});
		map.addInteraction(pointerHover);

		const pointerClick = new Select({
			layers: [gemeindeLayer],
			style: () => {
				return new Style({
					fill: new Fill({
						color: '#222'
					}),
					stroke: new Stroke({
						color: '#777',
						width: 1
					})
				});
			}
		});
		map.addInteraction(pointerClick);

		let selectedFeatures = pointerClick.getFeatures();
		selectedFeatures.on('add', (event) => {
			if (!map) return;
			let feature = event.target.item(0);
			if (!feature) return;
			selectedFeature = feature;
			let long = feature.get('centroid_long');
			// console.log(feature.get('BFS_NUMMER'));
			selectedLocation = feature.get('BFS_NUMMER');
			let lat = feature.get('centroid_lat');
			let targetZoom = map
				.getView()
				.getZoomForResolution(
					map.getView().getResolutionForExtent(feature.getGeometry().getExtent(), map.getSize())
				);
			updateMapCenter(long, lat, targetZoom ? targetZoom * 0.95 : DEFAULT_ZOOM);
		});
		return {
			destroy() {
				if (map) {
					map = null;
				}
			}
		};
	};

	function updateMapCenter(long: number, lat: number, zoom: number) {
		if (!map) {
			return;
		}
		map.getView().animate({ center: [long, lat], zoom: zoom, duration: 250, easing: easeOut });
	}
</script>

<div id={mapId} class="h-full w-full bg-gray-800" use:setupMap></div>
<div class="absolute top-4 right-4 rounded bg-neutral-800/50 p-2 text-white">
	<p>Selected: {selectedFeature?.get('NAME')}</p>
</div> -->

<style lang="scss">
	#mainMap {
		width: 100%;
		height: 40rem;
		border: 1px solid #aaa;
	}
</style>
