<script>
    import { onMount } from 'svelte';
    import { getAllAvailableMarketsInfo } from './functions/getMarketInfo';
    import { balances } from '../../stores/usesrAssets';
    import queryString from 'query-string';
    import LeftPanel from './leftPanel.svelte';
    import CenterPanel from './centerPanel.svelte';
    import RightPanel from './rightPanel.svelte';

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

    function setSelectedMarket(market) {
        selectedMarket = market;
        selectedMarketCodeUnit = market.market.split('-')[1].toUpperCase();
    }

    // Update the available balance whenever the selected market changes
    $: selectedMarketCodeUnit = selectedMarket?.market.split('-')[1].toUpperCase();
    $: availableBalance = $balances[selectedMarketCodeUnit]?.amount ?? 0;

    // Automatically gathers market information and refresh selectedaMarket for simultaneous updates, every 2 seconds
    setInterval(async () => {
        marketData = await getAllAvailableMarketsInfo();
        selectedMarket = marketData.find(market => market.market === selectedMarket.market) || marketData[0];
    }, 2000);

    // Automatically update the available balance when the user's assets change
    // Automatically update the market data when the user's assets change
    $: balances.subscribe(value => {
        availableBalance = value[selectedMarketCodeUnit]?.amount ?? 0;
    });

</script>

<main class="h-screen bg-gray-100 font-sans">
    <div class="grid grid-cols-12 gap-4 p-4 h-full">
        <div class="col-span-2 h-full">
            <LeftPanel {marketData} {setSelectedMarket} />
        </div>
        <div class="col-span-7 h-full">
            <CenterPanel {selectedMarket} />
        </div>
        <div class="col-span-3 h-full">
            <RightPanel {selectedMarketCodeUnit} {availableBalance} />
        </div>
    </div>
</main>

<style>
    main {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
