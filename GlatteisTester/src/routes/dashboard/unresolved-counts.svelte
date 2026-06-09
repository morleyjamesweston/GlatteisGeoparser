<script lang="ts">
	import type { UnresolvedLocsPerGeoparser } from '$lib/interfaces';
	import * as Collapsible from '$lib/components/ui/collapsible/index.js';
	import ChevronsUpDownIcon from '@lucide/svelte/icons/chevrons-up-down';
	import { buttonVariants } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	let {
		unresolvedLocsPerGeoparser
	}: { unresolvedLocsPerGeoparser: UnresolvedLocsPerGeoparser | null } = $props();
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Most common unresolved locations</Card.Title>
		<Card.Description>Each geoparser has some places that are unresolved.</Card.Description>
	</Card.Header>
	<Card.Content>
		{#if unresolvedLocsPerGeoparser}
			{#each Object.entries(unresolvedLocsPerGeoparser) as [geoparser, locs] (geoparser)}
				<Collapsible.Root class="w-full space-y-2">
					<div class="flex items-center justify-between">
						<h4 class="text-sm font-semibold">{geoparser}</h4>
						<Collapsible.Trigger
							class={buttonVariants({ variant: 'ghost', size: 'sm', class: 'w-9 p-0' })}
						>
							<ChevronsUpDownIcon />
							<span class="sr-only">Toggle</span>
						</Collapsible.Trigger>
					</div>
					<Collapsible.Content class="space-y-2">
						<ul>
							{#each locs.slice(0, 10) as loc (loc.name)}
								<li class="list-disc pl-2">{loc.name}: {loc.count}</li>
							{/each}
						</ul>
					</Collapsible.Content>
				</Collapsible.Root>
			{/each}
		{/if}
	</Card.Content>
</Card.Root>
