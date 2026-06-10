<script lang="ts">
	import { Field, Control, FieldErrors, Description } from 'formsnap';
	import { superForm, defaults } from 'sveltekit-superforms';
	import { loginSchema } from './schema';
	import { valibotClient, valibot } from 'sveltekit-superforms/adapters';
	import { buildApiUrl } from '$lib/api';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button';
	import Input from '$lib/components/ui/input/input.svelte';
	import Label from '$lib/components/ui/label/label.svelte';

	let errorMessage = $state('');
	let isLoading = $state(false);

	const superform = superForm(defaults(valibot(loginSchema)), {
		SPA: true,
		validators: valibotClient(loginSchema),
		onUpdate({ form }) {
			console.log('Form updated:', form);
			if (form.valid) {
				isLoading = true;
				errorMessage = '';

				console.log('Form data:', form.data);
				fetch(buildApiUrl('/auth/login'), {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(form.data),
					credentials: 'include'
				})
					.then((response) => {
						console.log('res');
						if (response.ok) {
							console.log('res1');
							return response.json().then(() => {
								// Redirect to dashboard on successful login
								window.location.href = '/dashboard';
							});
						} else {
							return response.json().then((data) => {
								errorMessage = data.error || 'Login failed';
							});
						}
					})
					.catch((error) => {
						errorMessage = 'An error occurred: ' + error.message;
					})
					.finally(() => {
						isLoading = false;
					});
			}
		}
	});

	const { form, enhance } = superform;
</script>

<div class="flex h-full w-full grow items-center justify-center">
	<Card.Root class="w-100">
		<Card.Header>
			<Card.Title>Log in</Card.Title>
			<Card.Description>Log in to your account to start geocoding.</Card.Description>
			<Card.Action><Button variant="secondary" href="/auth/register">Register</Button></Card.Action>
		</Card.Header>
		<Card.Content>
			<form method="POST" use:enhance class="flex flex-col gap-2">
				{#if errorMessage}
					<div class="error-message">{errorMessage}</div>
				{/if}

				<Field form={superform} name="username">
					<Control>
						{#snippet children({ props })}
							<Label>Username</Label>
							<Input {...props} bind:value={$form.username} />
						{/snippet}
					</Control>
					<Description>Enter your email address.</Description>
					<FieldErrors />
				</Field>
				<Field form={superform} name="password">
					<Control>
						{#snippet children({ props })}
							<Label>Password</Label>
							<Input {...props} type="password" bind:value={$form.password} />
						{/snippet}
					</Control>
					<FieldErrors />
				</Field>
				<Button type="submit" disabled={isLoading}>{isLoading ? 'Logging in...' : 'Login'}</Button>
			</form>
		</Card.Content>
	</Card.Root>
</div>
