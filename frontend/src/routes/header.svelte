<!-- The common header bar that will be added to service-wide  -->

<script>
    import { auth } from '../stores/auth.js';
    import { onMount, onDestroy } from 'svelte';
    import { push } from "svelte-spa-router";
    import NavbarTotalAssetTable from '../components/navbarTotalAssetTable.svelte';

    // Function to move to another page
    function moveToAnotherPage(path) {
        push(path);
    }

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

    window.addEventListener('storage', handleStorageEvent);

    onDestroy(() => {
        window.removeEventListener('storage', handleStorageEvent);
    });
</script>

<nav class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 shadow-lg py-4" id="navbar">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center">
            <a class="text-white text-3xl font-semibold no-underline"
               href="#/"
               on:click|preventDefault={() => moveToAnotherPage('/')}
               tabindex="0">KCX</a>

            <!-- Right-aligned navigation links -->
            <div class="flex items-center space-x-4">
                <a class="text-white hover:text-gray-200 no-underline link-flex" href="/" on:click|preventDefault={() => moveToAnotherPage('/')} tabindex="0">
                    Home
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house-fill" viewBox="0 0 16 16">
                        <path d="M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L8 2.207l6.646 6.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293z"/>
                        <path d="m8 3.293 6 6V13.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5V9.293z"/>
                    </svg>
                </a>
                {#if $auth}
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/logout" on:click|preventDefault={() => moveToAnotherPage('/logout')} tabindex="0">
                        Logout
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-door-open-fill" viewBox="0 0 16 16">
                            <path d="M1.5 15a.5.5 0 0 0 0 1h13a.5.5 0 0 0 0-1H13V2.5A1.5 1.5 0 0 0 11.5 1H11V.5a.5.5 0 0 0-.57-.495l-7 1A.5.5 0 0 0 3 1.5V15zM11 2h.5a.5.5 0 0 1 .5.5V15h-1zm-2.5 8c-.276 0-.5-.448-.5-1s.224-1 .5-1 .5.448.5 1-.224 1-.5 1"/>
                        </svg>
                    </a>
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/user/main" on:click|preventDefault={() => moveToAnotherPage('/user/main')} tabindex="0">
                        My page
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
                            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                        </svg>
                    </a>
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/exchange/main" on:click|preventDefault={() => moveToAnotherPage('/exchange/main')} tabindex="0">
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
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/login" on:click|preventDefault={() => moveToAnotherPage('/login')} tabindex="0">
                        Login
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-door-open-fill" viewBox="0 0 16 16">
                            <path d="M1.5 15a.5.5 0 0 0 0 1h13a.5.5 0 0 0 0-1H13V2.5A1.5 1.5 0 0 0 11.5 1H11V.5a.5.5 0 0 0-.57-.495l-7 1A.5.5 0 0 0 3 1.5V15zM11 2h.5a.5.5 0 0 1 .5.5V15h-1zm-2.5 8c-.276 0-.5-.448-.5-1s.224-1 .5-1 .5.448.5 1-.224 1-.5 1"/>
                        </svg>
                    </a>
                    <a class="text-white hover:text-gray-200 no-underline link-flex" href="/register" on:click|preventDefault={() => moveToAnotherPage('/register')} tabindex="0">
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
        src: url("../src/assets/SF-Pro-Display-Medium.otf") format("opentype");
    }

    #navbar {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
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
