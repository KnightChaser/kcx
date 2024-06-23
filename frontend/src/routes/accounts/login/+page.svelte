<!-- frontend/src/routes/accounts/login/+page.svelte -->

<script>
    import { onMount } from 'svelte';
    import { auth } from '../../../stores/auth';
    import Swal from 'sweetalert2';
    import axios from 'axios';
    import { EyeOutline, EyeSlashOutline } from 'flowbite-svelte-icons';
    import { browser } from '$app/environment';
    
    let username = '';
    let password = '';
    let errorMessage = '';
    let showPassword = false;
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    const toggleShowPassword = () => {
        showPassword = !showPassword;
    };

    async function login() {
        try {
            // Call the backend API to login the user
            const response = await axios.post(`${BACKEND_API_URL}/account/login`, {
                username,
                password
            });

            const user = response.data;
            if (response.status === 200) {
                Swal.fire({
                    title: 'Success',
                    text: `Welcome back, ${username}!`,
                    icon: 'success',
                    confirmButtonText: 'OK',
                    allowOutsideClick: false
                }).then((result) => {
                    // Save the JWT token and other details to the local storage
                    auth.login(user.access_token);
                    if (browser) {
                        localStorage.setItem('username', username);
                        localStorage.setItem('email', user.email);
                        localStorage.setItem('uuid', user.uuid);
                    }

                    // redirect to the home page
                    if (result.isConfirmed) {
                        // Move to the exchange page
                        if (browser) {
                            location.href = '/';
                        }
                        console.error('Failed to redirect to the home page');
                    }
                });
            }
        } catch (error) {
            if (error.response && (error.response.status === 401 || error.response.status === 404)) {
                errorMessage = 'Invalid username or password';
            } else {
                errorMessage = 'Failed to login: ' + error.message;
            }
        }
    }
</script>

<main class="min-h-screen flex items-center justify-center p-6 bg-gray-100" id="login_form">
    <div class="w-full max-w-xs bg-white rounded-lg shadow-lg p-8">
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
            <div class="mb-6 relative">
                <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                <div class="relative flex items-center">
                    {#if showPassword}
                        <input type="text" bind:value={password} 
                            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                            id="password" required>
                    {:else}
                        <input type="password" bind:value={password} 
                            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                            id="password" required>
                    {/if}
                    <button type="button" class="absolute right-3 transform -translate-y-1/2" on:click={toggleShowPassword} style="top: 60%">
                        {#if showPassword}
                            <EyeOutline class="w-5 h-5 text-gray-500" />
                        {:else}
                            <EyeSlashOutline class="w-5 h-5 text-gray-500" />
                        {/if}
                    </button>
                </div>
            </div>
            <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Login</button>
        </form>
    </div>
</main>

<style>
    #login_form {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
