<!-- routes/exchange/centerPanel.svelte -->

<script>
    import { balances } from "../../stores/usesrAssets";
    import { formatCurrency } from "../../utils/formatCurrency";
    import { onMount, afterUpdate } from 'svelte';
    export let selectedMarket;
    export let setShowModal;

    $: selectedMarketCodeUnit = selectedMarket?.market.split('-')[1].toUpperCase();

    let tradingViewWidgetContainer;

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
            <button on:click={() => setShowModal(true)} class="btn btn-primary flex items-center justify-center h-8 w-8 p-2 rounded-full">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
                    <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                </svg>    
            </button>
        </div>

        <!-- Trading Chart Area -->
        <div class="p-2 h-[600px] border border-gray-400 bg-white">
            <!-- TradingView Widget BEGIN -->
            <div bind:this={tradingViewWidgetContainer} class="tradingview-widget-container" style="height:100%;width:100%">
                <!-- Widget will be inserted here dynamically -->
            </div>
            <!-- TradingView Widget END -->
        </div>
    {:else}
        <p class="text-center text-gray-500">Loading...</p>
    {/if}
</div>

<style>
    .btn-primary {
        background-color: #3490dc;
        color: white;
        padding: 8px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .btn-primary:hover {
        background-color: #2779bd;
    }
</style>
