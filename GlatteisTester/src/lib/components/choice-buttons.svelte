<script lang="ts">
	let { selected = $bindable() }: { selected: string[] } = $props();
</script>

<!-- onclick={() => {
				selected = selected.filter((_, i) => i !== idx);
			}} -->
<div class="container">
	{#each selected as item, idx (`${item}-${idx}`)}
		<button>
			{item}
		</button>
	{:else}
		<div class="empty-content">Please all locations in the text.</div>
	{/each}
</div>

<style lang="scss">
	.empty-content {
		width: 100%;
		height: 2rem;
		display: flex;
		align-items: center;
		justify-content: center;
		font-style: italic;
	}
	.container {
		display: flex;
		min-height: 2rem;
		flex-wrap: wrap;
		gap: $spacing-sm;
	}
	button {
		border: none;
		background-color: #eee;
		padding: 0.5rem 1rem;
	}
</style>
