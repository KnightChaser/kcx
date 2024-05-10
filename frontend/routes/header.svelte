<!-- The common header bar that will be added to service-wide  -->
<script>
    import { auth } from '../src/stores/auth.js'
    import { onMount, onDestroy } from 'svelte';
    import { push } from "svelte-spa-router";

    // Function to move to another page
    function moveToAnotherPage(path) {
        push(path);
    }

    onMount(() => {
        // Check authentication status when the component mounts
        auth.check();
    });

    // Optionally, respond to storage events that might be triggered from other tabs
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

<nav class="navbar navbar-expand-lg bg-dark border-bottom border-body">
    <div class="container-fluid">
        <a class="navbar-brand"
           href="#/"
           on:click|preventDefault={() => moveToAnotherPage('/')}
           tabindex="0">KCX</a>

        <!-- Right-aligned navigation links -->
        <div class="d-flex justify-content-end" style="width: 100%;">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="/" on:click|preventDefault={() => moveToAnotherPage('/')}
                       tabindex="0">Home</a>
                </li>

                {#if $auth}
                    <li class="nav-item">
                        <a class="nav-link" href="/logout" on:click|preventDefault={() => moveToAnotherPage('/logout')}
                           tabindex="0">Logout</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a class="nav-link" href="/login" on:click|preventDefault={() => moveToAnotherPage('/login')}
                           tabindex="0">Login</a>
                    </li>
                {/if}
                
                <li class="nav-item">
                    <a class="nav-link" href="/register" on:click|preventDefault={() => moveToAnotherPage('/register')}
                       tabindex="0">Register</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<style>
    @font-face {
        font-family: "SF Pro Display";
        src: url("../src/assets/SF-Pro-Display-Medium.otf") format("opentype");
    }

    nav {
        font-family: "SF Pro Display";
        background-color: slateblue !important;
    }

    a {
        color: white;
    }
</style>
