<script lang="ts">
	let {
		features,
		value = $bindable(''),
		hovered = $bindable('')
	}: {
		features: Array<{
			id: string;
			properties: { original_names: string; gazetteer_name: string };
		}>;
		value: string;
		hovered: string | null;
	} = $props();
	import CheckCircleIcon from '@lucide/svelte/icons/circle-check-big';
	import CircleIcon from '@lucide/svelte/icons/circle';
	import { RadioGroup } from 'bits-ui';
</script>

<RadioGroup.Root class="radio-group" bind:value>
	{#each features as feature (feature.id)}
		<RadioGroup.Item
			id={feature.id}
			value={feature.id}
			class="radio-item"
			onmouseenter={() => (hovered = feature.id)}
			onmouseleave={() => (hovered = null)}
		>
			{#snippet children({ checked })}
				{#if checked}
					<CheckCircleIcon size={24} color="green" />
				{:else}
					<CircleIcon size={24} color="gray" />
				{/if}
				<b>{feature.properties.original_names}</b>
				<i>Gazetteer: {feature.properties.gazetteer_name}</i>
			{/snippet}
		</RadioGroup.Item>
	{/each}

	<RadioGroup.Item
		id="other"
		value="other"
		class="radio-item"
		onmouseenter={() => (hovered = 'other')}
		onmouseleave={() => (hovered = null)}
	>
		{#snippet children({ checked })}
			{#if checked}
				<CheckCircleIcon size={24} color="green" />
			{:else}
				<CircleIcon size={24} color="gray" />
			{/if}
			<b>Other location not listed</b>
		{/snippet}
	</RadioGroup.Item>
</RadioGroup.Root>

<style lang="scss">
	:global(.radio-group) {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	:global(.radio-item) {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		background: none;
		padding: 0.5rem;
		border: 1px solid transparent;
		cursor: pointer;
	}
</style>
