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
	// import Select from 'ol/interaction/Select.js';
	// import { pointerMove } from 'ol/events/condition.js';
	// import { easeOut } from 'ol/easing.js';
	// import { Feature } from 'ol';

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

	function addLayerFromGeodataStore() {
		const geoData = geoDataStore.geoData;
		if (map && geoData) {
			const vectorSource = new VectorSource({
				features: new GeoJSON().readFeatures(geoData, {
					featureProjection: 'EPSG:3857' // Web Mercator projection (what OSM uses)
				})
			});
			const style = new Style({
				fill: new Fill({
					color: 'rgba(255, 0, 0, 0.5)'
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
		} else {
			console.warn('Map or geoData not available', { map: !!map, geoData: !!geoData });
		}
	}

	$effect(() => {
		if (geoDataStore.dataLoaded) {
			addLayerFromGeodataStore();
		}
	});
</script>

<div id="mainMap" use:setupMap></div>

<style lang="scss">
	#mainMap {
		width: 100%;
		height: 400px;
		border: 1px solid #aaa;
	}
</style>
