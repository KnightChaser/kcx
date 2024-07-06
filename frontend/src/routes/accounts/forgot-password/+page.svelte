<!-- frontend/src/routes/accounts/forgot-password/+Page.svelte -->
<script>
    import { onMount } from 'svelte';
    import Swal from 'sweetalert2';
    import axios from 'axios';
    import { browser } from '$app/environment';
    
    let email = '';
    let verificationCode = '';
    let newPassword = '';
    let verificationSent = false;
    let verificationSuccess = false;
    let message = '';
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    async function sendVerificationEmail() {
        try {
            const response = await axios.post(`${BACKEND_API_URL}/auth/send-verification-email`, {
                email
            });
            message = response.data.message;
            if (response.status === 200) {
                verificationSent = true;
                Swal.fire({
                    title: 'Success',
                    text: `Verification email sent to ${email}`,
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
            }
        } catch (error) {
            message = error.response?.data?.detail || 'Failed to send verification email.';
        }
    }

    async function verifyEmail() {
        try {
            const response = await axios.post(`${BACKEND_API_URL}/auth/verify-email`, {
                email,
                code: verificationCode
            });
            message = response.data.message;
            if (response.status === 200) {
                verificationSuccess = true;
                Swal.fire({
                    title: 'Success',
                    text: 'Email verified successfully.',
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
            }
        } catch (error) {
            message = error.response?.data?.detail || 'Invalid verification code.';
        }
    }

    async function resetPassword() {
        try {
            const response = await axios.post(`${BACKEND_API_URL}/auth/password-recovery`, {
                email,
                new_password: newPassword
            });
            message = response.data.message;
            if (response.status === 200) {
                Swal.fire({
                    title: 'Success',
                    text: 'Password reset successfully.',
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    // Redirect to login page
                    if (browser) {
                        location.href = '/accounts/login';
                    }
                });
            }
        } catch (error) {
            message = error.response?.data?.detail || 'Failed to reset password.';
        }
    }
</script>

<main class="min-h-screen flex items-center justify-center p-6 bg-gray-100" id="forgot_password_form">
    <div class="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-3xl font-bold mb-4">Password Recovery</h1>
        <p class="mb-4">Oh, what a lost investor. Enter your email address to receive a verification code. Well, if you didn't receive the email, please check your spam folder.</p>
        {#if !verificationSent}
            <form on:submit|preventDefault={sendVerificationEmail}>
                <div class="mb-4">
                    <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                    <input type="email" bind:value={email} 
                        class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                        id="email" required>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Send Verification Email</button>
            </form>
        {/if}

        {#if verificationSent && !verificationSuccess}
            <form on:submit|preventDefault={verifyEmail}>
                <div class="mb-4">
                    <label for="verificationCode" class="block text-sm font-medium text-gray-700">Verification Code</label>
                    <input type="text" bind:value={verificationCode} 
                        class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                        id="verificationCode" required>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Verify Email</button>
            </form>
        {/if}

        {#if verificationSuccess}
            <form on:submit|preventDefault={resetPassword}>
                <div class="mb-4">
                    <label for="newPassword" class="block text-sm font-medium text-gray-700">New Password</label>
                    <input type="password" bind:value={newPassword} 
                        class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-shadow"
                        id="newPassword" required>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Reset Password</button>
            </form>
        {/if}

        {#if message}
            <p class="mt-4 text-red-600">{message}</p>
        {/if}
    </div>
</main>

<style>
    #forgot_password_form {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
