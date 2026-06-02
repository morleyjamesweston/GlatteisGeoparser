<script lang="ts">
	let { content, selected = $bindable([]) }: { content: string | null; selected: string[] } =
		$props();

	let splitWords = $derived(content ? content.split(/\s+/).slice(0, 50) : []);
	let selectedRanges: Array<{ start: number; end: number }> = $state([]);

	let currentHovered: number | null = $state(null);
	let hoveredRange = $derived.by(() => {
		if (currentHovered !== null && selectStart !== null) {
			const [start, end] = [currentHovered, selectStart].sort((a, b) => a - b);
			return [start, end];
		} else {
			return null;
		}
	});

	let selectStart: number | null = $state(null);
	let selectEnd: number | null = $state(null);

	function isInSelectedRanges(start: number, end: number) {
		return selectedRanges.some(
			(range) =>
				(start >= range.start && start <= range.end) ||
				(end >= range.start && end <= range.end) ||
				(start <= range.start && end >= range.end)
		);
	}

	function removeFromSelected() {
		if (selectStart !== null && selectEnd !== null) {
			const [start, end] = [selectStart, selectEnd].sort((a, b) => a - b);
			selected = selected.filter((_, idx) => {
				const range = selectedRanges[idx];
				return !(range.start >= start && range.end <= end);
			});
			selectedRanges = selectedRanges.filter(
				(range) => !(range.start >= start && range.end <= end)
			);
		}
	}

	function addRangeToSelected() {
		if (selectStart !== null && selectEnd !== null) {
			const [start, end] = [selectStart, selectEnd].sort((a, b) => a - b);
			const selectedWords = splitWords.slice(start, end + 1).join(' ');
			selected = [...selected, selectedWords];
			selectedRanges = [...selectedRanges, { start, end }];
		}
	}
</script>

<div class="select-container">
	{#each splitWords as word, idx (`${idx}-${word}`)}
		{@render selectableWord(word, idx)}
	{/each}
</div>
{selected}

{#snippet selectableWord(word: string, idx: number)}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div
		onmouseenter={() => {
			currentHovered = idx;
		}}
		onmousedown={() => {
			selectStart = idx;
		}}
		onmouseup={() => {
			selectEnd = idx;
			const isInSelected = isInSelectedRanges(selectStart!, selectEnd);
			if (isInSelected) {
				removeFromSelected();
			} else {
				addRangeToSelected();
			}
			selectStart = null;
			selectEnd = null;
		}}
		class="word
		{hoveredRange && hoveredRange[0] <= idx && hoveredRange[1] >= idx ? 'hovered' : ''}

		{isInSelectedRanges(idx, idx) ? 'selected' : ''}"
	>
		{word}
	</div>
{/snippet}

<style lang="scss">
	.word {
		border: none;
		background: none;
		font-size: 1.2rem;
		transition: background 0.2s ease;
		cursor: pointer;
		user-select: none;
		padding: 0.5rem 0.2rem;
	}

	.word.hovered {
		background: blue;
	}

	.selected {
		background: red;
	}

	.select-container {
		display: flex;
		/* row-gap: 0.5rem; */
		/* column-gap: 0.2rem; */
		flex-wrap: wrap;
	}
</style>
