<script lang="ts" module>
	import type { HTMLButtonAttributes } from 'svelte/elements';
	export type ButtonProps = HTMLButtonAttributes & {
		ref?: HTMLElement | null;
		variant?: 'primary' | 'secondary';
	};
</script>

<script lang="ts">
	let {
		ref = $bindable(null),
		variant = 'primary',
		class: className,
		type = 'button',
		children,
		...restProps
	}: ButtonProps = $props();
</script>

<button class={[className, variant]} {...restProps} {type} bind:this={ref}>
	{@render children?.()}
</button>

<style lang="scss">
	button {
		padding: 0.5rem 0;
		font-family: $font-ui;
		width: 100%;
		font-size: 1.2rem;
		/* background-color: var(--background); */
		/* color: var(--foreground); */
		/* border: 1px solid var(--border); */
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		/* font-weight: 200; */
	}
</style>
