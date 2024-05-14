<!-- routes/user/main.svelte -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import { fetchDataAndUpdate } from '../../utils/fetchAssetDataAndUpdate.js';
    import UserInfoTable from './userInfoTable.svelte';
    import TotalAssetTable from './totalAssetTable.svelte';
    import AssetTable from './assetTable.svelte';

    let fetchAssetDataAndUpdateIntervalId;
    onMount(() => {
        fetchDataAndUpdate();
        fetchAssetDataAndUpdateIntervalId = setInterval(fetchDataAndUpdate, 1000); // Fetch data every 1 second
    });

    onDestroy(() => {
        clearInterval(fetchAssetDataAndUpdateIntervalId);
    });
</script>

<main class="p-6 min-h-screen flex flex-col items-center">
    <UserInfoTable />
    <div id="asset_status" class="w-full max-w-4xl bg-white rounded-xl shadow-md p-6">
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

    @font-face {
        font-family: "SF Pro Display";
        src: url("../../assets/SF-Pro-Display-Medium.otf");
    }


    #asset_status {
        font-family: "SF Mono", "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
        max-width: 90vw; /* Ensures the panel is responsive and does not exceed 90% of the viewport width */
        width: 100%; /* Ensures the panel takes full width available within its container */
    }
</style>
