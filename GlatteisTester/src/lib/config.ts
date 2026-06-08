/**
 * API configuration
 *
 * In development: Set VITE_API_BASE_URL=http://localhost:5000 before running npm run dev
 * In production: Leave empty to use relative URLs
 */

// Check if we're in the browser
export const isBrowser = typeof window !== 'undefined';

// Get the base URL from window location or use relative paths
export function getApiBaseUrl(): string {
	if (!isBrowser) {
		return '';
	}

	// In development, the Vite dev server is on port 5173
	// but Flask is on port 5000, so we need to detect dev mode
	// If running on localhost and the port is 5173, use Flask on 5000
	if (window.location.hostname === 'localhost' && window.location.port === '5173') {
		return 'http://localhost:5000';
	}

	// In production (or when served from Flask), use relative URLs
	return '';
}

export const API_BASE_URL = isBrowser ? getApiBaseUrl() : '';
