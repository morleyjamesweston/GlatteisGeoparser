<script lang="ts">
	import * as Collapsible from '$lib/components/ui/collapsible/index.js';
	import ChevronsUpDownIcon from '@lucide/svelte/icons/chevrons-up-down';
	import { buttonVariants } from '$lib/components/ui/button/index.js';
	import Separator from '$lib/components/ui/separator/separator.svelte';

	import * as Card from '$lib/components/ui/card/index.js';
	import { apiGet } from '$lib/api';
	import { onMount } from 'svelte';

	// accuracy scores for each geoparser config
	let accuracyScores: Record<string, AccuracyResult> = $state({});

	interface AccuracyResult {
		precision: number;
		recall: number;
		f1_score: number;
	}

	async function getAccuracyScores() {
		try {
			const data = await apiGet(`/api/dashboard/geoparser_accuracies`);
			console.log(data);
			accuracyScores = data;
		} catch (err) {
			console.error('Error fetching article text:', err);
		}
	}

	onMount(() => {
		getAccuracyScores();
		const interval = setInterval(getAccuracyScores, 60000);
		return () => clearInterval(interval);
	});
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Geoparser Accuracy</Card.Title>
		<Card.Description>
			Precision, recall, and F1 score for each geoparser configuration.
		</Card.Description>
	</Card.Header>
	<Card.Content>
		{#each Object.entries(accuracyScores) as [config, acc] (config)}
			<Collapsible.Root class="w-full space-y-2">
				<div class="flex items-center justify-between">
					<h4 class="text-sm font-semibold">{config}</h4>
					<Collapsible.Trigger
						class={buttonVariants({ variant: 'ghost', size: 'sm', class: 'w-9 p-0' })}
					>
						<ChevronsUpDownIcon />
						<span class="sr-only">Toggle</span>
					</Collapsible.Trigger>
				</div>
				<Collapsible.Content class="space-y-2">
					<ul>
						<li class="ml-4 list-disc">
							<span class="font-bold text-muted-foreground">Precision:</span>
							{acc.precision}
						</li>
						<li class="ml-4 list-disc">
							<span class="font-bold text-muted-foreground">Recall:</span>
							{acc.recall}
						</li>
						<li class="ml-4 list-disc">
							<span class="font-bold text-muted-foreground">F1 Score:</span>
							{acc.f1_score}
						</li>
					</ul>
					<Separator class="mb-4" />
				</Collapsible.Content>
			</Collapsible.Root>
		{/each}
	</Card.Content>
</Card.Root>
