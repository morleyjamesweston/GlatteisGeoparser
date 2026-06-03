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
	import type { FeatureLike } from 'ol/Feature';
	import type { StyleFunction } from 'ol/style/Style';
	import VectorLayer from 'ol/layer/Vector.js';
	import { stripPunctuation } from '$lib/utilities/strip-punctuation';
	import FeatureChoices from './feature-choices.svelte';

	let {
		location,
		selectedFeature = $bindable('')
	}: { location: string; selectedFeature?: string } = $props();
	let map: Map | null = null;
	let vectorLayer: VectorLayer<VectorSource> | null = null;
	let geodata: GeoData | null = $state(null);
	let features: Array<GeoDataFeature> = $state([]);
	let hoveredFeature = $state<string | null>(null);
	// let selectedFeature = $state<string>('');

	const defaultStyle = new Style({
		fill: new Fill({
			color: 'rgba(255, 0, 0, 0.1)'
		}),
		stroke: new Stroke({
			color: 'red',
			width: 2
		})
	});
	const hoverStyle = new Style({
		fill: new Fill({
			color: 'rgba(255, 196, 0, 0.35)'
		}),
		stroke: new Stroke({
			color: '#ff7a00',
			width: 3
		})
	});

	const getFeatureId = (feature: FeatureLike) => {
		if ('getId' in feature && typeof feature.getId === 'function') {
			const id = feature.getId();
			if (id != null) {
				return String(id);
			}
		}
		if ('get' in feature && typeof feature.get === 'function') {
			const id = feature.get('id');
			if (id != null) {
				return String(id);
			}
		}
		if ('getProperties' in feature && typeof feature.getProperties === 'function') {
			const props = feature.getProperties() as { id?: unknown } | undefined;
			if (props?.id != null) {
				return String(props.id);
			}
		}
		return null;
	};

	const styleByHover: StyleFunction = (feature) => {
		if (!hoveredFeature || hoveredFeature === 'other') {
			return defaultStyle;
		}
		return getFeatureId(feature) === hoveredFeature ? hoverStyle : defaultStyle;
	};

	// geojson

	interface GeoDataFeature {
		type: string;
		id: string;
		properties: {
			original_names: string;
			gazetteer_name: string;
		};
		geometry: {
			type: string;
			coordinates: unknown;
		};
	}
	interface GeoData {
		type: string;
		features: GeoDataFeature[];
	}

	function fetch_location_choices(location: string) {
		const endpoint = 'http://localhost:5000/api/get_location_choices';
		const url = new URL(endpoint);
		url.searchParams.append('location', location);
		fetch(url)
			.then((response) => response.text())
			.then((text) => {
				let data: unknown = text;

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

				console.log('Parsed location choices data:', data);

				// 				Parsed location choices data:
				// Object { message: "No candidates found for 'Freiberg'" }
				//
				// if this is found, automatically make "none_found" the selected choice and skip the map interaction step

				if (data && typeof data === 'object' && 'message' in data) {
					if (typeof data.message === 'string' && data.message.includes('No candidates found')) {
						selectedFeature = 'none_found';
						hoveredFeature = 'none_found';
						return;
					}
				}

				if (data && typeof data === 'object' && 'features' in data) {
					if (Array.isArray(data.features)) {
						geodata = data as GeoData;
						features = geodata.features as GeoDataFeature[];
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
			if (vectorLayer) {
				map.removeLayer(vectorLayer);
			}
			vectorLayer = new VectorLayer({
				source: vectorSource,
				style: styleByHover
			});
			map.addLayer(vectorLayer);
			console.log('Layer added successfully with', vectorSource.getFeatures().length, 'features');
			centerMapOnGeoData(geodata);
		}
	});

	$effect(() => {
		// eslint-disable-next-line @typescript-eslint/no-unused-expressions
		hoveredFeature;
		if (vectorLayer) {
			vectorLayer.changed();
		}
	});

	function centerMapOnGeoData(geoData: GeoData | null) {
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

	$effect(() => {
		if (location) {
			fetch_location_choices(stripPunctuation(location));
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

<style lang="scss">
	#mainMap {
		width: 100%;
		height: 40rem;
		border: 1px solid #aaa;
	}
</style>
