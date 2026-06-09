<script lang="ts">
	import CheckIcon from '@lucide/svelte/icons/check';
	import ChevronsUpDownIcon from '@lucide/svelte/icons/chevrons-up-down';
	import { onMount, tick } from 'svelte';
	import * as Command from '$lib/components/ui/command/index.js';
	import * as Popover from '$lib/components/ui/popover/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { cn } from '$lib/utils.js';
	import { apiGet } from '$lib/api';
	let { value = $bindable('') }: { value?: string } = $props();

	let texts: { value: string; label: string }[] = $state([]);

	async function getArticleIds() {
		try {
			const data = await apiGet('/api/get_all_content_ids');
			console.log('All content IDs:', data);
			texts = data.map((id: number) => ({ value: id.toString(), label: id.toString() }));
		} catch (err) {
			console.error('Error fetching all coded data:', err);
		}
	}

	onMount(() => {
		getArticleIds();
	});

	let open = $state(false);
	// let value = $state('');
	let triggerRef = $state<HTMLButtonElement>(null!);

	const selectedValue = $derived(texts.find((f) => f.value === value)?.label);

	// We want to refocus the trigger button when the user selects
	// an item from the list so users can continue navigating the
	// rest of the form with the keyboard.
	function closeAndFocusTrigger() {
		open = false;
		tick().then(() => {
			triggerRef.focus();
		});
	}
</script>

<Popover.Root bind:open>
	<Popover.Trigger bind:ref={triggerRef}>
		{#snippet child({ props })}
			<Button
				{...props}
				variant="outline"
				class="w-50 justify-between"
				role="combobox"
				aria-expanded={open}
			>
				{selectedValue || 'Select content...'}
				<ChevronsUpDownIcon class="opacity-50" />
			</Button>
		{/snippet}
	</Popover.Trigger>
	<Popover.Content class="w-50 p-0">
		<Command.Root>
			<Command.Input placeholder="Search framework..." />
			<Command.List>
				<Command.Empty>No content ID found.</Command.Empty>
				<Command.Group value="frameworks">
					{#each texts as text (text.value)}
						<Command.Item
							value={text.value}
							onSelect={() => {
								value = text.value;
								closeAndFocusTrigger();
							}}
						>
							<CheckIcon class={cn(value !== text.value && 'text-transparent')} />
							{text.label}
						</Command.Item>
					{/each}
				</Command.Group>
			</Command.List>
		</Command.Root>
	</Popover.Content>
</Popover.Root>
