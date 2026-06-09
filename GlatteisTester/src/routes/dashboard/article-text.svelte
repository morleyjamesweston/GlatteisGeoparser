<script lang="ts">
	import { apiGet } from '$lib/api';
	import ScrollArea from '$lib/components/ui/scroll-area/scroll-area.svelte';

	let { selectedContentID }: { selectedContentID?: string } = $props();
	let articleText = $state('');

	async function getArticleText(contentID: string | undefined) {
		if (!contentID) return;
		try {
			const data = await apiGet(`/api/content?content_id=${contentID}`);
			console.log(data);
			articleText = data.content;
		} catch (err) {
			console.error('Error fetching article text:', err);
		}
	}

	$effect(() => {
		getArticleText(selectedContentID);
	});
</script>

<ScrollArea class="h-100 rounded-md border p-4">
	{#if articleText}
		{articleText}
	{:else}
		<div class="flex h-full items-center justify-center text-muted-foreground">
			No article selected
		</div>
	{/if}
</ScrollArea>
