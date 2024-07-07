// src/stores/auth.js
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Create a writable store to manage the authentication state
// The boolean value indicates whether the user is authenticated or not
function createAuthStore() {
    const { subscribe, set } = writable(false);

    return {
        subscribe,
        login: (token) => {
            // Save the token in the local storage after logging in
            if (browser) {
                localStorage.setItem('token', token);
                set(true);
            }
        },
        logout: () => {
            // Remove the token from the local storage after logging out
            if (browser) {
                localStorage.removeItem('token');
                set(false);
            }
        },
        check: () => {
            // Check if the user is authenticated by checking the token in the local storage
            if (browser) {
                const token = localStorage.getItem('token');
                set(!!token);
            }
        },
        getToken: () => {
            // Get the token from the local storage
            if (browser) {
                return localStorage.getItem('token');
            }
            return null;
        },
        getUsername: () => {
            // Get the username from the token
            if (browser) {
                return localStorage.getItem('username');
            }
            return null;
        },
        getUuid: () => {
            // Get the UUID from the token
            if (browser) {
                return localStorage.getItem('uuid');
            }
            return null;
        },
        getEmail: () => {
            // Get the email from the token
            if (browser) {
                return localStorage.getItem('email');
            }
            return null;
        },
        setEmail: (email) => {
            // Set the email in the local storage
            if (browser) {
                localStorage.setItem('email', email);
            }
        },
    };
}

export const auth = createAuthStore();