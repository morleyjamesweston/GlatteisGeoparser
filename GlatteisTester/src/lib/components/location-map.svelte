<script lang="ts">
	import Map from 'ol/Map';
	import View from 'ol/View';
	import OSM from 'ol/source/OSM.js';
	import TileLayer from 'ol/layer/Tile.js';

	import './map-style.css';
	// import GeoJSON from 'ol/format/GeoJSON.js';
	// import VectorSource from 'ol/source/Vector.js';
	// import VectorLayer from 'ol/layer/Vector.js';
	// import Select from 'ol/interaction/Select.js';
	// import { pointerMove } from 'ol/events/condition.js';
	// import { easeOut } from 'ol/easing.js';
	// import { Feature } from 'ol';
	// import { Fill, Stroke, Style } from 'ol/style.js';

	// let mapId = ;
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

<div id="mainMap" use:setupMap></div>

<style lang="scss">
	#mainMap {
		width: 100%;
		height: 400px;
		border: 1px solid #aaa;
	}
</style>
