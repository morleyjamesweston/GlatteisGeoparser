<script lang="ts">
	import * as Card from '$lib/components/ui/card/index.js';
	import ScrollArea from '$lib/components/ui/scroll-area/scroll-area.svelte';
	let { location, text }: { location: string; text: string | null } = $props();

	// Get all occurrences of the location in the text with 50 chars before and after
	let snippets: Array<{ before: string; after: string }> = $derived.by(() => {
		if (!text || !location) return [];

		const result: Array<{ before: string; after: string }> = [];
		const locationLower = location.toLowerCase();
		const textLower = text.toLowerCase();

		let searchStart = 0;
		let index = textLower.indexOf(locationLower, searchStart);

		while (index !== -1) {
			const beforeStart = Math.max(0, index - 80);
			const afterEnd = Math.min(text.length, index + location.length + 80);

			result.push({
				before: text.substring(beforeStart, index),
				after: text.substring(index + location.length, afterEnd)
			});

			searchStart = index + 1;
			index = textLower.indexOf(locationLower, searchStart);
		}

		return result;
	});
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Text snippets</Card.Title>
		<Card.Description
			>This is where <span class="font-bold text-foreground">{location}</span> was used in the text:
		</Card.Description>
	</Card.Header>
	<Card.Content class="flex flex-col gap-4">
		<ScrollArea class="h-120">
			{#each snippets as snippet, i (i)}
				<div class="text-sm">
					<span class="text-muted-foreground">...{snippet.before}</span>
					<span class="font-bold text-foreground">{location}</span>
					<span class="text-muted-foreground">{snippet.after}...</span>
				</div>
			{:else}
				<div class="text-muted-foreground">No occurrences found</div>
			{/each}
		</ScrollArea>
	</Card.Content>
</Card.Root>
