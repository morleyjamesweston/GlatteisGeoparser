import * as v from 'valibot';

export const loginSchema = v.object({
	username: v.string('Name is required'),
	password: v.pipe(
		v.string('Password is required'),
		v.minLength(6, 'Password must be at least 6 characters')
	)
});
