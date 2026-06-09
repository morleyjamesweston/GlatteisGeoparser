<script lang="ts">
	let { height, text } = $props();
</script>

<div
	class="flex w-full items-center justify-center bg-muted text-muted-foreground"
	style="height: {height}rem;"
>
	{text}
</div>
