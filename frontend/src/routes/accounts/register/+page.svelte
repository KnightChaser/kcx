<!-- frontend/src/routes/accounts/register/+page.svelte -->

<script>
	import { auth } from './../../../stores/auth.js';
    import { browser } from "$app/environment";
    import Swal from "sweetalert2";
    import axios from "axios";
    import { redirect } from "@sveltejs/kit";
    import { Accordion, AccordionItem, Banner } from 'flowbite-svelte';
    import { EyeOutline, EyeSlashOutline } from 'flowbite-svelte-icons';
    import { BullhornSolid } from 'flowbite-svelte-icons';

    let username = "";
    let email = "";
    let password = "";
    let confirmPassword = "";
    let showPassword = false;
    let showConfirmPassword = false;
    let usernameValid = true;
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    const toggleShowPassword = () => {
        showPassword = !showPassword;
    };

    const toggleShowConfirmPassword = () => {
        showConfirmPassword = !showConfirmPassword;
    };

    const isUsernameValid = (username) => {
        const regex = /^[a-zA-Z0-9_]+$/;
        return regex.test(username);
    };

    const submitForm = async () => {
        if (!isUsernameValid(username)) {
            usernameValid = false;
            Swal.fire({
                title: "Error",
                text: "Username can only contain alphanumeric characters and underscores.",
                icon: "error",
            });
            return;
        } else {
            usernameValid = true;
        }

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
    <!-- A temporary banner asking users to use real email addresses -->
    <Banner>
        <div class="flex items-center">
            <BullhornSolid class="w-6 h-6 text-blue-500" />
            <p class="ml-2 text-sm text-blue-500">Please <b>use a real email address</b> when registering.
            We may send important notifications to this email address, including password reset instructions.
            Using invalid emails may result in account lockout in the future and we will not be able to help you recover your account.</p>
        </div>
    </Banner>
    <br>

    <h2 class="text-3xl font-semibold mb-6 py-2 text-center">Register</h2>
    <form on:submit|preventDefault={submitForm}>
        <div class="mb-4">
            <label
                for="username"
                class="block text-sm font-medium text-gray-700">ID</label
            >
            <input
                type="text"
                class={`mt-1 block w-full px-3 py-2 border ${usernameValid ? 'border-gray-300' : 'border-red-500'} rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500`}
                id="username"
                bind:value={username}
                required
            />
            {#if !usernameValid}
                <p class="text-red-500 text-sm mt-1">Username can only contain alphanumeric characters and underscores.</p>
            {/if}
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

        <Accordion>
            <AccordionItem>
                <span slot="header">Policy of peneration(security) testing</span>
                <div class="border p-4 mt-2 rounded-md">
                    <p>By clicking the "Register" button, you agree to this condition.</p>
                    
                    <p><strong>1. Acceptance of Terms</strong><br />
                    By clicking the "Register" button and creating an account, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions.</p>

                    <p><strong>2. Not to disclose any security vulnerabilities without permission</strong><br />
                    If you discover any security vulnerabilities within the platform, you must not disclose them to the public. Instead, please report any security issues directly to the platform administrator immediately so that we can address and resolve them promptly.</p>

                    <p><strong>3. Contributions</strong><br />
                    By submitting ideas, suggestions, documents, and/or proposals ("Contributions") to the platform, you acknowledge and agree that:</p>
                    <ul>
                        <li>We are not under any obligation of confidentiality, express or implied, with respect to the Contributions.</li>
                        <li>We may have something similar to the Contributions already under consideration or in development.</li>
                        <li>We will gladly accept any Contributions that you make to improve the platform, but we are not obligated to use or incorporate your Contributions into the platform.</li>
                        <li>We can attribute your Contributions to you if you want, but you are not entitled to any compensation or reimbursement for them since it's free and open-sourced.</li>
                        <li>You grant us an irrevocable, non-exclusive, royalty-free, perpetual, worldwide license to use, modify, publish, distribute, and sublicense the Contributions.</li>
                    </ul>

                    <p><strong>4. Prohibitions</strong><br />
                    You must not misuse the platform by knowingly introducing viruses, trojans, worms, logic bombs, or other material that is malicious or technologically harmful. You must not attempt to gain unauthorized access to the platform, the server on which the platform is stored, or any server, computer, or database connected to the platform. You must not attack the platform via a denial-of-service attack or a distributed denial-of-service attack. By breaching this provision, you would commit a criminal offense under the Computer Misuse Act 1990. We will report any such breach to the relevant law enforcement authorities and we will cooperate with those authorities by disclosing your identity to them. In the event of such a breach, your right to use the platform will cease immediately.</p>

                    <p><strong>5. Ethical and education purpose of security testing on the platform</strong><br />
                    The platform is designed for educational purposes and ethical hacking practice (too). You must not use the platform for any illegal or malicious activities. You must not attempt to exploit any vulnerabilities found on the platform for personal gain or to harm others. You must not disrupt the platform's operation or interfere with other users' experience. You must use the platform responsibly and ethically.</p>
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
