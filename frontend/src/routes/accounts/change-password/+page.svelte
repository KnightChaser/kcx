<!-- frontend/src/routes/accounts/change-password/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import Swal from 'sweetalert2';
    import axios from 'axios';
    import { browser } from '$app/environment';
    import { auth } from '../../../stores/auth';

    let currentPassword = '';
    let newPassword = '';
    let confirmPassword = '';
    let passwordsMatch = true;
    let message = '';
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    function checkPasswords() {
        passwordsMatch = newPassword === confirmPassword;
    }

    async function changePassword() {
        if (!passwordsMatch) {
            Swal.fire({
                title: 'Error',
                text: 'Passwords do not match.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return;
        }

        try {
            const token = auth.getToken();
            const response = await axios.post(`${BACKEND_API_URL}/account/change-password`, {
                old_password: currentPassword,
                new_password: newPassword
            }, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            message = response.data.message;
            if (response.status === 200) {
                Swal.fire({
                    title: 'Success',
                    text: 'Password changed successfully. Please log in again.',
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    if (browser) {
                        auth.purge();       // Clear the auth store, now the user is logged out
                        location.href = '/accounts/login';
                    }
                });
            }
        } catch (error) {
            message = error.response?.data?.detail || 'Failed to change password.';
        }
    }
</script>

<main class="min-h-screen flex items-center justify-center p-6 bg-gray-100" id="change_password_form">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-3xl font-bold mb-4">Change Password</h1>
        <p class="mb-4">Enter your current password and a new password.</p>
        <form on:submit|preventDefault={changePassword}>
            <div class="mb-4">
                <label for="currentPassword" class="block text-sm font-medium text-gray-700">Current Password</label>
                <input type="password" bind:value={currentPassword} 
                    class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                    id="currentPassword" required>
            </div>
            <div class="mb-4">
                <label for="newPassword" class="block text-sm font-medium text-gray-700">New Password</label>
                <input type="password" bind:value={newPassword} on:input={checkPasswords}
                    class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                    id="newPassword" required>
            </div>
            <div class="mb-4">
                <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirm New Password</label>
                <input type="password" bind:value={confirmPassword} on:input={checkPasswords}
                    class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                    id="confirmPassword" required>
                {#if newPassword && confirmPassword}
                    {#if passwordsMatch}
                        <p class="mt-2 text-green-600">Passwords match!</p>
                    {:else}
                        <p class="mt-2 text-red-600">Passwords do not match.</p>
                    {/if}
                {/if}
            </div>
            <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" disabled={!passwordsMatch}>Change Password</button>
        </form>

        {#if message}
            <p class="mt-4 text-red-600">{message}</p>
        {/if}
    </div>
</main>

<style>
    #change_password_form {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
