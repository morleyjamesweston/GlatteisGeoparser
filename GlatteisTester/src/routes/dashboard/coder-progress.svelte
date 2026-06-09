<script lang="ts">
	import { Progress } from '$lib/components/ui/progress/index.js';
	import ScrollArea from '$lib/components/ui/scroll-area/scroll-area.svelte';
	import { Skeleton } from '$lib/components/ui/skeleton/index.js';
	import type { CodingProgress } from '$lib/interfaces';
	import * as Card from '$lib/components/ui/card/index.js';
	import { onMount } from 'svelte';
	import { apiGet } from '$lib/api';

	let progress: CodingProgress | null = $state(null);

	async function getProgress() {
		try {
			const data = await apiGet('/api/dashboard/coding_progress');
			console.log('Coding progress data:', data);
			progress = data;
		} catch (err) {
			console.error('Error fetching all coded data:', err);
		}
	}

	onMount(() => {
		getProgress();
		const setIntervalId = setInterval(getProgress, 10000);
		return () => clearInterval(setIntervalId);
	});
	// let { progress }: { progress: CodingProgress | null } = $props();
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Coding Progress</Card.Title>
		<Card.Description>Here you can see the coding progress of each human coder.</Card.Description>
	</Card.Header>
	<Card.Content>
		<ScrollArea class="h-40 w-full">
			<div class="flex flex-col gap-2">
				{#if progress}
					{#each progress.coding_progress as coder (coder.user_id)}
						<div class="flex items-center gap-4 px-2">
							<span>{coder.username}</span>
							<Progress value={(coder.coded_count / progress.total_test_data) * 100} />
							<div class="text-nowrap">{coder.coded_count} / {progress.total_test_data}</div>
						</div>
					{/each}
				{:else}
					<Skeleton class="h-4 w-full" />
					<Skeleton class="h-4 w-full" />
					<Skeleton class="h-4 w-full" />
					<Skeleton class="h-4 w-full" />
					<Skeleton class="h-4 w-full" />
				{/if}
			</div>
		</ScrollArea>
	</Card.Content>
</Card.Root>
