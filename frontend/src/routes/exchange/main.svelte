<!-- src/routes/exchange/main.svelte  -->

<script>
    import { onMount } from 'svelte';
    import { getAllAvailableMarketsInfo } from './functions/getMarketInfo';
    import { balances } from '../../stores/usesrAssets';
    import queryString from 'query-string';
    import CenterPanel from './centerPanel.svelte';
    import RightPanel from './rightPanel.svelte';
    import MarketSelectorModal from './MarketSelectorModal.svelte';

    export let marketData = [];
    let selectedMarket = null;
    let selectedMarketCodeUnit = null;
    let availableBalance = 0;
    let currentPrice = 0;
    let showModal = false;

    onMount(async () => {
        try {
            marketData = await getAllAvailableMarketsInfo();
            const queryParameters = queryString.parse(window.location.search);
            const selectedMarketCode = queryParameters.code || 'KRW-BTC';
            selectedMarketCodeUnit = selectedMarketCode.toString().split('-')[1].toUpperCase();
            selectedMarket = marketData.find(market => market.market === selectedMarketCode) || marketData[0];
            currentPrice = selectedMarket.trade_price;
        } catch (error) {
            console.error(error);
        }
    });

    function setSelectedMarket(market) {
        selectedMarket = market;
        selectedMarketCodeUnit = market.market.split('-')[1].toUpperCase();
        currentPrice = market.trade_price;
    }

    function setShowModal(value) {
        showModal = value;
    }

    $: selectedMarketCodeUnit = selectedMarket?.market.split('-')[1].toUpperCase();
    $: availableBalance = $balances[selectedMarketCodeUnit]?.amount ?? 0;

    setInterval(async () => {
        marketData = await getAllAvailableMarketsInfo();
        selectedMarket = marketData.find(market => market.market === selectedMarket.market) || marketData[0];
        currentPrice = selectedMarket.trade_price;
    }, 2000);

    $: balances.subscribe(value => {
        availableBalance = value[selectedMarketCodeUnit]?.amount ?? 0;
    });
</script>

<main class="h-screen bg-gray-100 font-sans">
    <div class="grid grid-cols-12 gap-4 p-4 h-full">
        <div class="col-span-9 h-full">
            <CenterPanel {selectedMarket} {setShowModal} />
        </div>
        <div class="col-span-3 h-full">
            <RightPanel {selectedMarketCodeUnit} {availableBalance} {currentPrice} />
        </div>
        {#if showModal}
            <MarketSelectorModal {marketData} {setSelectedMarket} on:close={() => setShowModal(false)} />
        {/if}
    </div>
</main>

<style>
    main {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
