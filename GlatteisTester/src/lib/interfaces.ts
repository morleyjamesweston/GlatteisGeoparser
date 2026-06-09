export interface ReturnGeoDataFeature {
	id: string | null;
	original_names: string;
	original_index: number | string | null;
	gazetteer_name: string | null;
}

export interface CodingProgress {
	coding_progress: Array<{
		coded_count: number;
		user_id: number;
		username: string;
	}>;
	total_test_data: number;
}

export interface CodedLoc {
	content_id: string;
	geoparser_label: string;
	id: number;
	location_id: number | null;
	location_name: string;
}
