<script lang="ts">
	import type { CodedLocHuman } from '$lib/interfaces';
	let { codedLocs }: { codedLocs?: CodedLocHuman[] } = $props();

	import * as HoverCard from '$lib/components/ui/hover-card/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import Separator from '$lib/components/ui/separator/separator.svelte';

	// Sort by geoparser_label
	let foundLocsByGeoparser: { [key: string]: CodedLocHuman[] } = $derived(
		codedLocs
			?.filter((loc) => loc.location_id !== null)
			?.reduce(
				(acc, loc) => {
					if (loc.user_id) {
						acc[loc.user_id] = acc[loc.user_id] ?? [];
						acc[loc.user_id].push(loc);
					}
					return acc;
				},
				{} as { [key: string]: CodedLocHuman[] }
			) ?? {}
	);

	let nullLocsByGeoparser: { [key: string]: CodedLocHuman[] } = $derived(
		codedLocs
			?.filter((loc) => loc.location_id === null)
			?.reduce(
				(acc, loc) => {
					if (loc.user_id) {
						acc[loc.user_id] = acc[loc.user_id] ?? [];
						acc[loc.user_id].push(loc);
					}
					return acc;
				},
				{} as { [key: string]: CodedLocHuman[] }
			) ?? {}
	);
</script>

{#snippet codedLoc(loc: CodedLocHuman)}
	<HoverCard.Root>
		<HoverCard.Trigger>
			<div class="rounded-lg bg-muted px-2 py-1">
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

<div class="grid grow grid-cols-1 gap-4 md:grid-cols-2">
	<Card.Root class="grow">
		<Card.Header>
			<Card.Title>Resolved Locations</Card.Title>
			<Card.Description>These are the locations resolved by each geoparser.</Card.Description>
		</Card.Header>
		<Card.Content>
			{#each Object.entries(foundLocsByGeoparser) as [geoparser, locs] (geoparser)}
				<div>
					<h3 class="mb-1 font-heading text-muted-foreground">Geoparser: {geoparser}</h3>
					<div class="flex flex-wrap gap-1">
						{#each locs as loc (loc.id)}
							{@render codedLoc(loc)}
						{/each}
					</div>
					<Separator class="mt-2" />
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
			<Card.Title>Unresolved Locations</Card.Title>
			<Card.Description>These are the locations that could not be resolved.</Card.Description>
		</Card.Header>
		<Card.Content>
			{#each Object.entries(nullLocsByGeoparser) as [geoparser, locs] (geoparser)}
				<div>
					<h3 class="mb-1 font-heading text-muted-foreground">Geoparser: {geoparser}</h3>
					<div class="flex flex-wrap gap-1">
						{#each locs as loc (loc.id)}
							{@render codedLoc(loc)}
						{/each}
					</div>
					<Separator class="mt-2" />
				</div>
			{:else}
				<div class="flex h-full min-h-12 items-center justify-center text-muted-foreground">
					No locations unresolved.
				</div>
			{/each}
		</Card.Content>
	</Card.Root>
</div>
