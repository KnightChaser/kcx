<!-- routes/user/assetTracking.svelte -->
<script>
    import { onMount } from 'svelte';
    import { push } from "svelte-spa-router";
    import { formatAmount } from '../../utils/formatAmount';
    import { formatCurrency } from '../../utils/formatCurrency';
    import { getAllAvailableMarketsInfo } from '../exchange/functions/getMarketInfo';
    import TotalAssetTable from './totalAssetTable.svelte';
    import CryptoAssetTile from './cryptoAssetTile.svelte';
    import axios from 'axios';
    import Swal from 'sweetalert2';

    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    let balanceData = {};
    let assetTiles = [];
    let error = null;

    onMount(async () => {
        // Fetch the user's balance
        try {
            const response = await axios.get(`${BACKEND_API_URL}/api/account/balance/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.status !== 200) {
                Swal.fire({
                    icon: 'error',
                    title: 'Failed to fetch balance',
                    text: 'Failed to fetch balance',
                });
                throw new Error('Failed to fetch balance');
            }
            
            balanceData = response.data;
            assetTiles = formatBalanceData(balanceData);
        } catch (err) {
            error = err.message;
            Swal.fire({
                icon: 'error',
                title: 'Failed to fetch balance',
                text: error,
            });
        }
    });

    function formatBalanceData(data) {
        return Object.keys(data).filter(key => !key.includes("_average_unit_price")).map(key => ({
            assetName: key,
            amount: data[key],
            averageUnitPrice: data[`${key}_average_unit_price`] || 0
        }));
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

    <TotalAssetTable 
        totalAssetKRWTargetElement="#total-asset-krw" 
        totalAssetBTCTargetElement="#total-asset-btc"
    />

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {#each assetTiles as tile}
            <CryptoAssetTile 
                assetName={tile.assetName}
                amount={tile.amount}
                averageUnitPrice={tile.averageUnitPrice}
            />
        {/each}
    </div>
</div>
