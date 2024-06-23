<!-- frontend/src/routes/exchange/headerPanel.svelte -->

<script>
    import { formatCurrency } from "../../utils/formatCurrency";
    import { selectedMarketCode } from './stores/selectedMarketStore.js';
    import { derived } from 'svelte/store';
    import { balances } from '../../stores/usesrAssets';
    import { Table, TableHead, TableHeadCell, TableBody, TableBodyRow, TableBodyCell } from 'flowbite-svelte';

    const selectedMarketCodeUnit = derived(selectedMarketCode, ($selectedMarketCode) => $selectedMarketCode.split('-')[1].toUpperCase());

    export let selectedMarket;
</script>

{#if selectedMarket}
    <div class="flex items-center justify-between border-b border-gray-400 p-2">
        <div class="flex items-center space-x-4 pl-2">
            <img src="/src/assets/currency_logo/{selectedMarket.market.replace('KRW-', '').toLowerCase()}_logo.png" alt="Market Icon" class="h-10 w-10">
            <div>
                <h2 class="text-3xl font-semibold text-gray-800">{$selectedMarketCodeUnit}</h2>
                <h1 class="text-lg font-medium text-gray-500">{$balances[$selectedMarketCodeUnit]?.fullname}</h1>
            </div>
        </div>
        <div class="overflow-x-auto">
            <Table class="min-w-full divide-y divide-gray-200 max-w-full">
                <TableHead class="bg-gray-50">
                    <TableHeadCell class="px-4 py-2 text-sm font-medium text-gray-500 uppercase tracking-wider text-center">Current Price</TableHeadCell>
                    <TableHeadCell class="px-4 py-2 text-sm font-medium text-gray-500 uppercase tracking-wider text-center">24h Change</TableHeadCell>
                    <TableHeadCell class="px-4 py-2 text-sm font-medium text-gray-500 uppercase tracking-wider text-center">24h Low/High</TableHeadCell>
                    <TableHeadCell class="px-4 py-2 text-sm font-medium text-gray-500 uppercase tracking-wider text-center">24h Volume</TableHeadCell>
                </TableHead>
                <TableBody class="bg-white divide-y divide-gray-200">
                    <TableBodyRow>
                        <TableBodyCell class="px-4 py-2 whitespace-nowrap text-center text-4xl font-semibold text-gray-800">{formatCurrency(selectedMarket.trade_price)}</TableBodyCell>
                        <TableBodyCell class="px-4 py-2 whitespace-nowrap text-center {selectedMarket.change === 'FALL' ? 'text-red-500' : 'text-green-500'} text-lg font-semibold">
                            {selectedMarket.change === 'FALL' ? '' : '+'}{formatCurrency(selectedMarket.signed_change_price)} <br>
                            ({(selectedMarket.signed_change_rate * 100).toFixed(2)}%)
                        </TableBodyCell>
                        <TableBodyCell class="px-4 py-2 whitespace-nowrap text-center text-lg font-semibold text-gray-800">{formatCurrency(selectedMarket.low_price)}<br>{formatCurrency(selectedMarket.high_price)}</TableBodyCell>
                        <TableBodyCell class="px-4 py-2 whitespace-nowrap text-center text-m font-semibold text-gray-800">{formatCurrency(selectedMarket.acc_trade_price_24h)}</TableBodyCell>
                    </TableBodyRow>
                </TableBody>
            </Table>
        </div>
    </div>
{:else}
    <p class="text-center text-gray-500">Loading...</p>
{/if}
