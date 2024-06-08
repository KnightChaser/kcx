<script>
    import { balances } from "../../stores/usesrAssets";
    import { formatCurrency } from "../../utils/formatCurrency";
    import { onMount, afterUpdate } from 'svelte';
    import { handleBuy, handleSell } from "./functions/buySellHandler";

    export let selectedMarket;
    export let availableBalance;
    export let currentPrice;

    let tradingViewWidgetContainer;
    let size = 0;
    let totalValue = 0;
    let sliderValue = 0;
    let mode = 'buy';  // Mode: 'buy' or 'sell'

    $: krwBalance = $balances.KRW.amount;

    // Get the value of slider and calculate the size and total value accordingly
    const handleSliderChange = (event) => {
        sliderValue = event.target.value;
        calculateValues();
    };

    // Get the value of size and calculate the total value accordingly
    // Because the value is localized with commas, we need to remove them before parsing
    const handleSizeChange = (event) => {
        size = parseFloat(event.target.value.replace(/,/g, ''));
        totalValue = Math.floor(size * currentPrice);
        sliderValue = mode === 'buy' ? totalValue / krwBalance : size / availableBalance;
    };

    // Get the value of total value and calculate the size accordingly
    // Because the value is localized with commas, we need to remove them before parsing
    const handleTotalValueChange = (event) => {
        totalValue = parseFloat(event.target.value.replace(/,/g, ''));
        size = totalValue / currentPrice;
        sliderValue = mode === 'buy' ? totalValue / krwBalance : size / availableBalance;
    };

    // Set the percentage of the slider
    const setPercentage = (percentage) => {
        sliderValue = percentage / 100;
        calculateValues();
    };

    // Calculate the size and total value based on the mode
    const calculateValues = () => {
        if (mode === 'buy') {
            // If the user is buying, the size is calculated based on the total value
            totalValue = Math.floor(sliderValue * krwBalance);
            size = totalValue / currentPrice;
        } else {
            // If the user is selling, the size is calculated based on the available balance
            size = sliderValue * availableBalance;
            totalValue = Math.floor(size * currentPrice);
        }
    };

    // Switch the mode between 'buy' and 'sell'
    const switchMode = (newMode) => {
        mode = newMode;
        resetValues();
    };

    // Reset the values
    const resetValues = () => {
        sliderValue = 0;
        size = 0;
        totalValue = 0;
        calculateValues();
    };

    // Format the number with commas
    const formatWithCommas = (value) => {
        const parts = value.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        return parts.join(".");
    };

    // Load the TradingView widget with the selected market
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
            resetValues();
        }
    });

    $: selectedMarketCodeUnit = selectedMarket?.market.split('-')[1].toUpperCase();
</script>

<div class="h-full bg-white rounded border border-gray-400">
    {#if selectedMarket}
        <div class="flex items-center justify-between border-b border-gray-400 p-2">
            <div class="flex items-center space-x-4 pl-2">
                <img src="/src/assets/currency_logo/{selectedMarket.market.replace('KRW-', '').toLowerCase()}_logo.png" alt="Market Icon" class="h-10 w-10">
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
                <div class="flex justify-center mb-4">
                    <button on:click={() => switchMode('buy')} class={`px-4 py-2 rounded-l ${mode === 'buy' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>Buy</button>
                    <button on:click={() => switchMode('sell')} class={`px-4 py-2 rounded-r ${mode === 'sell' ? 'bg-red-500 text-white' : 'bg-gray-200'}`}>Sell</button>
                </div>
                <div class="space-y-4">
                    <div class="flex space-x-4">
                        <div class="flex-1">
                            <label for="totalValue" class="block text-sm font-medium leading-6 text-gray-900">Total Value</label>
                            <div class="relative mt-2 rounded-md shadow-sm">
                                <input type="text" value={formatWithCommas(totalValue)} on:input={handleTotalValueChange} id="totalValue" class="block w-full text-right rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6" placeholder="0.00" />
                                <div class="absolute inset-y-0 right-0 flex items-center">
                                    <span class="text-gray-500 sm:text-sm pr-3">KRW</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex-1">
                            <label for="size" class="block text-sm font-medium leading-6 text-gray-900">Size</label>
                            <div class="relative mt-2 rounded-md shadow-sm">
                                <input type="text" value={formatWithCommas(size)} on:input={handleSizeChange} id="size" class="block w-full text-right rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6" placeholder="0.00">
                                <div class="absolute inset-y-0 right-0 flex items-center">
                                    <span class="text-gray-500 sm:text-sm pr-3">{selectedMarketCodeUnit}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <input type="range" min="0" max="1" step="0.01" bind:value={sliderValue} on:input={handleSliderChange} class="w-full">
                        <div class="flex justify-between text-xs text-gray-500 mt-1">
                            <span>0%</span>
                            <span>10%</span>
                            <span>20%</span>
                            <span>30%</span>
                            <span>40%</span>
                            <span>50%</span>
                            <span>60%</span>
                            <span>70%</span>
                            <span>80%</span>
                            <span>90%</span>
                            <span>100%</span>
                        </div>
                    </div>
                    <div class="flex justify-between space-x-2 mt-2">
                        <button on:click={() => setPercentage(20)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">20%</button>
                        <button on:click={() => setPercentage(40)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">40%</button>
                        <button on:click={() => setPercentage(60)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">60%</button>
                        <button on:click={() => setPercentage(80)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">80%</button>
                        <button on:click={() => setPercentage(100)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">100%</button>
                    </div>
                    <table class="w-full mt-4">
                        <tbody class="divide-y divide-gray-200">
                            <tr>
                                <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Available Balance</td>
                                <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                                    {formatWithCommas(Math.floor(krwBalance))} KRW 
                                    <div class="text-sm text-gray-500">(≈ {formatWithCommas((krwBalance / currentPrice).toFixed(4))} {selectedMarketCodeUnit})</div>
                                </td>
                            </tr>
                            <tr>
                                <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Available {selectedMarketCodeUnit}</td>
                                <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                                    {formatWithCommas(availableBalance.toFixed(4))} {selectedMarketCodeUnit}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="flex space-x-2">
                        <button on:click={() => mode === 'buy' ? handleBuy(selectedMarketCodeUnit, size, currentPrice) : handleSell(selectedMarketCodeUnit, size, currentPrice)} class={`bg-${mode === 'buy' ? 'blue' : 'red'}-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-${mode === 'buy' ? 'blue' : 'red'}-500`}>Proceed Order</button>
                    </div>
                </div>
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
