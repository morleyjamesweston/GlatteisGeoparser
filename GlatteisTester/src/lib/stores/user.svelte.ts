import { apiGet } from '$lib/api';

export class UserData {
	loggedIn = $state(false);
	username = $state(null);
	isAdmin = $state(false);
	isAuthenticated = $state(false);

	async loadUserData() {
		try {
			const user = await apiGet('/api/user');
			console.log('User data:', user);
			this.loggedIn = user.loggedIn;
			this.username = user.username;
			this.isAdmin = user.isAdmin;
			this.isAuthenticated = user.isAuthenticated;
		} catch (error) {
			console.error('Failed to load user data:', error);
			// User will remain in default unauthenticated state
		}
	}
}

export const userData = new UserData();
