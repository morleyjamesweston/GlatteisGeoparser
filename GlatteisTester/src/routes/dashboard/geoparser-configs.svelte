<script lang="ts">
	import { apiGet } from '$lib/api';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Collapsible from '$lib/components/ui/collapsible/index.js';
	import ChevronsUpDownIcon from '@lucide/svelte/icons/chevrons-up-down';
	import { buttonVariants } from '$lib/components/ui/button/index.js';

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	let allConfigs: any[] = $state([]);

	async function getGeoParserConfigs() {
		try {
			const data = await apiGet(`/api/dashboard/geoparser_configs`);
			console.log(data);
			allConfigs = data;
		} catch (err) {
			console.error('Error fetching article text:', err);
		}
	}

	// 	{
	//   "configs": {
	//     "gazetteers": {
	//       "naturalEarthPopulatedPlaces": {
	//         "admin_rank": 4,
	//         "index_col": "WOF_ID",
	//         "is_contextual": false,
	//         "name": "naturalEarthPopulatedPlaces",
	//         "names_col": "NAME_DE",
	//         "population_column": "POP_MIN"
	//       },
	//       "natural_earth_countries": {
	//         "admin_rank": 0,
	//         "index_col": "ADM0_A3",
	//         "is_contextual": true,
	//         "name": "natural_earth_countries",
	//         "names_col": "NAME_DE",
	//         "population_column": "POP_EST"
	//       },
	//       "swissCantons": {
	//         "admin_rank": 3,
	//         "index_col": "KANTONSNUM",
	//         "is_contextual": true,
	//         "name": "swissCantons",
	//         "names_col": "NAME",
	//         "population_column": "EINWOHNERZ"
	//       },
	//       "swissMunicipalities": {
	//         "admin_rank": 1,
	//         "index_col": "BFS_NUMMER",
	//         "is_contextual": false,
	//         "name": "swissMunicipalities",
	//         "names_col": "NAME",
	//         "population_column": "EINWOHNERZ"
	//       }
	//     },
	//     "language": "de",
	//     "recognizer": {
	//       "language": "de",
	//       "method": "spacy",
	//       "model": "de_core_news_sm"
	//     },
	//     "resolver": {
	//       "method": "statistical",
	//       "model": null
	//     }
	//   },
	//   "hash": "055479b7d9d8a3807f61"
	// }

	onMount(() => {
		getGeoParserConfigs();
	});
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Geoparser configs</Card.Title>
		<Card.Description>These are the geoparser configs tested so far.</Card.Description>
	</Card.Header>
	<Card.Content>
		{#each allConfigs as config (config.label)}
			{@const configData = config.configs_json}
			<Collapsible.Root class="w-full space-y-2">
				<div class="flex items-center justify-between">
					<h4 class="text-sm font-semibold">{config.label}</h4>
					<Collapsible.Trigger
						class={buttonVariants({ variant: 'ghost', size: 'sm', class: 'w-9 p-0' })}
					>
						<ChevronsUpDownIcon />
						<span class="sr-only">Toggle</span>
					</Collapsible.Trigger>
				</div>
				<Collapsible.Content class="space-y-2">
					<p><span class="font-bold">Hash:</span> {configData.hash}</p>
					<ul>
						<pre>{JSON.stringify(configData, null, 2)}</pre>
					</ul>
				</Collapsible.Content>
			</Collapsible.Root>
		{/each}
	</Card.Content>
</Card.Root>

<!-- <pre>{JSON.stringify(allConfigs, null, 2)}</pre> -->
