<!-- frontend/src/routes/accounts/user/assetTracking/+page.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { formatAmount } from '../../../../utils/formatAmount';
    import { formatCurrency } from '../../../../utils/formatCurrency';
    import { getAllAvailableMarketsInfo } from '../../../exchange/functions/getMarketInfo';
    import { auth } from '../../../../stores/auth';
    import CryptoAssetTile from './cryptoAssetTile.svelte';
    import TotalAssetTable from '../totalAssetTable.svelte';
    import ProfitTable from '../profitTable.svelte';
    import axios from 'axios';
    import Swal from 'sweetalert2';
    import AssetTable from '../assetTable.svelte';

    // Get user information
    const username = auth.getUsername();
    const token = auth.getToken();
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    let balanceData = {};               // User's balance data
    let marketData = [];                // Market data
    let assetTiles = [];                // Asset tiles (each crypto asset)
    let totalProfit = 0;                // Total profit (sum of all profit amounts)
    let totalProfitRate = 0;            // Total profit rate (weighted average of profit rates)
    let error = null;

    let intervalId;

    // Fetch and calculate data on mount
    onMount(async () => {
        await fetchAndCalculateData();
        intervalId = setInterval(fetchAndCalculateData, 1000);
    });

    // Clear interval when the components are destroyed
    onDestroy(() => {
        clearInterval(intervalId);
    });

    // Fetch balance data and calculate profitability
    async function fetchAndCalculateData() {
        try {
            // Fetch balance data
            const balanceResponse = await axios.get(`${BACKEND_API_URL}/account/balance/`, {
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
            
            const newBalanceData = balanceResponse.data;
            const newAssetTiles = formatBalanceData(newBalanceData);

            // Fetch market data
            const newMarketData = await getAllAvailableMarketsInfo();

            // Calculate profitability
            const updatedAssetTiles = calculateProfitability(newAssetTiles, newMarketData);

            // Calculate total profit and profit rate
            const validAssets = updatedAssetTiles.filter(tile => tile.profit !== 'N/A' && tile.profit !== 0);               // Filter out assets with no profit
            const totalInvestment = validAssets.reduce((sum, tile) => sum + (tile.averageUnitPrice * tile.amount), 0);      // Calculate total investment
            const newTotalProfit = validAssets.reduce((sum, tile) => sum + parseFloat(tile.profit), 0);                     // Calculate total profit
            const newTotalProfitRate = (totalInvestment > 0) ? (newTotalProfit / totalInvestment) * 100 : 0;                // Calculate total profit rate

            // Update state only after calculations are complete
            // Ensuring that the state is updated only after all calculations are complete,
            // so that the UI is updated only once with the latest data (no flickering)
            balanceData = newBalanceData;
            marketData = newMarketData;
            assetTiles = updatedAssetTiles;
            totalProfit = newTotalProfit;
            totalProfitRate = newTotalProfitRate;
        } catch (err) {
            error = err.message;
            Swal.fire({
                icon: 'error',
                title: 'Failed to fetch data',
                text: error,
            });
        }
    }

    // It formats the balance data to be displayed in the asset tiles
    function formatBalanceData(data) {
        return Object.keys(data).filter(key => !key.includes("_average_unit_price")).map(key => ({
            assetName: key,
            amount: data[key],
            averageUnitPrice: data[`${key}_average_unit_price`] || 0
        }));
    }

    // Calculate profitability of each asset
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
                const profit = (currentPrice - asset.averageUnitPrice) * asset.amount;                  // Profit amount is the multiplication of the profit per unit and the amount
                const profitRate = ((currentPrice / asset.averageUnitPrice) * 100 - 100).toFixed(2);    // Profit rate is the percentage increase in the current price compared to the average unit price
                return {
                    ...asset,
                    currentPrice,
                    profit: profit.toFixed(0),
                    profitRate
                };
            } else {
                return {
                    ...asset,
                    currentPrice: asset.currentPrice || 0,
                    profit: asset.profit || 0,
                    profitRate: asset.profitRate || 0
                    // If there is no record, 0 is returned for the current price, profit, and profit rate
                };
            }
        });
    }
</script>

<div class="w-full max-w-6xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6">
    <div class="flex justify-between items-center">
        <h2 class="text-2xl font-semibold text-gray-900">Asset Tracking</h2>
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
    div {
        font-family: "SF Pro Display", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif !important;
    }
</style>
