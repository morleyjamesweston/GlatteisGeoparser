<script lang="ts">
	let { selected, resolvedFeatures } = $props();
</script>

<div class="container">
	{#each selected as item, i (item)}
		{@const resolved = !!resolvedFeatures[item]}
		<div class="item {resolved ? 'resolved' : ''}">
			{item}
		</div>
	{/each}
</div>

<style lang="scss">
	.container {
		display: flex;
		gap: $spacing-sm;
	}
	.item {
		padding: $spacing-sm;
		border: 1px solid gray;
		border-radius: 4px;
	}

	.item.resolved {
		background-color: lightgreen;
		border-color: green;
	}
</style>
