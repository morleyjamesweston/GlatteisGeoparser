<script lang="ts">
	import { Field, Control, Label, FieldErrors, Description } from 'formsnap';
	import { superForm, defaults } from 'sveltekit-superforms';
	import { loginSchema } from './schema';
	import { valibotClient, valibot } from 'sveltekit-superforms/adapters';

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

				const endpoint = 'http://127.0.0.1:5000/auth/login';
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

<form method="POST" use:enhance>
	{#if errorMessage}
		<div class="error-message">{errorMessage}</div>
	{/if}

	<Field form={superform} name="username">
		<Control>
			{#snippet children({ props })}
				<Label>Username</Label>
				<input {...props} bind:value={$form.username} />
			{/snippet}
		</Control>
		<Description>Enter your email address.</Description>
		<FieldErrors />
	</Field>
	<Field form={superform} name="password">
		<Control>
			{#snippet children({ props })}
				<Label>Password</Label>
				<input {...props} type="password" bind:value={$form.password} />
			{/snippet}
		</Control>
		<Description>Ensure the password is at least 6 characters.</Description>
		<FieldErrors />
	</Field>
	<button type="submit" disabled={isLoading}> {isLoading ? 'Logging in...' : 'Login'}</button>
</form>

sdfdsfdsafd
