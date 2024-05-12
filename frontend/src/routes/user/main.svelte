<!-- user/main.svelte -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import { fetchDataAndUpdate } from '../../utils/fetchAssetDataAndUpdate.js';
    import TotalAssetTable from '../../components/totalAssetTable.svelte';
    import AssetTable from '../../components/assetTable.svelte';

    const username = localStorage.getItem('username');

    let fetchAssetDataAndUpdateIntervalId;
    onMount(() => {
        fetchDataAndUpdate();
        fetchAssetDataAndUpdateIntervalId = setInterval(fetchDataAndUpdate, 1000);   // Fetch data every 1 second
    });

    onDestroy(() => {
        clearInterval(fetchAssetDataAndUpdateIntervalId);
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