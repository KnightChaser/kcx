<!-- frontend/src/routes/welcome/totalTransactionAmountPanel.svelte -->

<script>
	import TotalTransactionAmountPanel from './totalTransactionAmountPanel.svelte';
    import { onMount, onDestroy } from 'svelte';
    import axios from 'axios';
    import { writable } from 'svelte/store';

    let totalTransactionAmount = writable(0);
    let totalTransactionCount = writable(0);

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    let fetchInterval;

    // Function to fetch total transaction amount
    async function fetchTotalTransactionAmount() {
        try {
            const response = await axios.get(`${BACKEND_API_URL}/statistics/total-transaction-amount`);
            // Access the KRW value from the response data
            totalTransactionAmount.set(response.data.KRW);
        } catch (error) {
            console.error(error);
        }
    }

    // Function to get the total transaction count
    async function fetchTotalTransactionCount() {
        try {
            const response = await axios.get(`${BACKEND_API_URL}/statistics/total-transaction-count`);
            // Access the count value from the response data
            totalTransactionCount.set(response.data.count);
        } catch (error) {
            console.error(error);
        }
    }

    // Fetch the total transaction amount every 1 second
    onMount(() => {
        // Immediately fetch data once
        fetchTotalTransactionAmount();

        fetchInterval = setInterval(() => {
            fetchTotalTransactionAmount();
            fetchTotalTransactionCount();
        }, 1000);
    });

    onDestroy(() => {
        clearInterval(fetchInterval);
    });
</script>

<!-- Display the total transaction amount with styling -->
<div id="totalTransactionAmountPanel" class="bg-white shadow-lg rounded-lg px-6 py-8 m-4 w-full text-center">
    <p class="text-2xl font-semibold text-gray-700">Members have traded</p>
    <p class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-800 to-purple-600 mt-4">
        <span>{Math.round($totalTransactionAmount).toLocaleString()} KRW</span>
    </p>
    <p class="text-lg text-gray-500 mt-2">for <strong>{($totalTransactionCount).toLocaleString()}</strong> transactions so far</p>
</div>

<style>
    #totalTransactionAmountPanel {
        font-family: 'SF Mono', 'Fira Code', 'Fira Mono', 'Roboto Mono', monospace;
        width: 600px;
    }
    .bg-white {
        background: white;
    }
    .shadow-lg {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
</style>
