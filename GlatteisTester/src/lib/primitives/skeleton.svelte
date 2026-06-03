<script lang="ts">
	let { height, text } = $props();
</script>

<div class="skeleton" style="height: {height}rem;">
	{text}
</div>

<style lang="scss">
	.skeleton {
		background-color: #eee;
		border-radius: 4px;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-style: italic;
	}
</style>
