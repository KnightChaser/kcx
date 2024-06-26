<!-- register.svelte (Applying user registration) -->

<script>
    import { push } from "svelte-spa-router";
    import Swal from "sweetalert2";
    import axios from "axios";

    let username = "";
    let email = "";
    let password = "";
    let confirmPassword = "";
    let acceptTerms = false;
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

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
            if (error.response.status === 409) {
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
            push("/login");
        });
    };

    // Accordion toggle
    let isAccordionOpen = false;
    function toggleAccordion() {
        isAccordionOpen = !isAccordionOpen;
    }
</script>

<main class="container mx-auto px-4 mt-8" id="registration_form">
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
        <div class="mb-4">
            <label
                for="password"
                class="block text-sm font-medium text-gray-700">Password</label
            >
            <input
                type="password"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                id="password"
                bind:value={password}
                required
            />
        </div>
        <div class="mb-4">
            <label
                for="confirmPassword"
                class="block text-sm font-medium text-gray-700"
                >Confirm Password</label
            >
            <input
                type="password"
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                id="confirmPassword"
                bind:value={confirmPassword}
                required
            />
        </div>
        <div class="my-4">
            <button
                type="button"
                class="text-left w-full py-2 px-4 bg-gray-100 text-gray-800 font-medium rounded-md"
                on:click={toggleAccordion}
            >
                You agree to the terms and conditions by clicking the "Register" button. (Click to expand)
            </button>
            {#if isAccordionOpen}
                <div class="border p-4 mt-2 rounded-md">
                    By clicking the "Register" button, you agree to this condition.<br />
                    <strong>First</strong>, any abusing or inappropriate behavior is strictly prohibited.<br />
                    <strong>Second</strong>, you must not share your account information with others.<br />
                    <strong>Third</strong>, you have not to leak any security vulnerabilities to the public (If you find any, please report it to the administrator immediately.)
                </div>
            {/if}
        </div>
        <!-- register button -->
        <button
            type="submit"
            class="w-full py-2 px-4 bg-indigo-600 text-white font-medium rounded-md"
        >Register</button>
    </form>
</main>

<style>
    * {
        max-width: 600px;
        margin: auto;
    }

    #registration_form {
        font-family: "SF Pro Display", "Arial", sans-serif;
    }
</style>
