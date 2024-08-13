<!-- frontend/src/routes/exchange/leftPanel.svelte -->

<script>
    import { createEventDispatcher } from 'svelte';
    import { formatCurrency } from '../../utils/formatCurrency';
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Input, Button } from 'flowbite-svelte';
    
    export let marketData;
    export let setSelectedMarket;
    export let selectedMarket;

    let filteredMarketData = marketData;
    let searchQuery = '';

    const dispatch = createEventDispatcher();

    // Format the change rate
    function formatChangeRate(changeRate) {
        return (changeRate * 100).toFixed(2);
    }

    // Handle the market selection
    function handleMarketSelect(market) {
        setSelectedMarket(market);
    }

    // Sort the market data
    export function handleSort(key) {
        dispatch('sort', { key });
    }

    // Filter the market data based on the search query
    function filterMarketData() {
        filteredMarketData = marketData.filter(market =>
            market.market.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }

    // Update the filtered market data whenever the market data or search query changes
    $: filteredMarketData = marketData.filter(market =>
        market.market.toLowerCase().includes(searchQuery.toLowerCase())
    );
</script>

<div class="h-full flex flex-col space-y-4">
    <div class="bg-white p-4 rounded-lg shadow-md border border-gray-500 flex-1 overflow-y-auto">
        <h2 class="text-xl font-semibold mb-1 text-gray-800 text-center">Markets</h2>
        <Input bind:value={searchQuery} placeholder="Type to choose..." on:input={filterMarketData} class="flex-grow mb-2" />
        <div class="overflow-y-auto">
            <Table class="min-w-full divide-y divide-gray-200">
                <TableHead class="bg-gray-50">
                    <TableHeadCell class="text-center cursor-pointer" on:click={() => handleSort('market')}>
                        Market
                        <span class="ml-1">&#9650;&#9660;</span>
                    </TableHeadCell>
                    <TableHeadCell class="text-center cursor-pointer" on:click={() => handleSort('trade_price')}>
                        Price
                        <span class="ml-1">&#9650;&#9660;</span>
                    </TableHeadCell>
                    <TableHeadCell class="text-center cursor-pointer" on:click={() => handleSort('signed_change_rate')}>
                        Change
                        <span class="ml-1">&#9650;&#9660;</span>
                    </TableHeadCell>
                    <TableHeadCell class="text-center cursor-pointer" on:click={() => handleSort('acc_trade_price_24h')}>
                        Volume
                        <span class="ml-1">&#9650;&#9660;</span>
                    </TableHeadCell>
                </TableHead>
                <TableBody class="bg-white divide-y divide-gray-200">
                    {#each filteredMarketData as market}
                        <TableBodyRow class="cursor-pointer hover:bg-gray-100 {market === selectedMarket ? 'bg-gray-200' : ''}" on:click={() => handleMarketSelect(market)}>
                            <TableBodyCell class="flex items-center justify-center space-x-2">
                                <img src={`/src/assets/currency_logo/${market.market.replace('KRW-', '').toLowerCase()}_logo.png`} alt="Market Icon" class="h-6 w-6">
                                <span class="text-gray-900 font-medium">{market.market.replace('KRW-', '')}</span>
                            </TableBodyCell>
                            <TableBodyCell class="text-right text-gray-500">
                                {formatCurrency(market.trade_price)}
                            </TableBodyCell>
                            <TableBodyCell class="font-semibold text-right {market.signed_change_rate > 0 ? 'text-green-500' : market.signed_change_rate === 0 ? 'text-gray-500' : 'text-red-500'}">
                                {market.signed_change_rate > 0 ? '+' : ''}{formatChangeRate(market.signed_change_rate)}%
                            </TableBodyCell>
                            <TableBodyCell class="text-right text-gray-500">
                                {formatCurrency(market.acc_trade_price_24h / 1e6)}M
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </div>
    </div>
</div>

<style>
</style>
