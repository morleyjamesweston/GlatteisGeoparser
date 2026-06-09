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

export interface ResolutionRatio {
	resolved: number;
	unresolved: number;
}

export interface GeoParserEvaluation {
	total_locs_per_geoparser: {
		[key: string]: ResolutionRatio;
	};
}

export interface GeoParserAgreementMetrics {
	location_id_assigned_ratio_per_geoparser: Array<{
		geoparser_label: string;
		ratio: number;
	}>;
	inter_geoparser_agreement_ratio: Array<{
		geoparser1: string;
		geoparser2: string;
		agreement_ratio: number;
		common_entries: number;
	}>;
	gazetteer_distribution_per_geoparser: Array<{
		geoparser_label: string;
		gazetteer_distribution: Array<{
			gazetteer: string;
			count: number;
		}>;
	}>;
	avg_unique_location_ids_per_content_id: number;
	entries_with_location_id_per_geoparser: Array<{
		geoparser_label: string;
		count: number;
	}>;
	entries_without_location_id_per_geoparser: Array<{
		geoparser_label: string;
		count: number;
	}>;
	top_10_common_location_ids_per_geoparser: Array<{
		geoparser_label: string;
		top_10_location_ids: Array<{
			location_id: string;
			count: number;
		}>;
	}>;
}
