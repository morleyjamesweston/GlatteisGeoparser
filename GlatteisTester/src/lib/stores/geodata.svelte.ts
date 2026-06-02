export class GeoDataStore {
	geoData = $state(null);

	loadGeoData() {
		fetch('http://127.0.0.1:5000/api/get_geodata')
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				this.geoData = data;
			})
			.catch((error) => {
				console.error('Error fetching geodata:', error);
			});
	}
}

export const geoDataStore = new GeoDataStore();
