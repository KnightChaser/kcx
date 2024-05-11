<!-- user/main.svelte -->

<script>
    import { push } from "svelte-spa-router";
    import "bootstrap/dist/css/bootstrap.min.css";
    import "bootstrap/dist/js/bootstrap.min.js";
    import Swal from "sweetalert2";
    import { onMount } from "svelte";

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
    let balances = { KRW: 'Loading...', BTC: 'Loading...', ETH: 'Loading...', XRP: 'Loading...' };
    let username = localStorage.getItem("username"); // Reactive variable for username

    async function getBalance() {
        const response = await fetch(`${BACKEND_API_URL}/account/balance`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        if (!response.ok) {
            Swal.fire({
                title: 'Error',
                text: 'Failed to get balance information',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            push('/login'); // Redirect if user is not authenticated
            return;
        }

        const data = await response.json();
        return data; // Return the entire balance object
    }

    onMount(async () => {
        const fetchedBalances = await getBalance() || { KRW: 'Unavailable', BTC: 'Unavailable', ETH: 'Unavailable', XRP: 'Unavailable' };
        balances = {...balances, ...fetchedBalances}; // Update the balances object
    });
</script>

<main>
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <h1>Welcome, {username}</h1>
                <h2>Your account balances are:</h2>
                <ul>
                    <li>KRW: {balances.KRW.toLocaleString()}</li>
                    <li>BTC: {balances.BTC}</li>
                    <li>ETH: {balances.ETH}</li>
                    <li>XRP: {balances.XRP}</li>
                </ul>
            </div>
        </div>
    </div>
</main>
