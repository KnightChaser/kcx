<!-- routes/user/depositWithdrawHistory.svelte -->
<script>
    import { onMount } from 'svelte';
    import { push } from "svelte-spa-router";
    import Swal from 'sweetalert2';
    
    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
    
    let history = [];
    let error = null;

    onMount(async () => {
        try {
            const response = await fetch(`${BACKEND_API_URL}/account/deposit_withdraw/history/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!response.ok) {
                Swal.fire({
                    icon: 'error',
                    title: 'Failed to fetch history',
                    text: 'Failed to fetch history',
                });
                throw new Error('Failed to fetch history');
            }
            history = await response.json();
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

<div class="w-full max-w-4xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6">
    <div class="flex justify-between items-center" id="history_table_header">
        <h2 class="text-2xl font-semibold text-gray-900">Deposit/Withdraw History</h2>
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
            <table class="min-w-full bg-white border border-gray-200">
                <caption class="caption-top">
                    Only up to 20 most recent records are shown.
                </caption>
                <thead class="bg-gray-50">
                    <tr>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Currency</th>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Amount</th>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Transaction Type</th>
                        <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Date</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    {#each history as record}
                        <tr class="hover:bg-gray-100">
                            <td class="py-2 px-6 whitespace-nowrap text-center">{record.currency}</td>
                            <td class="py-2 px-6 whitespace-nowrap text-right">{Number(record.amount).toLocaleString()}</td>
                            <td class="py-2 px-6 whitespace-nowrap text-center">{record.transaction_type}</td>
                            <td class="py-2 px-6 whitespace-nowrap text-center">{new Date(record.created_at).toLocaleString()}</td>
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
    }
</style>