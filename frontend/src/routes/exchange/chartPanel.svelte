<!-- frontend/src/routes/exchange/chartPanel.svelte -->

<script>
    import { onMount, afterUpdate } from 'svelte';
    import { selectedMarketCode } from './stores/selectedMarketStore.js';
    import { derived } from 'svelte/store';

    const selectedMarketCodeUnit = derived(selectedMarketCode, ($selectedMarketCode) => $selectedMarketCode.split('-')[1].toUpperCase());

    export let selectedMarket;

    let tradingViewWidgetContainer;
    let previousMarket;

    function loadTradingViewWidget(market) {
        const script = document.createElement('script');
        script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
        script.async = true;
        script.innerHTML = JSON.stringify({
            "autosize": true,
            "symbol": `UPBIT:${$selectedMarketCodeUnit}KRW`,
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

<div class="p-2 h-[450px] border-b border-gray-400 bg-white">
    <div bind:this={tradingViewWidgetContainer} class="tradingview-widget-container" style="height:100%;width:100%">
    </div>
</div>
