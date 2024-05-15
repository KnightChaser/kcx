<script>
    import { push } from "svelte-spa-router";
    import { onMount } from "svelte";
    import { auth } from "../stores/auth.js";
    import Swal from "sweetalert2";
    import axios from "axios";
    
    let username = "";
    let password = "";
    let errorMessage = "";
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    async function login() {
        try {
            // Call the backend API to login the user
            const response = await axios.post(`${BACKEND_API_URL}/account/login`, {
                username,
                password
            });

            if (response.status === 401 || response.status === 404) {
                Swal.fire({
                    title: 'Who are you?',
                    text: 'Invalid username or password',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
                return;
            } else if (response.status !== 200) {
                // Untriggered error
                errorMessage = 'An error occurred while logging in.';
            }
            
            const user = response.data;
            if (response.status === 200) {
                Swal.fire({
                    title: 'Success',
                    text: `Welcome back, ${username}!`,
                    icon: 'success',
                    confirmButtonText: 'OK',
                    allowOutsideClick: false
                }).then((result) => {
                    // Save the JWT token to the local storage
                    auth.login(user.access_token);
                    localStorage.setItem('username', username);
                    localStorage.setItem('email', user.email);
                    localStorage.setItem('uuid', user.uuid);
                    
                    // redirect to the home page
                    if (result.isConfirmed) {
                        // Move to the exchange page
                        push('/exchange/main');
                    }
                });
            }
        } catch (error) {
            errorMessage = error.message;
        }
    }
</script>

<main class="min-h-screen flex items-center justify-center p-6" id="login_form">
    <div class="w-full max-w-xs">
        <h1 class="text-3xl font-bold mb-2">Login</h1>
        <h5 class="text-xl mb-4">Oh, who's there?</h5>
        {#if errorMessage}
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
                {errorMessage}
            </div>
        {/if}
        <form on:submit|preventDefault={login}>
            <div class="mb-4">
                <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                <input type="text" bind:value={username} 
                    class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                    id="username" required>
            </div>
            <div class="mb-6">
                <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                <input type="password" bind:value={password} 
                    class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                    id="password" required>
            </div>
            <button type="submit" class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Login</button>
        </form>
    </div>
</main>

<style>
    #login_form {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>