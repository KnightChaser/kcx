<!-- routes/exchange/marketSelectorModal.svelte  -->

<script>
    import { createEventDispatcher } from 'svelte';
    import { formatCurrency } from '../../utils/formatCurrency';
    export let marketData;
    export let setSelectedMarket;

    const dispatch = createEventDispatcher();

    function handleClose() {
        dispatch('close');
    }

    function handleMarketSelect(market) {
        setSelectedMarket(market);
        handleClose();
    }

    function formatChangeRate(changeRate) {
        return (changeRate * 100).toFixed(2);
    }
</script>

<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-4 rounded-lg shadow-md border border-gray-500 max-h-3/4 w-full sm:w-3/4 lg:w-1/2 overflow-y-auto relative">
        <button on:click={handleClose} class="absolute top-2 right-2 text-gray-500 hover:text-gray-900 text-2xl">
            &times;
        </button>
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Markets</h2>
        <div class="overflow-y-auto max-h-full">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Market
                        </th>
                        <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Change
                        </th>
                        <th scope="col" class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Trade Price
                        </th>
                        <th scope="col" class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Trade Volume
                        </th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    {#each marketData as market}
                        <tr class="cursor-pointer hover:bg-gray-100" on:click={() => handleMarketSelect(market)}>
                            <td class="px-4 py-2 whitespace-nowrap flex items-center space-x-2">
                                <img src={`/src/assets/currency_logo/${market.market.replace('KRW-', '').toLowerCase()}_logo.png`} alt="Market Icon" class="h-6 w-6">
                                <span class="text-gray-900 font-medium">{market.market.replace('KRW-', '')}</span>
                            </td>
                            <td class="px-4 py-2 whitespace-nowrap font-semibold {market.signed_change_rate > 0 ? 'text-green-500' : 'text-red-500'}">
                                {market.signed_change_rate > 0 ? '+' : '-'}{formatChangeRate(market.change_rate)}%
                            </td>
                            <td class="px-4 py-2 whitespace-nowrap text-right text-sm text-gray-500">
                                {formatCurrency(market.trade_price)}
                            </td>
                            <td class="px-4 py-2 whitespace-nowrap text-right text-sm text-gray-500">
                                {formatCurrency(market.acc_trade_price_24h)}
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>
