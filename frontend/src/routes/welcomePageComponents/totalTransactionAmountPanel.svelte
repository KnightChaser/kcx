<script>
    import { onMount, onDestroy } from 'svelte';
    import axios from 'axios';
    import { writable } from 'svelte/store';
    import { CountUp } from 'countup.js';
    import { Odometer } from 'odometer_countup';

    // Create a writable store to hold the transaction amount
    let totalTransactionAmount = writable(0);

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    let totalAmountElement;
    let countUpInstance;
    let fetchInterval;

    // Function to fetch total transaction amount
    function fetchTotalTransactionAmount() {
        axios.get(`${BACKEND_API_URL}/api/statistics/total-transaction-amount`)
            .then(response => {
                // Access the KRW value from the response data
                totalTransactionAmount.set(response.data.KRW);
            })
            .catch(error => {
                console.error(error);
            });
    }

    // Fetch the total transaction amount every 1 second
    onMount(() => {
        countUpInstance = new CountUp(totalAmountElement, 0, {
            duration: 0.5,
            separator: ',',
            decimal: '.',
            startVal: 0,
            plugin: new Odometer({
                duration: 0.5,
                lastDigitDelay: 0,
            }),
        });

        countUpInstance.start();

        // Immediately fetch data once
        fetchTotalTransactionAmount();

        fetchInterval = setInterval(() => {
            fetchTotalTransactionAmount();
        }, 1000);

        // Subscribe to store changes to update countUp
        totalTransactionAmount.subscribe($totalTransactionAmount => {
            if (!isNaN($totalTransactionAmount)) {
                countUpInstance.update($totalTransactionAmount);
            }
        });
    });

    onDestroy(() => {
        clearInterval(fetchInterval);
        if (countUpInstance) {
            countUpInstance.reset();
        }
    });

    // Function to format the number with localization
    function formatCurrency(value) {
        return new Intl.NumberFormat('ko-KR', {
            style: 'currency',
            currency: 'KRW',
            minimumFractionDigits: 2
        }).format(value);
    }
</script>

<!-- Display the total transaction amount with styling -->
<div class="bg-white shadow-lg rounded-lg px-4 py-6 m-2 w-3/2 text-center bg-opacity-80">
    <p class="text-lg font-semibold text-gray-700">Total transactions so far</p>
    <p class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-800 to-purple-600 mt-2">
        ≈ <span bind:this={totalAmountElement} class="text-gray-700"></span> KRW
    </p>
</div>

<style>
    .bg-white {
        background: linear-gradient(145deg, #f8f8f8, #ffffff);
    }
    .shadow-lg {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
</style>
