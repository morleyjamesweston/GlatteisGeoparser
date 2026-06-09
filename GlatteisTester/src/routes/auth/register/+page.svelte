<script lang="ts">
	import { Field, Control, FieldErrors, Description } from 'formsnap';
	import { superForm, defaults } from 'sveltekit-superforms';
	import { registerSchema } from './schema';
	import { valibotClient, valibot } from 'sveltekit-superforms/adapters';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button';
	import Input from '$lib/components/ui/input/input.svelte';
	import Label from '$lib/components/ui/label/label.svelte';

	let errorMessage = $state('');
	let successMessage = $state('');
	let isLoading = $state(false);

	const superform = superForm(defaults(valibot(registerSchema)), {
		SPA: true,
		validators: valibotClient(registerSchema),
		onUpdate({ form }) {
			console.log('Form updated:', form);
			if (form.valid) {
				isLoading = true;
				errorMessage = '';
				successMessage = '';

				const endpoint = 'http://127.0.0.1:5000/auth/register';
				console.log('Submitting to endpoint:', endpoint);
				console.log('Form data:', form.data);
				fetch(endpoint, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(form.data),
					credentials: 'include'
				})
					.then((response) => {
						if (response.ok) {
							return response.json().then(() => {
								successMessage = 'Registration successful! Redirecting to login...';
								// Redirect to login after 2 seconds
								setTimeout(() => {
									window.location.href = '/auth/login';
								}, 2000);
							});
						} else {
							return response.json().then((data) => {
								errorMessage = data.error || 'Registration failed';
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

<div class="flex h-full w-full items-center justify-center">
	<Card.Root class="w-100">
		<Card.Header>
			<Card.Title>Register</Card.Title>
			<Card.Description>Register for an account to start geocoding.</Card.Description>
			<Card.Action><Button variant="secondary" href="/auth/login">Login</Button></Card.Action>
		</Card.Header>
		<Card.Content>
			<form method="POST" use:enhance class="flex flex-col gap-2">
				{#if errorMessage}
					<div class="error-message">{errorMessage}</div>
				{/if}

				{#if successMessage}
					<div class="success-message">{successMessage}</div>
				{/if}

				<Field form={superform} name="username">
					<Control>
						{#snippet children({ props })}
							<Label>Username</Label>
							<Input {...props} bind:value={$form.username} />
						{/snippet}
					</Control>
					<Description>Choose a unique username.</Description>
					<FieldErrors />
				</Field>

				<Field form={superform} name="password">
					<Control>
						{#snippet children({ props })}
							<Label>Password</Label>
							<Input {...props} type="password" bind:value={$form.password} />
						{/snippet}
					</Control>
					<Description>Password must be at least 6 characters.</Description>
					<FieldErrors />
				</Field>

				<Field form={superform} name="confirmPassword">
					<Control>
						{#snippet children({ props })}
							<Label>Confirm Password</Label>
							<Input {...props} type="password" bind:value={$form.confirmPassword} />
						{/snippet}
					</Control>
					<Description>Passwords must match.</Description>
					<FieldErrors />
				</Field>

				<Button type="submit" disabled={isLoading}>
					{isLoading ? 'Registering...' : 'Register'}
				</Button>
			</form>
		</Card.Content>
	</Card.Root>
</div>

<form method="POST" use:enhance></form>

<style>
	.error-message {
		color: #dc3545;
		background-color: #f8d7da;
		padding: 0.75rem;
		border-radius: 4px;
		border: 1px solid #f5c6cb;
	}

	.success-message {
		color: #155724;
		background-color: #d4edda;
		padding: 0.75rem;
		border-radius: 4px;
		border: 1px solid #c3e6cb;
	}
</style>
