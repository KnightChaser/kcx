<!-- user/main.svelte (user personal home page)  -->

<script>
    import Router from 'svelte-spa-router';
    import Header from '../header.svelte';
    import 'bootstrap/dist/css/bootstrap.min.css';
    import 'bootstrap/dist/js/bootstrap.min.js';
</script>

<main>
    <h1>KCX</h1>
    <p>Welcome back!</p>
    <p>Your username: {localStorage.getItem('username')}</p>
    <p>Your email: {localStorage.getItem('email')}</p>
    <p>Coming soon...</p>
</main>