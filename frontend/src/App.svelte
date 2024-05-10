<script>
    import Router from 'svelte-spa-router';
    import Header from '../routes/header.svelte';
    import 'bootstrap/dist/css/bootstrap.min.css'
    import 'bootstrap/dist/js/bootstrap.min.js'
</script>

<main>
    <!-- Header component included to appear on all pages -->
    <Header />
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }
</style>
