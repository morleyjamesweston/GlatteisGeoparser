import * as v from 'valibot';

export const registerSchema = v.pipe(
	v.object({
		username: v.pipe(
			v.string('Username is required'),
			v.minLength(3, 'Username must be at least 3 characters'),
			v.maxLength(50, 'Username must be at most 50 characters')
		),
		password: v.pipe(
			v.string('Password is required'),
			v.minLength(6, 'Password must be at least 6 characters')
		),
		confirmPassword: v.string('Please confirm your password')
	}),
	v.forward(
		v.check(
			(input) => input.password === input.confirmPassword,
			'Passwords do not match'
		),
		['confirmPassword']
	)
);
