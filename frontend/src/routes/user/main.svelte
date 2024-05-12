<!-- user/main.svelte -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import Swal from 'sweetalert2';
    import { push } from 'svelte-spa-router';
    import { getBalance, calculateAssetValueInKRW } from '../../utils/userAssets.js';
    import TotalAssetTable from '../../components/totalAssetTable.svelte';
    import AssetTable from '../../components/assetTable.svelte';

    const username = localStorage.getItem('username');

    async function fetchDataAndUpdate() {
        try {
            await getBalance();                     // This will automatically update the balances store
            await calculateAssetValueInKRW();       // This updates totalKRW and recalculates estimated values
        } catch (error) {
            Swal.fire({
                title: 'Error',
                text: error.message,
                icon: 'error',
                confirmButtonText: 'OK',
            });
            push('/login');                         // Redirect to login page
        }
    }

    let fetchDataAndUpdateIntervalId;
    onMount(() => {
        fetchDataAndUpdate();
        fetchDataAndUpdateIntervalId = setInterval(fetchDataAndUpdate, 1000);   // Fetch data every 1 second
    });

    onDestroy(() => {
        clearInterval(fetchDataAndUpdateIntervalId);
    });
</script>

<main class="p-6">
    <h1 class="text-2xl font-semibold mb-6 text-center" id="welcome_username">Welcome, {username}</h1> 
    <div id="asset_status">
        <TotalAssetTable 
            totalAssetKRWTargetElement="#total-asset-krw" 
            totalAssetBTCTargetElement="#total-asset-btc"
        />
        <AssetTable />
    </div>
</main>

<style>
    @font-face {
        font-family: "SF Mono";
        src: url("../../assets/SFMono-Regular.otf");
    }

    #welcome_username {
        font-family: "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }

    #asset_status {
        display: flex;
        flex-direction: column;
        align-items: center; 
        width: 100%; 
        max-width: 80vw;
        margin: 0 auto;
        font-family: "SF Mono", "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>