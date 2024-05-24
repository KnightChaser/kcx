<!-- routes/exchange/centerPanel.svelte -->

<script>
    import { balances } from "../../stores/usesrAssets";
    import { formatCurrency } from "../../utils/formatCurrency";
    import { onMount, afterUpdate } from 'svelte';
    import { handleBuy } from "./functions/buySellHandler";
    import { handleSell } from "./functions/buySellHandler";
    export let selectedMarket;
    export let availableBalance;
    export let currentPrice;

    let tradingViewWidgetContainer;
    let size = 0;
    let totalValue = 0;
    let sliderValue = 0;  // Slider value to bind with input

    // Get the user's KRW balance
    $: krwBalance = $balances.KRW.amount;
    $: totalValue = size * currentPrice;

    const handleSliderChange = (event) => {
        sliderValue = event.target.value;
        totalValue = sliderValue * krwBalance;
        size = totalValue / currentPrice;
    };

    const handleSizeChange = () => {
        totalValue = size * currentPrice;
        sliderValue = totalValue / krwBalance;
    };

    function loadTradingViewWidget(market) {
        const script = document.createElement('script');
        script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
        script.async = true;
        script.innerHTML = JSON.stringify({
            "autosize": true,
            "symbol": `UPBIT:${selectedMarketCodeUnit}KRW`,
            "interval": "15",
            "timezone": "Asia/Seoul",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "withdateranges": true,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "calendar": false,
            "studies": [
                "STD;Bollinger_Bands"
            ],
            "support_host": "https://www.tradingview.com"
        });
        tradingViewWidgetContainer.innerHTML = '';
        tradingViewWidgetContainer.appendChild(script);
    }

    let previousMarket;

    onMount(() => {
        if (selectedMarket) {
            loadTradingViewWidget(selectedMarket);
            previousMarket = selectedMarket.market;
        }
    });

    afterUpdate(() => {
        if (selectedMarket && selectedMarket.market !== previousMarket) {
            loadTradingViewWidget(selectedMarket);
            previousMarket = selectedMarket.market;
        }
    });

    $: selectedMarketCodeUnit = selectedMarket?.market.split('-')[1].toUpperCase();
</script>

<div class="h-full bg-white rounded border border-gray-400">
    {#if selectedMarket}
        <div class="flex items-center justify-between border-b border-gray-400 p-2">
            <div class="flex items-center space-x-4 pl-2">
                <img src="src/assets/currency_logo/{selectedMarket.market.replace('KRW-', '').toLowerCase()}_logo.png" alt="Market Icon" class="h-10 w-10">
                <div>
                    <h2 class="text-3xl font-semibold text-gray-800">{selectedMarketCodeUnit}</h2>
                    <h1 class="text-lg font-medium text-gray-500">{$balances[selectedMarketCodeUnit]?.fullname}</h1>
                </div>
            </div>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 max-w-full">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-4 py-2 text-sm font-medium text-gray-500 uppercase tracking-wider text-center">Current Price</th>
                            <th class="px-4 py-2 text-sm font-medium text-gray-500 uppercase tracking-wider text-center">24h Change</th>
                            <th class="px-4 py-2 text-sm font-medium text-gray-500 uppercase tracking-wider text-center">24h Low/High</th>
                            <th class="px-4 py-2 text-sm font-medium text-gray-500 uppercase tracking-wider text-center">24h Volume</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr>
                            <td class="px-4 py-2 whitespace-nowrap text-center text-4xl font-semibold text-gray-800">{formatCurrency(selectedMarket.trade_price)}</td>
                            <td class="px-4 py-2 whitespace-nowrap text-center {selectedMarket.change === 'FALL' ? 'text-red-500' : 'text-green-500'} text-lg font-semibold">
                                {selectedMarket.change === 'FALL' ? '' : '+'}{formatCurrency(selectedMarket.signed_change_price)} <br>
                                ({(selectedMarket.signed_change_rate * 100).toFixed(2)}%)
                            </td>
                            <td class="px-4 py-2 whitespace-nowrap text-center text-lg font-semibold text-gray-800">{formatCurrency(selectedMarket.low_price)}<br>{formatCurrency(selectedMarket.high_price)}</td>
                            <td class="px-4 py-2 whitespace-nowrap text-center text-m font-semibold text-gray-800">{formatCurrency(selectedMarket.acc_trade_price_24h)}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Trading Chart Area -->
        <div class="p-2 h-[400px] border-b border-gray-400 bg-white">
            <!-- TradingView Widget BEGIN -->
            <div bind:this={tradingViewWidgetContainer} class="tradingview-widget-container" style="height:100%;width:100%">
                <!-- Widget will be inserted here dynamically -->
            </div>
            <!-- TradingView Widget END -->
        </div>

        <!-- Order Panel -->
        <div class="p-4 bg-white border-gray-300 space-y-4">
            <div class="p-4 rounded border border-gray-300 bg-white shadow-sm">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">Place Order</h2>
                <div class="space-y-4">
                    <div>
                        <label for="size" class="block text-sm font-medium leading-6 text-gray-900">Size</label>
                        <div class="relative mt-2 rounded-md shadow-sm">
                            <input type="number" bind:value={size} on:input={handleSizeChange} id="size" class="block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6" placeholder="0.00">
                            <div class="absolute inset-y-0 right-0 flex items-center">
                                <span class="text-gray-500 sm:text-sm pr-3">{selectedMarketCodeUnit}</span>
                            </div>
                        </div>
                    </div>
                    <div>
                        <input type="range" min="0" max="1" step="0.2" bind:value={sliderValue} on:input={handleSliderChange} class="w-full">
                        <div class="flex justify-between text-xs text-gray-500 mt-1">
                            <span>0%</span>
                            <span>20%</span>
                            <span>40%</span>
                            <span>60%</span>
                            <span>80%</span>
                            <span>100%</span>
                        </div>
                    </div>
                    <table class="w-full">
                        <tbody class="divide-y divide-gray-200">
                            <tr>
                                <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Total Value</td>
                                <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                                    {formatCurrency(totalValue)} 
                                    <div class="text-sm text-gray-500">({(totalValue / currentPrice).toFixed(4)} {selectedMarketCodeUnit})</div>
                                </td>
                            </tr>
                            <tr>
                                <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Available Balance</td>
                                <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                                    {formatCurrency(krwBalance)} 
                                    <div class="text-sm text-gray-500">({(krwBalance / currentPrice).toFixed(4)} {selectedMarketCodeUnit})</div>
                                </td>
                            </tr>
                            <tr>
                                <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Available {selectedMarketCodeUnit}</td>
                                <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                                    {availableBalance.toFixed(4)} {selectedMarketCodeUnit}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="flex space-x-2">
                        <button on:click={() => handleBuy(selectedMarketCodeUnit, size, currentPrice)} class="bg-blue-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500">BUY</button>
                        <button on:click={() => handleSell(selectedMarketCodeUnit, size, currentPrice)} class="bg-red-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-red-500">SELL</button>
                    </div>
                </div>
            </div>

            <div class="p-4 rounded border border-gray-300 bg-white shadow-sm">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">Your order history</h2>
                <p class="text-gray-500">Your order</p>
            </div>
        </div>
    {:else}
        <p class="text-center text-gray-500">Loading...</p>
    {/if}
</div>

<style>
    .h-full {
        height: 100%;
    }
</style>
