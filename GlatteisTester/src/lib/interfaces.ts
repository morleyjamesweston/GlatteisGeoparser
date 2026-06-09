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
export interface CodedLocHuman {
	content_id: string;
	user_id: string;
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
	unresolved_locs_per_geoparser: UnresolvedLocsPerGeoparser;
}

export interface UnresolvedLocsPerGeoparser {
	[key: string]: Array<{ count: number; name: string }>;
}

// spacy_test': [{'count': 27, 'name': 'USA'},
//                 {'count': 26, 'name': 'Franken'},
//                 {'count': 21, 'name': 'Kanton'},
//                 {'count': 19, 'name': 'Stadt'},
//                 {'count': 11, 'name': 'Europa'},
//                 {'count': 11, 'name': 'Bund'},
//                 {'count': 10, 'name': 'US-Präsident'},
//                 {'count': 9, 'name': 'China'},
//                 {'count': 9, 'name': 'Landes'},
//                 {'count': 9, 'name': 'NA'},
//                 {'count': 8, 'name': '>'},
//                 {'count': 7, 'name': 'Staaten'},
//                 {'count': 6, 'name': 'Kantons'},
//                 {'count': 5, 'name': 'Corona'},
//                 {'count': 5, 'name': 'schweiz'},
//                 {'count': 5, 'name': 'Tessin'},
//                 {'count': 5, 'name': 'Covid-19'},
//                 {'count': 4, 'name': 'Grossbritannien'},
//                 {'count': 4, 'name': 'Keystone</p></lg></tx'},
//                 {'count': 4, 'name': 'Haus'}],
//  'stanza_test': [{'count': 49, 'name': 'Schweizer'},
//                  {'count': 29, 'name': 'USA'},
//                  {'count': 26, 'name': 'US'},
//                  {'count': 24, 'name': 'Zürcher'},
//                  {'count': 13, 'name': 'Europa'},
//                  {'count': 12, 'name': 'deutsche'},
//                  {'count': 9, 'name': 'China'},
//                  {'count': 8, 'name': 'amerikanische'},
//                  {'count': 7, 'name': 'französischen'},
//                  {'count': 7, 'name': 'deutschen'},
//                  {'count': 6, 'name': 'europäischen'},
//                  {'count': 6, 'name': 'Tessin'},
//                  {'count': 6, 'name': 'britische'},
//                  {'count': 5, 'name': 'Amerika'},
//                  {'count': 5, 'name': 'israelische'},
//                  {'count': 5, 'name': 'Basler'},
//                  {'count': 4, 'name': 'Grossbritannien'},
//                  {'count': 4, 'name': 'britischen'},
//                  {'count': 4, 'name': 'italienischen'},
//                  {'count': 4, 'name': 'Norweger'}]}

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
