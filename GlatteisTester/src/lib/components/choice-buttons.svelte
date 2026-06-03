<script lang="ts">
	import Skeleton from '$lib/primitives/skeleton.svelte';
	import { stripPunctuation } from '$lib/utilities/strip-punctuation';

	let { selected = $bindable() }: { selected: string[] } = $props();

	let uniqueSelected = $derived(
		selected
			.map((item) => item.trim())
			.filter((item) => item.length > 0)
			.filter((item, index, self) => self.indexOf(item) === index)
	);
</script>

<div class="container">
	{#each uniqueSelected as item, idx (`${item}-${idx}`)}
		<button
			onclick={() => {
				selected = selected.filter((_, i) => i !== idx);
			}}
		>
			{stripPunctuation(item)}
		</button>
	{:else}
		<Skeleton height={6} text="Please identify all locations in the text." />
	{/each}
</div>

<style lang="scss">
	.container {
		display: flex;
		min-height: 6rem;
		flex-wrap: wrap;
		gap: $spacing-sm;
		align-items: start;
		justify-content: start;
	}
	button {
		border: none;
		background-color: #eee;
		padding: 0.5rem 1rem;
	}
</style>
