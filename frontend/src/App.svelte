<script>
    import Router, { location } from 'svelte-spa-router';
    import Header from '../routes/header.svelte';
    import Welcome from '../routes/welcome.svelte';
    import Login from '../routes/login.svelte';
    import Logout from '../routes/logout.svelte';
    // import Register from '../routes/register.svelte';
    import 'bootstrap/dist/css/bootstrap.min.css';
    import 'bootstrap/dist/js/bootstrap.min.js';

    import { auth } from '../src/stores/auth.js'

    const routes = {
        '/': Welcome,  // Ensure there's a route for '/'
        '/login': Login,
        '/logout': Logout
        // '/register': Register
    };
</script>

<main>
    <Header />
    <Router {routes} />
    <!-- Reactively show Welcome component -->
    <body>
    {#if !$auth && $location === '/'}
        <Welcome />
    {/if}
    </body>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }
</style>