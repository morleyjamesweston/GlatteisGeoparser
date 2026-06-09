<script lang="ts">
	import type { ResolutionRatio } from '$lib/interfaces';
	import * as Chart from '$lib/components/ui/chart/index.js';
	import * as Card from '$lib/components/ui/card/index.js';

	import { scaleBand } from 'd3-scale';
	import { BarChart, Highlight } from 'layerchart';

	import { cubicInOut } from 'svelte/easing';
	import Skeleton from '$lib/components/ui/skeleton/skeleton.svelte';
	const chartConfig = {
		resolved: {
			label: 'Resolved',
			color: 'var(--color-neutral-400)'
		},
		unresolved: {
			label: 'Unresolved',
			color: 'var(--color-neutral-700)'
		}
	} satisfies Chart.ChartConfig;

	let { resolutionRatios }: { resolutionRatios: { [key: string]: ResolutionRatio } | null } =
		$props();

	let chartData = $derived(
		Object.entries(resolutionRatios ?? {}).map(([geoparser, ratio]) => ({
			geoparser,
			resolved: ratio.resolved,
			unresolved: ratio.unresolved
		}))
	);
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Total locations found per geoparser</Card.Title>
		<Card.Description></Card.Description>
	</Card.Header>
	<Card.Content>
		{#if chartData}
			<Chart.Container config={chartConfig}>
				<BarChart
					data={chartData}
					xScale={scaleBand().padding(0.25)}
					x="geoparser"
					axis="x"
					rule={false}
					series={[
						{
							key: 'resolved',
							label: 'Resolved',
							color: chartConfig.resolved.color,
							props: { rounded: 'bottom' }
						},
						{
							key: 'unresolved',
							label: 'Unresolved',
							color: chartConfig.unresolved.color
						}
					]}
					seriesLayout="stack"
					props={{
						bars: {
							stroke: 'none',
							motion: { type: 'tween', duration: 300, easing: cubicInOut }
						},
						highlight: { area: false }
					}}
					legend
				>
					{#snippet belowMarks()}
						<Highlight area={{ class: 'fill-muted' }} />
					{/snippet}

					{#snippet tooltip()}
						<Chart.Tooltip />
					{/snippet}
				</BarChart>
			</Chart.Container>
		{:else}
			<div class="flex h-60 w-full items-center justify-between gap-2">
				<Skeleton class="h-full w-full" />
				<Skeleton class="h-full w-full" />
				<Skeleton class="h-full w-full" />
				<Skeleton class="h-full w-full" />
				<Skeleton class="h-full w-full" />
				<Skeleton class="h-full w-full" />
			</div>
		{/if}
	</Card.Content>
</Card.Root>
