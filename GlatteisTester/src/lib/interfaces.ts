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

// [
//   {
//     "configs_json": {
//       "configs": {
//         "gazetteers": {
//           "naturalEarthPopulatedPlaces": {
//             "admin_rank": 4,
//             "index_col": "WOF_ID",
//             "is_contextual": false,
//             "name": "naturalEarthPopulatedPlaces",
//             "names_col": "NAME_DE",
//             "population_column": "POP_MIN"
//           },
//           "natural_earth_countries": {
//             "admin_rank": 0,
//             "index_col": "ADM0_A3",
//             "is_contextual": true,
//             "name": "natural_earth_countries",
//             "names_col": "NAME_DE",
//             "population_column": "POP_EST"
//           },
//           "swissCantons": {
//             "admin_rank": 3,
//             "index_col": "KANTONSNUM",
//             "is_contextual": true,
//             "name": "swissCantons",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           },
//           "swissMunicipalities": {
//             "admin_rank": 1,
//             "index_col": "BFS_NUMMER",
//             "is_contextual": false,
//             "name": "swissMunicipalities",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           }
//         },
//         "language": "de",
//         "recognizer": {
//           "language": "de",
//           "method": "spacy",
//           "model": "de_core_news_sm"
//         },
//         "resolver": {
//           "method": "statistical",
//           "model": null
//         }
//       },
//       "hash": "055479b7d9d8a3807f61"
//     },
//     "label": "055479b7d9d8a3807f61"
//   },
//   {
//     "configs_json": {
//       "configs": {
//         "gazetteers": {
//           "naturalEarthPopulatedPlaces": {
//             "admin_rank": 4,
//             "index_col": "WOF_ID",
//             "is_contextual": false,
//             "name": "naturalEarthPopulatedPlaces",
//             "names_col": "NAME_DE",
//             "population_column": "POP_MIN"
//           },
//           "natural_earth_countries": {
//             "admin_rank": 3,
//             "index_col": "ADM0_A3",
//             "is_contextual": true,
//             "name": "natural_earth_countries",
//             "names_col": "NAME_DE",
//             "population_column": "POP_EST"
//           },
//           "swissCantons": {
//             "admin_rank": 3,
//             "index_col": "KANTONSNUM",
//             "is_contextual": true,
//             "name": "swissCantons",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           },
//           "swissDistricts": {
//             "admin_rank": 2,
//             "index_col": "BEZIRKSNUM",
//             "is_contextual": false,
//             "name": "swissDistricts",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           },
//           "swissMunicipalities": {
//             "admin_rank": 1,
//             "index_col": "BFS_NUMMER",
//             "is_contextual": false,
//             "name": "swissMunicipalities",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           }
//         },
//         "language": "de",
//         "recognizer": {
//           "language": "de",
//           "method": "spacy",
//           "model": "de_core_news_sm"
//         },
//         "resolver": {
//           "method": "statistical",
//           "model": null
//         }
//       },
//       "hash": "eae9b2add8a088590639"
//     },
//     "label": "eae9b2add8a088590639"
//   },
//   {
//     "configs_json": {
//       "configs": {
//         "gazetteers": {
//           "natural_earth_countries": {
//             "admin_rank": 3,
//             "index_col": "ADM0_A3",
//             "is_contextual": true,
//             "name": "natural_earth_countries",
//             "names_col": "NAME_DE",
//             "population_column": "POP_EST"
//           }
//         },
//         "language": "de",
//         "recognizer": {
//           "language": "de",
//           "method": "spacy",
//           "model": "de_core_news_sm"
//         },
//         "resolver": {
//           "method": "statistical",
//           "model": null
//         }
//       },
//       "hash": "27be2956b47f266cf0e6"
//     },
//     "label": "27be2956b47f266cf0e6"
//   },
//   {
//     "configs_json": {
//       "configs": {
//         "gazetteers": {
//           "naturalEarthPopulatedPlaces": {
//             "admin_rank": 4,
//             "index_col": "WOF_ID",
//             "is_contextual": false,
//             "name": "naturalEarthPopulatedPlaces",
//             "names_col": "NAME_DE",
//             "population_column": "POP_MIN"
//           },
//           "natural_earth_countries": {
//             "admin_rank": 0,
//             "index_col": "ADM0_A3",
//             "is_contextual": true,
//             "name": "natural_earth_countries",
//             "names_col": "NAME_DE",
//             "population_column": "POP_EST"
//           },
//           "swissCantons": {
//             "admin_rank": 3,
//             "index_col": "KANTONSNUM",
//             "is_contextual": true,
//             "name": "swissCantons",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           },
//           "swissMunicipalities": {
//             "admin_rank": 1,
//             "index_col": "BFS_NUMMER",
//             "is_contextual": false,
//             "name": "swissMunicipalities",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           }
//         },
//         "language": "de",
//         "recognizer": {
//           "language": "de",
//           "method": "spacy",
//           "model": "de_core_news_lg"
//         },
//         "resolver": {
//           "method": "statistical",
//           "model": null
//         }
//       },
//       "hash": "667847482144ba532965"
//     },
//     "label": "spacy_test"
//   },
//   {
//     "configs_json": {
//       "configs": {
//         "gazetteers": {
//           "naturalEarthPopulatedPlaces": {
//             "admin_rank": 4,
//             "index_col": "WOF_ID",
//             "is_contextual": false,
//             "name": "naturalEarthPopulatedPlaces",
//             "names_col": "NAME_DE",
//             "population_column": "POP_MIN"
//           },
//           "natural_earth_countries": {
//             "admin_rank": 0,
//             "index_col": "ADM0_A3",
//             "is_contextual": true,
//             "name": "natural_earth_countries",
//             "names_col": "NAME_DE",
//             "population_column": "POP_EST"
//           },
//           "swissCantons": {
//             "admin_rank": 3,
//             "index_col": "KANTONSNUM",
//             "is_contextual": true,
//             "name": "swissCantons",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           },
//           "swissMunicipalities": {
//             "admin_rank": 1,
//             "index_col": "BFS_NUMMER",
//             "is_contextual": false,
//             "name": "swissMunicipalities",
//             "names_col": "NAME",
//             "population_column": "EINWOHNERZ"
//           }
//         },
//         "language": "de",
//         "recognizer": {
//           "language": "de",
//           "method": "stanza",
//           "model": "de"
//         },
//         "resolver": {
//           "method": "statistical",
//           "model": null
//         }
//       },
//       "hash": "b43b9dcb9fb1b6178e5b"
//     },
//     "label": "stanza_test"
//   }
// ]

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
