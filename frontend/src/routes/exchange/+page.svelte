<!-- frontend/src/routes/exchange/+page.svelte -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import { getAllAvailableMarketsInfo } from './functions/getMarketInfo.js';
    import { balances } from '../../stores/usesrAssets';
    import { selectedMarketCode } from './stores/selectedMarketStore.js';
    import HeaderPanel from './headerPanel.svelte';
    import LeftPanel from './leftPanel.svelte';
    import ChartPanel from './chartPanel.svelte';
    import OrderPanel from './orderPanel.svelte';
    import { get } from 'svelte/store';

    let marketData = [];             // Market data
    let selectedMarket = null;       // Selected market (the market that the user is currently viewing)
    let selectedMarketCodeUnit = null; // The unit of the selected market
    let availableBalance = 0;        // The available balance of the selected market
    let currentPrice = 0;            // The current price of the selected market
    let intervalId;                  // The interval ID for fetching market data

    let sortKey = '';                // The key to sort the market data by (e.g., market, signed_change_rate, trade_price, acc_trade_price_24h)
    let sortOrder = 'asc';           // The sort order (asc for ascending, desc for descending)

    async function fetchMarketData() {
        try {
            marketData = await getAllAvailableMarketsInfo();
            const initialMarketCode = get(selectedMarketCode);  // Get the initial value from the store
            selectedMarket = marketData.find(market => market.market === initialMarketCode) || marketData[0];
            selectedMarketCode.set(selectedMarket.market);
            selectedMarketCodeUnit = selectedMarket.market.split('-')[1].toUpperCase();
            currentPrice = selectedMarket.trade_price;
            sortMarketData();
        } catch (error) {
            console.error(error);
        }
    }

    onMount(async () => {
        await fetchMarketData();
        intervalId = setInterval(fetchMarketData, 2000);
    });

    onDestroy(() => {
        if (intervalId) {
            clearInterval(intervalId);
        }
    });

    function setSelectedMarket(market) {
        selectedMarket = market;
        selectedMarketCode.set(market.market);
        selectedMarketCodeUnit = market.market.split('-')[1].toUpperCase();
        currentPrice = market.trade_price;
    }

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

<main class="h-[130vh] font-sans overflow-hidden">
    <div class="grid grid-cols-10 h-full">
        <div class="col-span-3 h-full">
            <LeftPanel {marketData} {setSelectedMarket} {selectedMarket} on:sort={handleSort} />
        </div>
        <div class="col-span-7 h-full">
            <HeaderPanel {selectedMarket} {selectedMarketCodeUnit} />
            <ChartPanel {selectedMarket} {selectedMarketCodeUnit} />
            <OrderPanel {selectedMarket} {availableBalance} {currentPrice} />
        </div>
    </div>
</main>

<style>
    main {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
    .grid {
        overflow: hidden;
    }
    .col-span-3, .col-span-7 {
        height: 100%;
        display: flex;
        flex-direction: column;
    }
</style>
