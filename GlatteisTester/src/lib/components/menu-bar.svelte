<script lang="ts">
	import ModeSwitcher from './mode-switcher.svelte';
	import { userData } from '$lib/stores/user.svelte';
	import Button from './ui/button/button.svelte';
	import Separator from './ui/separator/separator.svelte';
	import LogInIcon from '@lucide/svelte/icons/log-in';
</script>

<header class="flex w-full items-center justify-between px-4 py-2">
	<div class="font-heading text-2xl">Glatteis Geotester</div>

	<div class="flex items-center gap-1">
		{#if userData.isAuthenticated}
			<div class="text-sm">Hi, {userData.username}!</div>
			<Button variant="outline" size="sm" href="/auth/logout">Log out</Button>
			<!-- {#if userData.isAdmin}
			<div>You have admin privileges</div>
		{/if} -->
		{:else}
			<Button variant="outline" href="/auth/login">
				<LogInIcon class="h-4 w-4" />
				Log in
			</Button>
		{/if}
		<ModeSwitcher />
	</div>
</header>
<Separator />
