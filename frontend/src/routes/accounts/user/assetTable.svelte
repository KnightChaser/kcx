<!-- frontend/src/routes/accounts/user/assetTable.svelte  -->
<!-- Getting the asset table per asset -->

<script>
    import { balances } from "../../../stores/usesrAssets.js";
    import { formatAmount } from "../../../utils/formatAmount.js";
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Button, Checkbox, Input, Popover, Label } from 'flowbite-svelte';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { SearchOutline } from 'flowbite-svelte-icons';

    let searchTerm = '';
    let showOnlyOwnedAssets = false;
    const sortKey = writable('');
    const sortDirection = writable(1);
    const sortedBalances = writable([]);

    onMount(() => {
        sortedBalances.set(Object.entries($balances));
    });

    $: {
        const key = $sortKey;
        const direction = $sortDirection;
        const term = searchTerm.toLowerCase();
        const filtered = Object.entries($balances).filter(([currency, { fullname, amount }]) => {
            const matchesSearch = currency.toLowerCase().includes(term) || fullname.toLowerCase().includes(term);
            const matchesOwnership = showOnlyOwnedAssets ? amount > 0 : true;
            return matchesSearch && matchesOwnership;
        });

        const sorted = filtered.sort((a, b) => {
            const aVal = key ? a[1][key] : a[0];
            const bVal = key ? b[1][key] : b[0];
            if (aVal < bVal) {
                return -direction;
            } else if (aVal > bVal) {
                return direction;
            }
            return 0;
        });
        sortedBalances.set(sorted);
    }

    function sortTable(key) {
        // If the same key is clicked, reverse the sort direction
        if ($sortKey === key) {
            sortDirection.update((val) => -val);
        } else {
            sortKey.set(key);
            sortDirection.set(1);
        }
    }

    function getSortIndicator(key) {
        if ($sortKey === key) {
            return $sortDirection === 1 ? '▲' : '▼';
        }
        return '';
    }
</script>

<div class="overflow-x-auto w-full pt-3 px-1">
    <div class="flex justify-between items-center mb-4">
        <Checkbox aria-describedby="helper-checkbox-text" bind:checked={showOnlyOwnedAssets}>
            <pre> Show only owned assets</pre>
        </Checkbox>
        <Input id="search" placeholder="Search assets by full name or symbol" size="lg" bind:value={searchTerm} class="w-1/3" />
    </div>

    <Table class="min-w-full text-lg">
        <TableHead class="bg-gray-50 text-xl" id="assetTableHead">
            <TableHeadCell class="px-4 py-2 whitespace-nowrap cursor-pointer" on:click={() => sortTable('fullname')}>
                Assets {getSortIndicator('fullname')}
            </TableHeadCell>
            <TableHeadCell class="px-4 py-2 text-right whitespace-nowrap cursor-pointer" on:click={() => sortTable('currency')}>
                Symbol {getSortIndicator('currency')}
            </TableHeadCell>
            <TableHeadCell class="px-4 py-2 text-right whitespace-nowrap cursor-pointer" on:click={() => sortTable('amount')}>
                Amount {getSortIndicator('amount')}
            </TableHeadCell>
            <TableHeadCell class="px-4 py-2 text-right whitespace-nowrap cursor-pointer" on:click={() => sortTable('estimatedValue')}>
                Value {getSortIndicator('estimatedValue')}
            </TableHeadCell>
        </TableHead>
        <Popover target="#assetTableHead" class="w-full">Click the column to sort...</Popover>
        <TableBody class="bg-white divide-y divide-gray-200">
            {#each $sortedBalances as [currency, { amount, estimatedValue, fullname }]}
                <TableBodyRow class="border-t">
                    <TableBodyCell class="px-4 py-2 flex items-center whitespace-nowrap">
                        <img src="/src/assets/currency_logo/{currency.toLowerCase()}_logo.png" alt="{currency} logo" class="h-8 w-8 mr-3" />
                        <span class="truncate">{fullname}</span>
                    </TableBodyCell>
                    <TableBodyCell class="px-4 py-2 text-right whitespace-nowrap">{currency}</TableBodyCell>
                    <TableBodyCell class="px-4 py-2 text-right whitespace-nowrap">
                        {@html formatAmount(amount)}
                    </TableBodyCell>
                    <TableBodyCell class="px-4 py-2 text-right whitespace-nowrap">
                        {#if currency !== "KRW"}
                            <p class="text-blue-500">
                                ≈ <b>{Math.round(estimatedValue).toLocaleString()}</b> KRW
                            </p>
                        {/if}
                    </TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</div>
