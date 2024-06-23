<!-- frontend/src/routes/exchange/leftPanel.svelte  -->

<script>
    import { createEventDispatcher } from 'svelte';
    import { formatCurrency } from '../../utils/formatCurrency';
    export let marketData;
    export let setSelectedMarket;

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
        <div class="mb-4 flex">
            <input
                type="text"
                placeholder="Type to choose..."
                class="flex-grow p-2 border border-gray-300 rounded-l"
                bind:value={searchQuery}
                on:input={filterMarketData}
            />
            <button class="px-4 py-2 bg-blue-500 text-white rounded-r" on:click={filterMarketData}>Search</button>
        </div>
        <div class="overflow-y-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col" class="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" on:click={() => handleSort('market')}>
                            Market<br>
                            <span class="ml-1">&#9650;&#9660;</span>
                        </th>
                        <th scope="col" class="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" on:click={() => handleSort('trade_price')}>
                            Price<br>
                            <span class="ml-1">&#9650;&#9660;</span>
                        </th>
                        <th scope="col" class="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" on:click={() => handleSort('signed_change_rate')}>
                            Change<br>
                            <span class="ml-1">&#9650;&#9660;</span>
                        </th>
                        <th scope="col" class="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" on:click={() => handleSort('acc_trade_price_24h')}>
                            Volume<br>
                            <span class="ml-1">&#9650;&#9660;</span>
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    {#each filteredMarketData as market}
                        <tr class="cursor-pointer hover:bg-gray-100" on:click={() => handleMarketSelect(market)}>
                            <td class="px-4 py-2 whitespace-nowrap flex items-center text-center space-x-2">
                                <img src={`/src/assets/currency_logo/${market.market.replace('KRW-', '').toLowerCase()}_logo.png`} alt="Market Icon" class="h-6 w-6">
                                <span class="text-gray-900 font-medium">{market.market.replace('KRW-', '')}</span>
                            </td>
                            <td class="px-4 py-2 whitespace-nowrap text-sm text-right text-gray-500">
                                {formatCurrency(market.trade_price)}
                            </td>
                            <td class="px-4 py-2 whitespace-nowrap font-semibold text-right {market.signed_change_rate > 0 ? 'text-green-500' : market.signed_change_rate === 0 ? 'text-gray-500' : 'text-red-500'}">
                                {market.signed_change_rate > 0 ? '+' : ''}{formatChangeRate(market.signed_change_rate)}%
                            </td>
                            <td class="px-4 py-2 whitespace-nowrap text-sm text-right text-gray-500">
                                {formatCurrency(market.acc_trade_price_24h / 1e6)}M
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>

<style>
    .h-full {
        height: 100%;
    }
    .overflow-y-auto {
        max-height: calc(124vh);
    }
</style>
