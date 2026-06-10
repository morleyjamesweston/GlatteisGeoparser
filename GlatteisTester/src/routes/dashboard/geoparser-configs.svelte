<script lang="ts">
	import { apiGet } from '$lib/api';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Collapsible from '$lib/components/ui/collapsible/index.js';
	import ChevronsUpDownIcon from '@lucide/svelte/icons/chevrons-up-down';
	import { buttonVariants } from '$lib/components/ui/button/index.js';
	import Separator from '$lib/components/ui/separator/separator.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import { toast } from 'svelte-sonner';

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

	onMount(() => {
		getGeoParserConfigs();
	});
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Geoparser Configs</Card.Title>
		<Card.Description>These are the geoparser configs tested so far.</Card.Description>
	</Card.Header>
	<Card.Content>
		{#each allConfigs as config (config.label)}
			{@const configData = config.configs_json.configs}
			{@const gazetteers = Object.keys(configData.gazetteers)}
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
					<Separator />
					<p>
						<span class="font-bold text-muted-foreground">Hash:</span>
						{config.configs_json.hash}
					</p>
					<Separator />
					<h5 class="text-sm font-semibold">Gazetteers:</h5>
					<ul class="list-disc pl-3">
						{#each gazetteers as gazetteer (gazetteer)}
							<li>{gazetteer}</li>
						{/each}
					</ul>
					<Separator />
					<h5 class="text-sm font-semibold">Recognizer:</h5>
					<p>
						<span class="font-bold text-muted-foreground">Language:</span>
						{configData.recognizer.language}
					</p>
					<p>
						<span class="font-bold text-muted-foreground">Method:</span>
						{configData.recognizer.method}
					</p>
					<p>
						<span class="font-bold text-muted-foreground">Model:</span>
						{configData.recognizer.model}
					</p>
					<h5 class="text-sm font-semibold">Resolver:</h5>
					<p>
						<span class="font-bold text-muted-foreground">Method:</span>
						{configData.resolver.method}
					</p>
					<p>
						<span class="font-bold text-muted-foreground">Model:</span>
						{configData.resolver.model ?? 'None'}
					</p>
					<Button
						class="w-full"
						variant="outline"
						onclick={() => {
							navigator.clipboard.writeText(JSON.stringify(config.configs_json, null, 2));
							toast.success('Copied to clipboard');
						}}>Copy JSON</Button
					>
					<Separator class="mb-4" />
				</Collapsible.Content>
			</Collapsible.Root>
		{/each}
	</Card.Content>
</Card.Root>

<!-- <pre>{JSON.stringify(allConfigs, null, 2)}</pre> -->
