<!-- frontend/src/routes/accounts/user/depositHistory/+page.svelte  -->

<script>
    import { onMount } from 'svelte';
    import Swal from 'sweetalert2';
    import axios from 'axios';
    import { auth } from '../../../../stores/auth.js';
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Alert } from 'flowbite-svelte';
    
    const username = auth.getUsername();
    const token = auth.getToken();
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
    
    let history = [];
    let error = null;

    onMount(async () => {
        try {
            const response = await axios.get(`${BACKEND_API_URL}/account/deposit_withdraw/history/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.status !== 200) {
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
</script>

<div class="w-full max-w-4xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6 mt-6">
    <div class="flex justify-between items-center" id="history_table_header">
        <h2 class="text-2xl font-semibold text-gray-900">Deposit/Withdraw History</h2>
    </div>

    {#if error}
        <Alert color="failure" class="mb-4">
            {error}
        </Alert>
    {:else}
        <div class="overflow-x-auto" id="walletHistoryTable">
            <Table>
                <caption class="caption-top">
                    Only up to 20 most recent records are shown.
                </caption>
                <TableHead class="bg-gray-50">
                    <TableHeadCell class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Currency</TableHeadCell>
                    <TableHeadCell class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Amount</TableHeadCell>
                    <TableHeadCell class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Transaction Type</TableHeadCell>
                    <TableHeadCell class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Date</TableHeadCell>
                </TableHead>
                <TableBody class="bg-white divide-y divide-gray-200">
                    {#each history as record}
                        <TableBodyRow class="hover:bg-gray-100">
                            <TableBodyCell class="py-2 px-6 whitespace-nowrap text-center">{record.currency}</TableBodyCell>
                            <TableBodyCell class="py-2 px-6 whitespace-nowrap text-right">{Number(record.amount).toLocaleString()}</TableBodyCell>
                            <TableBodyCell class="py-2 px-6 whitespace-nowrap text-center">{record.transaction_type}</TableBodyCell>
                            <TableBodyCell class="py-2 px-6 whitespace-nowrap text-center">{new Date(record.created_at).toLocaleString()}</TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </div>
    {/if}
</div>

<style>
    #history_table_header {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
        margin-bottom: 1rem;
    }

    #walletHistoryTable {
        font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", monospace;
    }
</style>
