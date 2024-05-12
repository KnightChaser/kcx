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
                <a class="text-white hover:text-gray-200 no-underline" href="/" on:click|preventDefault={() => moveToAnotherPage('/')} tabindex="0">Home</a>
                
                {#if $auth}
                    <a class="text-white hover:text-gray-200 no-underline" href="/logout" on:click|preventDefault={() => moveToAnotherPage('/logout')} tabindex="0">Logout</a>
                    <a class="text-white hover:text-gray-200 no-underline" href="/user/main" on:click|preventDefault={() => moveToAnotherPage('/user/main')} tabindex="0">My page</a>
                    <a class="text-white hover:text-gray-200 no-underline" href="/exchange/main" on:click|preventDefault={() => moveToAnotherPage('/exchange/main')} tabindex="0">Exchange</a>
                    <NavbarTotalAssetTable />
                {:else}
                    <a class="text-white hover:text-gray-200 no-underline" href="/login" on:click|preventDefault={() => moveToAnotherPage('/login')} tabindex="0">Login</a>
                    <a class="text-white hover:text-gray-200 no-underline" href="/register" on:click|preventDefault={() => moveToAnotherPage('/register')} tabindex="0">Register</a>
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
</style>
