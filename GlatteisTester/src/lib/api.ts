import { API_BASE_URL } from './config';

/**
 * Build the full API URL based on environment
 * - Development (port 5173): uses localhost:5000 (Flask)
 * - Production (served from Flask): uses relative URLs
 */
export function buildApiUrl(path: string): string {
	return `${API_BASE_URL}${path}`;
}

/**
 * Common fetch options for API requests
 */
export const fetchOptions = {
	credentials: 'include' as const,
	headers: {
		'Content-Type': 'application/json'
	}
};

/**
 * Make a GET request to the API
 */
export async function apiGet(path: string) {
	const url = buildApiUrl(path);
	const response = await fetch(url, {
		...fetchOptions,
		method: 'GET'
	});
	return response.json();
}

/**
 * Make a POST request to the API
 */
export async function apiPost(path: string, data: unknown) {
	const url = buildApiUrl(path);
	const response = await fetch(url, {
		...fetchOptions,
		method: 'POST',
		body: JSON.stringify(data)
	});
	return response.json();
}
