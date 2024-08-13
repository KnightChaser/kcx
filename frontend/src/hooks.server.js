// frontend/src/hooks.server.js
import { browser } from '$app/environment';

export async function handle({ event, resolve }) {
    // Check authentication for protected routes
    const protectedRoutes = ['/dashboards', '/accounts/logout', '/accounts/user', '/exchange'];
    const isProtected = protectedRoutes.some(route => event.url.pathname.startsWith(route));

    // Check if the authentication cookie is present
    const isAuthenticated = event.request.headers.get('cookie')?.includes('access_token');

    if (isProtected && !isAuthenticated) {
        if (browser) {
            window.location.href = '/accounts/login';
        }
    }

    return resolve(event);
}