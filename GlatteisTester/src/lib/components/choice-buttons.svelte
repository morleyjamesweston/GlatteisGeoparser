<script lang="ts">
	import Skeleton from '$lib/primitives/skeleton.svelte';
	import { stripPunctuation } from '$lib/utilities/strip-punctuation';
	import Button from './ui/button/button.svelte';

	let { selected = $bindable() }: { selected: string[] } = $props();

	let uniqueSelected = $derived(
		selected
			.map((item) => item.trim())
			.filter((item) => item.length > 0)
			.filter((item, index, self) => self.indexOf(item) === index)
	);
</script>

<div class="h-16 w-full">
	{#each uniqueSelected as item, idx (`${item}-${idx}`)}
		<Button
			size="lg"
			onclick={() => {
				selected = selected.filter((_, i) => i !== idx);
			}}
		>
			{stripPunctuation(item)}
		</Button>
	{:else}
		<Skeleton height={4} text="Please identify all locations in the text." />
	{/each}
</div>
