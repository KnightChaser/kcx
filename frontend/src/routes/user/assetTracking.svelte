<!-- routes/user/assetTracking.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { push } from "svelte-spa-router";
    import { formatAmount } from '../../utils/formatAmount';
    import { formatCurrency } from '../../utils/formatCurrency';
    import { getAllAvailableMarketsInfo } from '../exchange/functions/getMarketInfo';   
    import CryptoAssetTile from './cryptoAssetTile.svelte';
    import TotalAssetTable from './totalAssetTable.svelte';
    import ProfitTable from './profitTable.svelte';
    import axios from 'axios';
    import Swal from 'sweetalert2';

    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    let balanceData = {};
    let marketData = [];
    let assetTiles = [];
    let totalProfit = 0;
    let totalProfitRate = 0;
    let error = null;

    let intervalId;

    onMount(async () => {
        await fetchAndCalculateData();
        intervalId = setInterval(fetchAndCalculateData, 1000);
    });

    onDestroy(() => {
        clearInterval(intervalId);
    });

    async function fetchAndCalculateData() {
        try {
            // Fetch balance data
            const balanceResponse = await axios.get(`${BACKEND_API_URL}/api/account/balance/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (balanceResponse.status !== 200) {
                Swal.fire({
                    icon: 'error',
                    title: 'Failed to fetch balance',
                    text: 'Failed to fetch balance',
                });
                throw new Error('Failed to fetch balance');
            }
            
            balanceData = balanceResponse.data;
            assetTiles = formatBalanceData(balanceData);

            // Fetch market data
            marketData = await getAllAvailableMarketsInfo();

            // Calculate profitability
            assetTiles = calculateProfitability(assetTiles, marketData);

            // Calculate total profit and profit rate
            const validAssets = assetTiles.filter(tile => tile.profit !== 'N/A' && tile.profit !== 0);
            const totalInvestment = validAssets.reduce((sum, tile) => sum + (tile.averageUnitPrice * tile.amount), 0);
            totalProfit = validAssets.reduce((sum, tile) => sum + parseFloat(tile.profit), 0);
            totalProfitRate = (totalInvestment > 0) ? (totalProfit / totalInvestment) * 100 : 0;
        } catch (err) {
            error = err.message;
            Swal.fire({
                icon: 'error',
                title: 'Failed to fetch data',
                text: error,
            });
        }
    }

    function formatBalanceData(data) {
        return Object.keys(data).filter(key => !key.includes("_average_unit_price")).map(key => ({
            assetName: key,
            amount: data[key],
            averageUnitPrice: data[`${key}_average_unit_price`] || 0
        }));
    }

    function calculateProfitability(assets, marketData) {
        return assets.map(asset => {
            if (asset.amount === 0) {
                return {
                    ...asset,
                    currentPrice: 0,
                    profit: 0,
                    profitRate: 0
                };
            }

            const marketInfo = marketData.find(market => market.market === `KRW-${asset.assetName}`);
            if (marketInfo) {
                const currentPrice = marketInfo.trade_price;
                const profit = (currentPrice - asset.averageUnitPrice) * asset.amount;
                const profitRate = ((currentPrice / asset.averageUnitPrice) * 100 - 100).toFixed(2);
                return {
                    ...asset,
                    currentPrice,
                    profit: profit.toFixed(0),
                    profitRate
                };
            } else {
                return {
                    ...asset,
                    currentPrice: 'N/A',
                    profit: 'N/A',
                    profitRate: 'N/A'
                };
            }
        });
    }

    function moveTouserPage() {
        push("/user/main");
    }
</script>

<div class="w-full max-w-6xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6">
    <div class="flex justify-between items-center">
        <h2 class="text-2xl font-semibold text-gray-900">Asset Tracking</h2>
        <button 
            class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
            on:click={moveTouserPage}>
            Back to User Page
        </button>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <TotalAssetTable 
            totalAssetKRWTargetElement="#total-asset-krw" 
            totalAssetBTCTargetElement="#total-asset-btc"
        />
        <ProfitTable 
            totalProfit={totalProfit}
            totalProfitRate={totalProfitRate}
            totalProfitKRWTargetElement="#total-profit-krw"
            totalProfitRateTargetElement="#total-profit-rate"
        />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {#each assetTiles as tile}
            <CryptoAssetTile 
                assetName={tile.assetName}
                amount={tile.amount}
                averageUnitPrice={tile.averageUnitPrice}
                currentPrice={tile.currentPrice}
                profit={tile.profit}
                profitRate={tile.profitRate}
            />
        {/each}
    </div>
</div>

<style>
    button {
        font-family: "SF Pro Display", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif !important;
    }

    div {
        font-family: "SF Pro Display", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif !important;
    }
</style>