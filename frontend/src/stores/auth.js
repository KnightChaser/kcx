// src/stores/auth.js
import { writable } from 'svelte/store';

// Create a writable store to manage the authentication state
// The boolean value indicates whether the user is authenticated or not
function createAuthStore() {
    const { subscribe, set } = writable(false);

    return {
        subscribe,
        login: (token) => {
            localStorage.setItem('token', token);
            set(true);
        },
        logout: () => {
            localStorage.removeItem('token');
            set(false);
        },
        check: () => {
            const token = localStorage.getItem('token');
            set(!!token);
        }
    };
}

export const auth = createAuthStore();