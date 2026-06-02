<script lang="ts">
	import { ScrollArea, type WithoutChild } from 'bits-ui';

	type Props = WithoutChild<ScrollArea.RootProps> & {
		orientation: 'vertical' | 'horizontal' | 'both';
	};

	let { ref = $bindable(null), orientation = 'vertical', children, ...restProps }: Props = $props();
</script>

{#snippet Scrollbar({ orientation }: { orientation: 'vertical' | 'horizontal' })}
	<ScrollArea.Scrollbar class="scroll-area-scrollbar" {orientation}>
		<ScrollArea.Thumb class="scroll-area-thumb" />
	</ScrollArea.Scrollbar>
{/snippet}

<ScrollArea.Root class="scrollbar-root" bind:ref {...restProps}>
	<ScrollArea.Viewport class="scroll-area-viewport">
		{@render children?.()}
	</ScrollArea.Viewport>
	{#if orientation === 'vertical' || orientation === 'both'}
		{@render Scrollbar({ orientation: 'vertical' })}
	{/if}
	{#if orientation === 'horizontal' || orientation === 'both'}
		{@render Scrollbar({ orientation: 'horizontal' })}
	{/if}
	<ScrollArea.Corner />
</ScrollArea.Root>

<style lang="scss">
	:global(.scrollbar-root) {
		position: relative;
		overflow: hidden;
	}

	:global(.scrollbar-root) {
		position: relative;
		overflow: hidden;
	}

	:global(.scroll-area-scrollbar[data-orientation='vertical']) {
		position: absolute;
		right: 0;
		top: 0;
		bottom: 0;
		width: 10px;
		padding: 2px;
		transition: width 0.2s ease;
	}

	:global(.scroll-area-scrollbar[data-orientation='vertical']:hover) {
		width: 12px;
	}

	:global(.scroll-area-scrollbar[data-orientation='horizontal']) {
		position: absolute;
		left: 0;
		right: 0;
		bottom: 0;
		height: 10px;
		padding: 2px;
		transition: height 0.2s ease;
	}

	:global(.scroll-area-scrollbar[data-orientation='horizontal']:hover) {
		height: 12px;
	}

	:global(.scroll-area-thumb) {
		background-color: #aaa;
		border-radius: 4px;
		flex-grow: 1;
		transition: background-color 0.2s ease;
	}

	:global(.scroll-area-thumb:hover) {
		background-color: #999;
	}

	:global(.scroll-area-viewport) {
		height: 100%;
		overflow: auto;
		margin-left: 0.5rem;
		margin-right: 1rem;
	}
</style>
