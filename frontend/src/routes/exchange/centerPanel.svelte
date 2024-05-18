<!-- routes/exchange/centerPanel.svelte -->

<script>
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

<div class="col-span-7 bg-white p-4 rounded border border-gray-400">
    {#if selectedMarket}
        <div class="flex justify-between items-center mb-4">
            <div class="flex items-center space-x-2">
                <img src="src/assets/currency_logo/{selectedMarket.market.replace('KRW-', '').toLowerCase()}_logo.png" alt="Market Icon" class="h-6 w-6 rounded-full">
                <h2 class="text-2xl font-semibold text-gray-800">{selectedMarket.market.replace('KRW-', '')}</h2>
                <button on:click={() => setShowModal(true)} class="ml-4 btn btn-primary">
                    Select Market
                </button>
            </div>
            <div class="space-y-1 text-right">
                <span class="text-2xl block text-gray-800">{formatCurrency(selectedMarket.trade_price)}</span>
                <span class="block" class:text-red-500={selectedMarket.change === 'FALL'} class:text-green-500={selectedMarket.change === 'RISE'}>
                    {selectedMarket.change === 'FALL' ? '' : '+'}{formatCurrency(selectedMarket.signed_change_price)} ({(selectedMarket.signed_change_rate * 100).toFixed(2)}%)
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
        <div class="p-4 rounded h-[500px] border border-gray-400 bg-white">
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
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .btn-primary:hover {
        background-color: #2779bd;
    }
</style>
