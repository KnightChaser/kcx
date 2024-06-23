<!-- frontend/src/routes/accounts/register/+page.svelte -->

<script>
	import { auth } from './../../../stores/auth.js';
    import { browser } from "$app/environment";
    import Swal from "sweetalert2";
    import axios from "axios";
    import { redirect } from "@sveltejs/kit";
    import { Accordion, AccordionItem } from 'flowbite-svelte';
    import { EyeOutline, EyeSlashOutline } from 'flowbite-svelte-icons';

    let username = "";
    let email = "";
    let password = "";
    let confirmPassword = "";
    let showPassword = false;
    let showConfirmPassword = false;
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    const toggleShowPassword = () => {
        showPassword = !showPassword;
    };

    const toggleShowConfirmPassword = () => {
        showConfirmPassword = !showConfirmPassword;
    };

    const submitForm = async () => {
        if (password !== confirmPassword) {
            Swal.fire({
                title: "Error",
                text: "Passwords do not match.",
                icon: "error",
            });
            return;
        }

        try {
            // Call the backend API to register the user
            const response = await axios.post(`${BACKEND_API_URL}/account/register`, {
                username,
                email,
                password,
            });
            
            // If not successful, show an error message
            if (response.status !== 200) {
                console.error("Error registering user:", response.data);
                Swal.fire({
                    title: "Error",
                    text: "An error occurred while creating the account.",
                    icon: "error",
                });
                return;
            }
        } catch (error) {
            // If the response code is 409 (Conflict), it means the username or email already exists
            if (error.response?.status === 409) {
                Swal.fire({
                    title: "Error",
                    text: "Username or email already exists.",
                    icon: "error",
                });
            } else {
                console.error("Error registering user:", error);
                Swal.fire({
                    title: "Error",
                    text: "An error occurred while creating the account.",
                    icon: "error",
                });
            }
            return;
        }

        // Account created successfully, send the user to the login page
        Swal.fire({
            title: "Success",
            text: "Account created successfully.",
            icon: "success",
        }).then(() => {
            redirect("/accounts/login");
        });
    };
</script>

<main class="container mx-auto px-4 mt-8 max-w-lg" id="registration_form">
    <h2 class="text-3xl font-semibold mb-6 py-2">Register</h2>
    <form on:submit|preventDefault={submitForm}>
        <div class="mb-4">
            <label
                for="username"
                class="block text-sm font-medium text-gray-700">ID</label
            >
            <input
                type="text"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                id="username"
                bind:value={username}
                required
            />
        </div>
        <div class="mb-4">
            <label for="email" class="block text-sm font-medium text-gray-700"
                >Email</label
            >
            <input
                type="email"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                id="email"
                bind:value={email}
                required
            />
        </div>
        <div class="mb-4 relative">
            <label
                for="password"
                class="block text-sm font-medium text-gray-700">Password</label
            >
            {#if showPassword}
                <input
                    type="text"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    id="password"
                    bind:value={password}
                    required
                />
            {:else}
                <input
                    type="password"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    id="password"
                    bind:value={password}
                    required
                />
            {/if}
            <button type="button" class="absolute right-3 top-8" on:click={toggleShowPassword}>
                {#if showPassword}
                    <EyeOutline class="w-5 h-5 text-gray-500" />
                {:else}
                    <EyeSlashOutline class="w-5 h-5 text-gray-500" />
                {/if}
            </button>
        </div>
        <div class="mb-4 relative">
            <label
                for="confirmPassword"
                class="block text-sm font-medium text-gray-700"
                >Confirm Password</label
            >
            {#if showConfirmPassword}
                <input
                    type="text"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    id="confirmPassword"
                    bind:value={confirmPassword}
                    required
                />
            {:else}
                <input
                    type="password"
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    id="confirmPassword"
                    bind:value={confirmPassword}
                    required
                />
            {/if}
            <button type="button" class="absolute right-3 top-8" on:click={toggleShowConfirmPassword}>
                {#if showConfirmPassword}
                    <EyeOutline class="w-5 h-5 text-gray-500" />
                {:else}
                    <EyeSlashOutline class="w-5 h-5 text-gray-500" />
                {/if}
            </button>
        </div>

        <Accordion>
            <AccordionItem>
                <span slot="header">Terms and Conditions</span>
                <div class="border p-4 mt-2 rounded-md">
                    <p>By clicking the "Register" button, you agree to this condition.</p>
                    <p><strong>1. Acceptance of Terms</strong><br />
                    By clicking the "Register" button and creating an account, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions.</p>
                    
                    <p><strong>2. Appropriate Use</strong><br />
                    Users must conduct themselves in a respectful and appropriate manner. Any form of abuse, harassment, or inappropriate behavior is strictly prohibited. This includes, but is not limited to, the use of offensive language, threats, or any actions that may harm or disrupt other users or the platform.</p>
                    
                    <p><strong>3. Account Security</strong><br />
                    You are responsible for maintaining the confidentiality of your account information, including your username and password. You must not share your account information with others. Any unauthorized access or use of your account must be reported to the platform administrator immediately.</p>
                    
                    <p><strong>4. Security Vulnerabilities</strong><br />
                    If you discover any security vulnerabilities within the platform, you must not disclose them to the public. Instead, please report any security issues directly to the platform administrator immediately so that we can address and resolve them promptly.</p>
                    
                    <p><strong>5. Use of the Platform</strong><br />
                    This platform is intended solely for the purpose of simulating cryptocurrency trading. It is designed for exercising, experimenting, or having fun. No real financial transactions or actual cryptocurrency trades are conducted on this platform.</p>
                    
                    <p><strong>6. Limitation of Liability</strong><br />
                    The platform is provided "as is" without any warranties of any kind, express or implied. We do not guarantee the accuracy, completeness, or reliability of the platform or any simulated trading data. Users agree to use the platform at their own risk.</p>
                    
                    <p><strong>7. Modifications to Terms</strong><br />
                    We reserve the right to modify these terms and conditions at any time. Any changes will be posted on the platform, and it is your responsibility to review these terms periodically. Your continued use of the platform following any changes constitutes your acceptance of the new terms.</p>
                    
                    <p><strong>8. Termination of Use</strong><br />
                    We reserve the right to terminate or suspend your account and access to the platform at our sole discretion, without notice, for conduct that we believe violates these terms or is otherwise harmful to other users or the platform.</p>
                    
                    <p><strong>9. Governing Law</strong><br />
                    These terms and conditions shall be governed by and construed in accordance with the laws of the jurisdiction in which the platform operates, without regard to its conflict of law principles.</p>
                    
                    <p>If you have any questions or concerns about these terms and conditions, please contact our support team.</p>
                    
                    <p>By clicking the "Register" button, you acknowledge that you have read, understood, and agree to these terms and conditions.</p>
                </div>
            </AccordionItem>
        </Accordion>
        <br>


        <!-- register button -->
        <button
            type="submit"
            class="w-full py-2 px-4 bg-indigo-600 text-white font-medium rounded-md"
        >Register</button>
    </form>
</main>

<style>
    #registration_form {
        font-family: "SF Pro Display", "Arial", sans-serif;
    }
</style>
