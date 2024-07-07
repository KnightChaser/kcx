<!-- frontend/src/routes/accounts/change-email/+Page.svelte -->
<script>
    import { onMount } from 'svelte';
    import Swal from 'sweetalert2';
    import axios from 'axios';
    import { browser } from '$app/environment';
    import { auth } from '../../../stores/auth';

    let currentEmail = auth.getEmail();
    let newEmail = '';
    let verificationCode = '';
    let verificationSent = false;
    let verificationSuccess = false;
    let message = '';
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    async function sendVerificationEmail() {
        try {
            const response = await axios.post(`${BACKEND_API_URL}/auth/send-verification-email`, {
                email: newEmail
            });
            message = response.data.message;
            if (response.status === 200) {
                verificationSent = true;
                Swal.fire({
                    title: 'Success',
                    text: `Verification email sent to ${newEmail}`,
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
            }
        } catch (error) {
            message = error.response?.data?.detail || 'Failed to send verification email.';
        }
    }

    async function verifyEmailChange() {
        try {
            const response = await axios.post(`${BACKEND_API_URL}/auth/verify-email`, {
                email: newEmail,
                code: verificationCode
            });
            message = response.data.message;
            if (response.status === 200) {
                verificationSuccess = true;
                changeEmail();
            }
        } catch (error) {
            message = error.response?.data?.detail || 'Invalid verification code. Try again.';
            verificationSent = false; // Reset to allow the user to request verification again
            verificationSuccess = false;
        }
    }

    async function changeEmail() {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`${BACKEND_API_URL}/account/change-email`, {
                old_email: currentEmail,
                new_email: newEmail
            }, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            message = response.data.message;
            if (response.status === 200) {
                Swal.fire({
                    title: 'Success',
                    text: 'Email address changed successfully.',
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    // Update the auth store with the new email and redirect to settings page
                    auth.setEmail(newEmail);
                    if (browser) {
                        location.href = '/accounts/user/settings';
                    }
                });
            }
        } catch (error) {
            message = error.response?.data?.detail || 'Failed to change email address.';
        }
    }
</script>

<main class="min-h-screen flex items-center justify-center p-6 bg-gray-100" id="change_email_form">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-3xl font-bold mb-4">Change Email Address</h1>
        <p class="mb-4">Enter your new email address to receive a verification code.</p>
        {#if !verificationSent}
            <form on:submit|preventDefault={sendVerificationEmail}>
                <div class="mb-4">
                    <label for="currentEmail" class="block text-sm font-medium text-gray-700">Current Email</label>
                    <input type="email" value={currentEmail} disabled
                        class="mt-1 block w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md shadow-sm focus:outline-none transition-shadow"
                        id="currentEmail">
                </div>
                <div class="mb-4">
                    <label for="newEmail" class="block text-sm font-medium text-gray-700">New Email</label>
                    <input type="email" bind:value={newEmail} 
                        class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                        id="newEmail" required>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Send Verification Email</button>
            </form>
        {/if}

        {#if verificationSent && !verificationSuccess}
            <form on:submit|preventDefault={verifyEmailChange}>
                <div class="mb-4">
                    <label for="verificationCode" class="block text-sm font-medium text-gray-700">Verification Code</label>
                    <input type="text" bind:value={verificationCode} 
                        class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                        id="verificationCode" required>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Verify Email Change</button>
            </form>
        {/if}

        {#if message}
            <p class="mt-4 text-red-600">{message}</p>
        {/if}
    </div>
</main>

<style>
    #change_email_form {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
