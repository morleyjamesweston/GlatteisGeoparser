import { userData } from '$lib/stores/user.svelte';

export const prerender = true;

// Load user data when the app first loads
export async function load() {
	userData.loadUserData();
}
