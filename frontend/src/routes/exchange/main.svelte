<script>
    import { onMount } from 'svelte';
    import { getAllAvailableMarketsInfo } from './functions/getMarketInfo';
    import { balances } from '../../stores/usesrAssets';
    import queryString from 'query-string';

    // Exchange page components will share these variables to render the data
    let marketData = [];
    let selectedMarket = null;
    let selectedMarketCodeUnit = null;
    let availableBalance = 0;  // Change to a reactive variable

    onMount(async () => {
        try {
            marketData = await getAllAvailableMarketsInfo();

            // Get the query string to decide which market to display
            const queryParameters = queryString.parse(window.location.search);
            const selectedMarketCode = queryParameters.code || 'KRW-BTC';  // Default market is KRW-BTC (Bitcoin market)
            selectedMarketCodeUnit = selectedMarketCode.toString().split('-')[1].toUpperCase();  // ex. "KRW-BTC" => "BTC"

            // Find the selected market from the market data
            selectedMarket = marketData.find(market => market.market === selectedMarketCode) || marketData[0];
        } catch (error) {
            console.error(error);
        }
    });

    // Update the available balance whenever the selected market changes
    $: selectedMarketCodeUnit = selectedMarket?.market.split('-')[1].toUpperCase();
    $: availableBalance = $balances[selectedMarketCodeUnit]?.amount ?? 0;

    function formatCurrency(value) {
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value);
    }
</script>

<main class="h-screen bg-gray-100 font-sans">
    <!-- Content -->
    <div class="grid grid-cols-12 gap-4 p-4">
        <!-- Left Panel -->
        <div class="col-span-2 bg-white p-4 rounded border border-gray-400">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">Markets</h2>
            <ul class="space-y-2">
                {#each marketData as market}
                    <button 
                        class="cursor-pointer"
                        class:text-red-500={market.change === 'FALL'}
                        class:text-green-500={market.change === 'RISE'}
                        on:click={() => {
                            selectedMarket = market;
                            selectedMarketCodeUnit = market.market.split('-')[1].toUpperCase();
                        }}
                    >
                        {market.market.replace('KRW-', '')} {market.change === 'FALL' ? '-' : '+'}{(market.change_rate * 100).toFixed(2)}%
                    </button>
                {/each}
            </ul>
        </div>

        <!-- Center Panel -->
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

        <!-- Right Panel -->
        <div class="col-span-3 bg-white p-4 rounded border border-gray-400 space-y-4">
            <div class="p-4 rounded border border-gray-400 bg-white">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">Place Order</h2>
                <div class="space-y-4">
                    <div class="space-y-2">
                        <input type="text" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Target price (KRW)" aria-label="Target price (KRW)">
                    </div>
                    <div class="space-y-2">
                        <input type="text" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Size" aria-label="Size">
                    </div>
                    <div class="space-y-2">
                        <input type="text" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Take profit (KRW)" aria-label="Take profit (KRW)">
                    </div>
                    <div class="space-y-2">
                        <input type="text" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Stop loss (KRW)" aria-label="Stop loss (KRW)">
                    </div>
                    <div class="space-y-2">
                        <p class="block text-sm text-gray-700">Available Balance</p>
                        <p class="text-lg font-semibold text-gray-800">{formatCurrency($balances.KRW.amount)}</p>
                    </div>
                    <div class="space-y-2">
                        <p class="block text-sm text-gray-700">Available {selectedMarketCodeUnit}</p>
                        <p class="text-lg font-semibold text-gray-800">{availableBalance} {selectedMarketCodeUnit}</p> <!-- Fixed -->
                    </div>
                    <div class="flex space-x-2">
                        <button class="bg-blue-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500">BUY</button>
                        <button class="bg-red-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-red-500">SELL</button>
                    </div>
                </div>
            </div>

            <div class="p-4 rounded border border-gray-400 bg-white">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">Your order history</h2>
                <p class="text-gray-500">Your order</p>
            </div>
        </div>
    </div>
</main>

<style>
    main {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
