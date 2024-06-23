<!-- frontend/src/routes/welcome/totalTransactionAmountPanel.svelte -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import axios from 'axios';
    import { writable } from 'svelte/store';

    // Create a writable store to hold the transaction amount
    let totalTransactionAmount = writable(0);

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

    // Fetch the total transaction amount every 1 second
    onMount(() => {
        // Immediately fetch data once
        fetchTotalTransactionAmount();

        fetchInterval = setInterval(() => {
            fetchTotalTransactionAmount();
        }, 1000);
    });

    onDestroy(() => {
        clearInterval(fetchInterval);
    });
</script>

<!-- Display the total transaction amount with styling -->
<div id="totalTransactionAmountPanel" class="bg-white shadow-lg rounded-lg px-4 py-6 m-2 w-full text-center bg-opacity-80">
    <p class="text-xl font-semibold text-gray-700">Total transactions so far</p>
    <p class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-800 to-purple-600 mt-2">
        ≈ <span>{Math.round($totalTransactionAmount).toLocaleString()} KRW</span>
    </p>
</div>

<style>
    .bg-white {
        background: linear-gradient(145deg, #f8f8f8, #ffffff);
    }
    .shadow-lg {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    #totalTransactionAmountPanel {
        width: 500px;
    }
</style>
