<script>
    import { formatCurrency } from "../../utils/formatCurrency";
    export let selectedMarket;

    $: selectedMarketCodeUnit = selectedMarket?.market.split('-')[1].toUpperCase();
</script>

<div class="col-span-7 bg-white p-4 rounded border border-gray-400">
    {#if selectedMarket}
        <div class="flex justify-between items-center mb-4">
            <div class="flex items-center space-x-2">
                <img src="src/assets/currency_logo/{selectedMarket.market.replace('KRW-', '').toLowerCase()}_logo.png" alt="Market Icon" class="h-6 w-6 rounded-full">
                <h2 class="text-2xl font-semibold text-gray-800">{selectedMarket.market.replace('KRW-', '')}</h2>
            </div>
            <div class="space-y-1 text-right">
                <span class="text-2xl block text-gray-800">{formatCurrency(selectedMarket.trade_price)}</span>
                <span class="block" class:text-red-500={selectedMarket.change === 'FALL'} class:text-green-500={selectedMarket.change === 'RISE'}>
                    {selectedMarket.change === 'FALL' ? '-' : '+'}{formatCurrency(selectedMarket.signed_change_price)} ({(selectedMarket.change_rate * 100).toFixed(2)}%)
                </span>
            </div>
        </div>

        <!-- Info Panel -->
        <div class="p-2 rounded mb-4 border border-gray-400">
            <div class="grid grid-cols-3 gap-4 text-center">
                <div>
                    <p class="text-sm text-gray-500">24h High</p>
                    <p class="text-lg font-semibold text-gray-800">{formatCurrency(selectedMarket.high_price)}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">24h Low</p>
                    <p class="text-lg font-semibold text-gray-800">{formatCurrency(selectedMarket.low_price)}</p>
                </div>
                <div>
                    <p class="text-sm text-gray-500">24h Volume (KRW)</p>
                    <p class="text-lg font-semibold text-gray-800">{formatCurrency(selectedMarket.acc_trade_price_24h)}</p>
                </div>
            </div>
        </div>

        <!-- Trading Chart Area -->
        <div class="p-4 rounded h-80 border border-gray-400 bg-white">
            <p class="text-center text-gray-500">Trading chart here</p>
        </div>
    {:else}
        <p class="text-center text-gray-500">Loading...</p>
    {/if}
</div>
