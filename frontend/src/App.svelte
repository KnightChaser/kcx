<script>
    import Header from './routes/header.svelte';
    import Welcome from './routes/welcome.svelte';
    import NotFound from './routes/error/notfound.svelte';
    import Router from 'svelte-spa-router';
    import wrap from 'svelte-spa-router/wrap';
    import { auth } from '../src/stores/auth.js';
    import { onMount } from 'svelte';
    
    import "bootstrap/dist/css/bootstrap.min.css"
    import "bootstrap/dist/js/bootstrap.js"
    
    onMount(() => {
        // Check authentication status when the component mounts
        auth.check();
    });

    // Setup routes with immediate and lazy-loaded components
    const routes = {
        '/': Welcome,  // Load immediately
        '/login': wrap({
            asyncComponent: () => import('./routes/login.svelte'),
            conditions: [() => !$auth]  // Only show if not logged in
        }),
        '/logout': wrap({
            asyncComponent: () => import('./routes/logout.svelte'),
            conditions: [() => $auth]  // Only show if logged in
        }),
        '/register': wrap({
            asyncComponent: () => import('./routes/register.svelte'),
            conditions: [() => !$auth]  // Only show if not logged in
        }),
        '/leaderboard': wrap({
            asyncComponent: () => import('./routes/leaderboard.svelte'),
            // No conditions, always show
        }),
        '/exchange/main': wrap({
            asyncComponent: () => import('./routes/exchange/main.svelte'),
            conditions: [() => $auth]  // Ensure authenticated
        }),
        '/user/main': wrap({
            asyncComponent: () => import('./routes/user/main.svelte'),
            conditions: [() => $auth]  // Ensure authenticated
        }),
        '/user/depositWithdrawHistory': wrap({
            asyncComponent: () => import('./routes/user/depositeWithdrawlHistory.svelte'),
            conditions: [() => $auth]  // Ensure authenticated
        }),
        '/user/cryptoTradeHistory': wrap({
            asyncComponent: () => import('./routes/user/cryptoTradeHistory.svelte'),
            conditions: [() => $auth]  // Ensure authenticated
        }),
        '/user/assetTracking': wrap({
            asyncComponent: () => import('./routes/user/assetTracking.svelte'),
            conditions: [() => $auth]  // Ensure authenticated
        }),
        '*': NotFound  // Load immediately
    };
</script>

<main>
    <Header />  <!-- Always visible and loaded immediately -->
    <body>
        <Router {routes} />
    </body>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }
</style>
