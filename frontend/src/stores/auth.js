// src/stores/auth.js
import { writable } from 'svelte/store';

// Create a writable store to manage the authentication state
// The boolean value indicates whether the user is authenticated or not
function createAuthStore() {
    const { subscribe, set } = writable(false);

    return {
        subscribe,
        login: (token) => {
            // Save the token in the local storage after logging in
            localStorage.setItem('token', token);
            set(true);
        },
        logout: () => {
            // Remove the token from the local storage after logging out
            localStorage.removeItem('token');
            set(false);
        },
        check: () => {
            // Check if the user is authenticated by checking the token in the local storage
            const token = localStorage.getItem('token');
            set(!!token);
        }
    };
}

export const auth = createAuthStore();