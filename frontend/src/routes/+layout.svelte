<!-- frontend/src/routes/+layout.svelte -->
<script>
    import Header from './header/+page.svelte';
    import { auth } from '../stores/auth';
    import { onMount } from 'svelte';
    import "../app.css";

    onMount(() => {
        auth.check();
    });
</script>

<main>
    <Header />      <!-- Header will be always visible -->
    <slot />        <!-- Slot for the nested routes -->
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }
</style>