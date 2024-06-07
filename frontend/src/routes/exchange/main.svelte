<!-- routes/exchange/main.svelte  -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import { getAllAvailableMarketsInfo } from './functions/getMarketInfo';
    import { balances } from '../../stores/usesrAssets';
    import queryString from 'query-string';
    import CenterPanel from './centerPanel.svelte';
    import LeftPanel from './leftPanel.svelte';

    export let marketData = [];             // Market data
    let selectedMarket = null;              // Selected market (the market that the user is currently viewing)
    let selectedMarketCodeUnit = null;      // The unit of the selected market
    let availableBalance = 0;               // The available balance of the selected market
    let currentPrice = 0;                   // The current price of the selected market
    let intervalId;                         // The interval ID for fetching market data

    let sortKey = '';                       // The key to sort the market data by (e.g., market, signed_change_rate, trade_price, acc_trade_price_24h)
    let sortOrder = 'asc';                  // The sort order (asc for ascending, desc for descending)

    onMount(async () => {
        try {
            // Fetch the market data
            marketData = await getAllAvailableMarketsInfo();
            const queryParameters = queryString.parse(window.location.search);
            const selectedMarketCode = queryParameters.code || 'KRW-BTC';
            selectedMarketCodeUnit = selectedMarketCode.toString().split('-')[1].toUpperCase();
            selectedMarket = marketData.find(market => market.market === selectedMarketCode) || marketData[0];
            currentPrice = selectedMarket.trade_price;
            
            // Sort the market data
            sortMarketData();
        } catch (error) {
            console.error(error);
        }

        // Fetch the market data every 2 seconds
        intervalId = setInterval(async () => {
            marketData = await getAllAvailableMarketsInfo();
            selectedMarket = marketData.find(market => market.market === selectedMarket.market) || marketData[0];
            currentPrice = selectedMarket.trade_price;
            sortMarketData();
        }, 2000);
    });

    // Clear the interval when the component is destroyed
    onDestroy(() => {
        if (intervalId) {
            clearInterval(intervalId);
        }
    });

    // Set the selected market
    function setSelectedMarket(market) {
        selectedMarket = market;
        selectedMarketCodeUnit = market.market.split('-')[1].toUpperCase();
        currentPrice = market.trade_price;
    }

    // Handle the sorting of the market data
    function handleSort(event) {
        const { key } = event.detail;
        if (sortKey === key) {
            sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
        } else {
            sortKey = key;
            sortOrder = 'asc';
        }
        sortMarketData();
    }

    // Sort the market data based on the sort key and sort order
    function sortMarketData() {
        if (!sortKey) return;

        marketData = marketData.slice().sort((a, b) => {
            const valueA = a[sortKey];
            const valueB = b[sortKey];

            if (valueA < valueB) {
                return sortOrder === 'asc' ? -1 : 1;
            }
            if (valueA > valueB) {
                return sortOrder === 'asc' ? 1 : -1;
            }
            return 0;
        });
    }

    $: selectedMarketCodeUnit = selectedMarket?.market.split('-')[1].toUpperCase();
    $: availableBalance = $balances[selectedMarketCodeUnit]?.amount ?? 0;

    $: balances.subscribe(value => {
        availableBalance = value[selectedMarketCodeUnit]?.amount ?? 0;
    });
</script>

<main class="h-screen bg-gray-100 font-sans">
    <div class="grid grid-cols-10 h-full">
        <div class="col-span-3 h-full">
            <LeftPanel {marketData} {setSelectedMarket} on:sort={handleSort} />
        </div>
        <div class="col-span-7 h-full">
            <CenterPanel {selectedMarket} {availableBalance} {currentPrice} />
        </div>
    </div>
</main>

<style>
    main {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
