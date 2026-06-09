<script lang="ts">
	import type { CodedLoc } from '$lib/interfaces';
	let { codedLocs }: { codedLocs?: CodedLoc[] } = $props();

	import * as HoverCard from '$lib/components/ui/hover-card/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import Separator from '$lib/components/ui/separator/separator.svelte';

	// Sort by geoparser_label
	let foundLocsByGeoparser: { [key: string]: CodedLoc[] } = $derived(
		codedLocs
			?.filter((loc) => loc.location_id !== null)
			?.reduce(
				(acc, loc) => {
					if (loc.geoparser_label) {
						acc[loc.geoparser_label] = acc[loc.geoparser_label] ?? [];
						acc[loc.geoparser_label].push(loc);
					}
					return acc;
				},
				{} as { [key: string]: CodedLoc[] }
			) ?? {}
	);

	let nullLocsByGeoparser: { [key: string]: CodedLoc[] } = $derived(
		codedLocs
			?.filter((loc) => loc.location_id === null)
			?.reduce(
				(acc, loc) => {
					if (loc.geoparser_label) {
						acc[loc.geoparser_label] = acc[loc.geoparser_label] ?? [];
						acc[loc.geoparser_label].push(loc);
					}
					return acc;
				},
				{} as { [key: string]: CodedLoc[] }
			) ?? {}
	);
</script>

{#snippet codedLoc(loc: CodedLoc)}
	<HoverCard.Root>
		<HoverCard.Trigger>
			<div class="rounded-lg bg-muted p-2">
				{loc.location_name}
			</div>
		</HoverCard.Trigger>
		<HoverCard.Content>
			<div class="flex flex-col">
				<div>Content Name: {loc.location_name}</div>
				<div>Location ID: {loc.location_id ?? 'None'}</div>
			</div>
		</HoverCard.Content>
	</HoverCard.Root>
{/snippet}

<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
	<Card.Root class="grow">
		<Card.Header>
			<Card.Title class="font-heading text-2xl">Resolved Locations</Card.Title>
			<Card.Description>These are the locations resolved by each geoparser.</Card.Description>
		</Card.Header>
		<Card.Content>
			{#each Object.entries(foundLocsByGeoparser) as [geoparser, locs] (geoparser)}
				<div>
					<Separator class="my-4" />
					<h3 class="mb-4 font-heading text-lg text-muted-foreground">Geoparser: {geoparser}</h3>
					<div class="flex flex-wrap gap-1">
						{#each locs as loc (loc.id)}
							{@render codedLoc(loc)}
						{/each}
					</div>
				</div>
			{:else}
				<div class="flex h-full min-h-12 items-center justify-center text-muted-foreground">
					No locations resolved.
				</div>
			{/each}
		</Card.Content>
	</Card.Root>

	<Card.Root>
		<Card.Header>
			<Card.Title class="font-heading text-2xl">Unresolved Locations</Card.Title>
			<Card.Description>
				These are the locations that could not be resolved by any geoparser.
			</Card.Description>
		</Card.Header>
		<Card.Content>
			{#each Object.entries(nullLocsByGeoparser) as [geoparser, locs] (geoparser)}
				<div>
					<Separator class="my-4" />
					<h3 class="mb-4 font-heading text-lg text-muted-foreground">Geoparser: {geoparser}</h3>
					<div class="flex flex-wrap gap-1">
						{#each locs as loc (loc.id)}
							{@render codedLoc(loc)}
						{/each}
					</div>
				</div>
			{:else}
				<div class="flex h-full min-h-12 items-center justify-center text-muted-foreground">
					No locations unresolved.
				</div>
			{/each}
		</Card.Content>
	</Card.Root>
</div>
