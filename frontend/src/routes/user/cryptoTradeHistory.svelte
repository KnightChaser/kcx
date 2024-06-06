<!-- routes/user/cryptoTradeHistory.svelte  -->
<script>
    import { onMount } from 'svelte';
    import { push } from 'svelte-spa-router';
    import Swal from 'sweetalert2';
    import axios from 'axios';
    import { formatAmount } from '../../utils/formatAmount';
    import { formatCurrency } from '../../utils/formatCurrency';

    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    let history = [];
    let error = null;

    onMount(async () => {
        try {
            const response = await axios.get(`${BACKEND_API_URL}/api/account/crypto_trade/history/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.status != 200) {
                Swal.fire({
                    icon: 'error',
                    title: 'Failed to fetch history',
                    text: 'Failed to fetch history',
                });
                throw new Error('Failed to fetch history');
            }

            history = response.data;
        } catch (err) {
            // Show error message
            error = err.message;
            Swal.fire({
                icon: 'error',
                title: 'Failed to fetch history',
                text: error,
            });
        }
    });

    function moveToUserPage() {
        push("/user/main");
    }
</script>

<div class="w-full max-w-6xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6">
    <div class="flex justify-between items-center" id="history_table_header">
        <h2 class="text-2xl font-semibold text-gray-900">Crypto Trade History</h2>
        <button 
            class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
            on:click={moveToUserPage}>
            Back to User Page
        </button>
    </div>

    {#if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white border border-gray-200 table-auto">
                <caption class="caption-top">
                    Only up to 50 most recent records are shown.
                </caption>
                <thead class="bg-gray-50">
                    <tr>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Timestamp</th>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Currency</th>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Type</th>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Amount</th>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Price</th>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Total price</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    {#each history as record}
                        <tr class="hover:bg-gray-100">
                            <td class="py-2 px-6 whitespace-nowrap text-center">{new Date(record.created_at).toLocaleString()}</td>
                            <td class="py-2 px-6 whitespace-nowrap text-center">
                                <div class="flex items-center">
                                    <img src={`/src/assets/currency_logo/${String(record.currency).toLowerCase()}_logo.png`} alt={record.currency} width="25px">
                                    <span class="ml-2">{record.currency}</span>
                                </div>
                            </td>
                            <td class="py-2 px-6 whitespace-nowrap text-center">{record.transaction_type.toUpperCase()}</td>
                            <td class="py-2 px-6 whitespace-nowrap text-right">{@html formatAmount(record.amount)}</td>
                            <td class="py-2 px-6 whitespace-nowrap text-right">{@html formatAmount(record.price)}</td>
                            <td class="py-2 px-6 whitespace-nowrap text-right">{formatCurrency(Number(record.amount) * record.price)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>

<style>
    #history_table_header {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
        margin-bottom: 1rem;
    }

    table {
        font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", monospace;
        width: 100%;
    }

    th, td {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }

    td {
        white-space: nowrap;
    }

    .table-auto th, .table-auto td {
        min-width: 150px;
    }
</style>
