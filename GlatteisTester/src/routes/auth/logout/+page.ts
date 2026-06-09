import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { userData } from '$lib/stores/user.svelte';

export const load: PageLoad = async ({ fetch }) => {
	try {
		const response = await fetch('http://127.0.0.1:5000/auth/logout', {
			method: 'GET',
			credentials: 'include'
		});

		if (response.ok) {
			userData.loadUserData();
			redirect(302, '/auth/login');
		} else {
			console.error('Logout failed');
			redirect(302, '/auth/login');
		}
	} catch (error) {
		console.error('Logout error:', error);
		redirect(302, '/auth/login');
	}
};
