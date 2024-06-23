// src/hooks.server.js

export async function handle({ event, resolve }) {
    // Check authentication for protected routes
    const protectedRoutes = ['/dashboards', '/user', '/exchange'];
    const isProtected = protectedRoutes.some(route => event.url.pathname.startsWith(route));

    // Check if the authentication cookie is present
    const isAuthenticated = event.request.headers.get('cookie')?.includes('access_token');

    if (isProtected && !isAuthenticated) {
        return Response.redirect('/accounts/login');
    }

    return resolve(event);
}