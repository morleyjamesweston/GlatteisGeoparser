<script lang="ts">
	import ScrollArea from './ui/scroll-area/scroll-area.svelte';

	let {
		content,
		selected = $bindable([]),
		enabled
	}: { content: string | null; selected: string[]; enabled: boolean } = $props();

	let splitWords = $derived(content ? content.split(/\s+/) : []);

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

	// Normalize words by removing punctuation for comparison
	function normalizeWord(word: string): string {
		return word.replace(/[^\w\s]/g, '').toLowerCase();
	}

	function isInSelectedRanges(start: number, end: number) {
		return selectedRanges.some(
			(range) =>
				(start >= range.start && start <= range.end) ||
				(end >= range.start && end <= range.end) ||
				(start <= range.start && end >= range.end)
		);
	}

	function rebuildRangesFromSelected() {
		const newRanges: Array<{ start: number; end: number }> = [];

		selected.forEach((selectedText) => {
			const trimmedText = selectedText.trim();
			if (trimmedText.length === 0) return;

			const selectedWords = trimmedText.split(/\s+/);
			const normalizedSelectedWords = selectedWords.map(normalizeWord);

			// Find all ranges in the document that match this exact phrase
			for (let i = 0; i <= splitWords.length - selectedWords.length; i++) {
				let matches = true;
				for (let j = 0; j < selectedWords.length; j++) {
					if (normalizeWord(splitWords[i + j]) !== normalizedSelectedWords[j]) {
						matches = false;
						break;
					}
				}

				if (matches) {
					const start = i;
					const end = i + selectedWords.length - 1;
					if (!newRanges.some((r) => r.start === start && r.end === end)) {
						newRanges.push({ start, end });
					}
				}
			}
		});

		selectedRanges = newRanges;
	}

	$effect(() => {
		rebuildRangesFromSelected();
	});

	function removeFromSelected() {
		if (selectStart !== null && selectEnd !== null) {
			const [start, end] = [selectStart, selectEnd].sort((a, b) => a - b);

			// Find which phrase contains this clicked word
			const phrasesToRemove: string[] = [];

			selected.forEach((phrase) => {
				const trimmedPhrase = phrase.trim();
				if (trimmedPhrase.length === 0) return;

				const phraseWords = trimmedPhrase.split(/\s+/);
				const normalizedPhraseWords = phraseWords.map(normalizeWord);

				// Check if the clicked range overlaps with any instance of this phrase
				for (let i = 0; i <= splitWords.length - phraseWords.length; i++) {
					let matches = true;
					for (let j = 0; j < phraseWords.length; j++) {
						if (normalizeWord(splitWords[i + j]) !== normalizedPhraseWords[j]) {
							matches = false;
							break;
						}
					}

					if (matches) {
						const phraseStart = i;
						const phraseEnd = i + phraseWords.length - 1;

						// Check if clicked range overlaps with this phrase instance
						if (
							(start >= phraseStart && start <= phraseEnd) ||
							(end >= phraseStart && end <= phraseEnd) ||
							(start <= phraseStart && end >= phraseEnd)
						) {
							if (!phrasesToRemove.includes(phrase)) {
								phrasesToRemove.push(phrase);
							}
							break;
						}
					}
				}
			});

			// Remove the overlapping phrases
			selected = selected.filter((item) => !phrasesToRemove.includes(item));
		}
	}

	function addRangeToSelected() {
		if (selectStart !== null && selectEnd !== null) {
			const [start, end] = [selectStart, selectEnd].sort((a, b) => a - b);

			// Get the exact phrase from the selection
			const wordsInRange = splitWords.slice(start, end + 1);
			const phrase = wordsInRange.join(' ');

			// Add this phrase to selected
			if (!selected.includes(phrase)) {
				selected = [...selected, phrase];
			}
		}
	}
</script>

<ScrollArea class="h-full max-h-200 rounded border px-6 py-4">
	{#each splitWords as word, idx (`${idx}-${word}`)}
		{@render selectableWord(word, idx)}
	{/each}
</ScrollArea>

{#snippet selectableWord(word: string, idx: number)}
	<button
		onmouseenter={() => {
			if (!enabled) return;
			currentHovered = idx;
		}}
		onmousedown={() => {
			if (!enabled) return;

			selectStart = idx;
		}}
		onmouseup={() => {
			if (!enabled) return;
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
		class="selectable-word
		{hoveredRange && hoveredRange[0] <= idx && hoveredRange[1] >= idx ? 'hovered' : ''}

		{isInSelectedRanges(idx, idx) ? 'selected' : ''}"
	>
		{word}
	</button>
{/snippet}

<style lang="scss">
	.selectable-word {
		border: none;
		background: none;
		font-size: 1.2rem;
		transition: background 0.2s ease;
		cursor: pointer;
		user-select: none;
		padding: 0.1rem 0.15rem;
	}

	.selectable-word.hovered {
		background: $selection-hovered;
	}

	.selected {
		background: $selection;
	}
</style>
