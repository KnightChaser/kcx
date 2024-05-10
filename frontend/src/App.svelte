<script>
    import Router from 'svelte-spa-router';
    import Header from '../routes/header.svelte';
    import Login from '../routes/login.svelte';
    // import Register from '../routes/register.svelte';
    import 'bootstrap/dist/css/bootstrap.min.css';
    import 'bootstrap/dist/js/bootstrap.min.js';

    const routes = {
        '/login': Login,
        // '/register': Register
    };
</script>

<main>
    <Header />
    <Router {routes} />
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }
</style>