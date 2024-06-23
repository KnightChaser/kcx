<!-- frontend/src/routes/headder/+page.svelte -->
<!-- The common header bar that will be added to service-wide  -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import { redirect } from '@sveltejs/kit';
    import { browser } from '$app/environment';
    import { auth } from "../../stores/auth.js";
    import NavbarTotalAssetTable from "./navbarTotalAssetTable.svelte";
    import { HomeOutline } from 'flowbite-svelte-icons';

    onMount(() => {
        // Check authentication status when the component mounts
        auth.check();
    });

    // Handle the storage event
    function handleStorageEvent(event) {
        if (event.key === 'token') {
            auth.check();
        }
    }

    if (browser) {
        window.addEventListener('storage', handleStorageEvent);
    }

    onDestroy(() => {
        if (browser) {
            window.removeEventListener('storage', handleStorageEvent);
        }
    });
</script>

<nav class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 shadow-lg py-4" id="navbar">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center">
            <a class="text-white text-3xl font-semibold no-underline"
               href="#/"
               on:click|preventDefault={() => redirect('/')}
               tabindex="0">KCX</a>

            <!-- Right-aligned navigation links -->
            <div class="flex items-center space-x-4">
                <!-- Github page -->
                <a class="text-white hover:text-gray-200 no-underline link-flex" href="https://github.com/KnightChaser/kcx" tabindex="0" target="_blank">
                    GitHub
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" fill="#ffffff"/>
                    </svg>
                </a>
                <!-- Home -->
                <a class="text-white hover:text-gray-200 no-underline link-flex" href="/" tabindex="0">
                    Home
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house-fill" viewBox="0 0 16 16">
                        <path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L8 2.207l6.646 6.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293z"/>
                        <path d="m8 3.293 6 6V13.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5V9.293z"/>
                    </svg>
                </a>
                <!-- Leaderboard -->
                <a class="text-white hover:text-gray-200 no-underline link-flex" href="/leaderboard" tabindex="0">
                    Leaderboard
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard2-data-fill" viewBox="0 0 16 16">
                        <path d="M10 .5a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5.5.5 0 0 1-.5.5.5.5 0 0 0-.5.5V2a.5.5 0 0 0 .5.5h5A.5.5 0 0 0 11 2v-.5a.5.5 0 0 0-.5-.5.5.5 0 0 1-.5-.5"/>
                        <path d="M4.085 1H3.5A1.5 1.5 0 0 0 2 2.5v12A1.5 1.5 0 0 0 3.5 16h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 12.5 1h-.585q.084.236.085.5V2a1.5 1.5 0 0 1-1.5 1.5h-5A1.5 1.5 0 0 1 4 2v-.5q.001-.264.085-.5M10 7a1 1 0 1 1 2 0v5a1 1 0 1 1-2 0zm-6 4a1 1 0 1 1 2 0v1a1 1 0 1 1-2 0zm4-3a1 1 0 0 1 1 1v3a1 1 0 1 1-2 0V9a1 1 0 0 1 1-1"/>
                    </svg>
                </a>
                <!-- Service pages only for authenticated subjects -->
                {#if $auth}
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/accounts/logout" tabindex="0">
                        Logout
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-door-open-fill" viewBox="0 0 16 16">
                            <path d="M1.5 15a.5.5 0 0 0 0 1h13a.5.5 0 0 0 0-1H13V2.5A1.5 1.5 0 0 0 11.5 1H11V.5a.5.5 0 0 0-.57-.495l-7 1A.5.5 0 0 0 3 1.5V15zM11 2h.5a.5.5 0 0 1 .5.5V15h-1zm-2.5 8c-.276 0-.5-.448-.5-1s.224-1 .5-1 .5.448.5 1-.224 1-.5 1"/>
                        </svg>
                    </a>
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/accounts/user" tabindex="0">
                        My page
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                        </svg>
                    </a>
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/exchange" tabindex="0">
                        Exchange
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-wallet-fill" viewBox="0 0 16 16">
                            <path d="M1.5 2A1.5 1.5 0 0 0 0 3.5v2h6a.5.5 0 0 1 .5.5c0 .253.08.644.306.958.207.288.557.542 1.194.542s.987-.254 1.194-.542C9.42 6.644 9.5 6.253 9.5 6a.5.5 0 0 1 .5-.5h6v-2A1.5 1.5 0 0 0 14.5 2z"/>
                            <path d="M16 6.5h-5.551a2.7 2.7 0 0 1-.443 1.042C9.613 8.088 8.963 8.5 8 8.5s-1.613-.412-2.006-.958A2.7 2.7 0 0 1 5.551 6.5H0v6A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5z"/>
                        </svg>
                    </a>
                    <div>
                        <NavbarTotalAssetTable />
                    </div>
                {:else}
                    <!-- Service pages only for unauthenticated subjects -->
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/accounts/login" tabindex="0">
                        Login
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-door-open-fill" viewBox="0 0 16 16">
                            <path d="M1.5 15a.5.5 0 0 0 0 1h13a.5.5 0 0 0 0-1H13V2.5A1.5 1.5 0 0 0 11.5 1H11V.5a.5.5 0 0 0-.57-.495l-7 1A.5.5 0 0 0 3 1.5V15zM11 2h.5a.5.5 0 0 1 .5.5V15h-1zm-2.5 8c-.276 0-.5-.448-.5-1s.224-1 .5-1 .5.448.5 1-.224 1-.5 1"/>
                        </svg>
                    </a>
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/accounts/register" tabindex="0">
                        Register
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill-add" viewBox="0 0 16 16">
                            <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m.5-5v1h1a.5.5 0 0 1 0 1h-1v1a.5.5 0 0 1-1 0v-1h-1a.5.5 0 0 1 0-1h1v-1a.5.5 0 0 1 1 0m-2-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                            <path d="M2 13c0 1 1 1 1 1h5.256A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1 1.544-3.393Q8.844 9.002 8 9c-5 0-6 3-6 4"/>
                        </svg>
                    </a>
                {/if}
            </div>
        </div>
    </div>
</nav>

<style>
    @font-face {
        font-family: "SF Pro Display";
        src: url("../../assets/SF-Pro-Display-Medium.otf");
    }

    nav {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
        width: 100vw;
    }

    /* Remove underline from links and apply any additional link styling */
    .no-underline {
        text-decoration: none;
    }

    .link-flex {
        display: flex;
        align-items: center; 
        justify-content: center; 
        flex-direction: column;
        gap: 5px; 
    }

    .link-flex svg {
        width: 20px;
        height: 20px;
    }
</style>