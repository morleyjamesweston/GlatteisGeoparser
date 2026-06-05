<script lang="ts">
	import { Field, Control, Label, FieldErrors, Description } from 'formsnap';
	import { superForm, defaults } from 'sveltekit-superforms';
	import { loginSchema } from './schema';
	import { valibotClient, valibot } from 'sveltekit-superforms/adapters';

	const superform = superForm(defaults(valibot(loginSchema)), {
		SPA: true,
		validators: valibotClient(loginSchema),
		onUpdate({ form }) {
			if (form.valid) {
				const endpoint = 'http://127.0.0.1:5000/auth/login';
				fetch(endpoint, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(form.data)
				});
				// TODO: Call an external API with form.data, await the result and update form
			}
		}
	});

	const { form, enhance } = superform;
</script>

<form method="POST" use:enhance>
	<Field form={superform} name="name">
		<Control>
			{#snippet children({ props })}
				<Label>Username</Label>
				<input {...props} bind:value={$form.name} />
			{/snippet}
		</Control>
		<Description>Be sure to use your real name.</Description>
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
	<button type="submit"> Submit</button>
</form>
