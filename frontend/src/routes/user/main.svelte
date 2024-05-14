<!-- user/main.svelte -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import { fetchDataAndUpdate } from '../../utils/fetchAssetDataAndUpdate.js';
    import TotalAssetTable from './totalAssetTable.svelte';
    import AssetTable from './assetTable.svelte';
    import Welcome from '../welcome.svelte';

    const username = localStorage.getItem('username');
    const uuid = localStorage.getItem('uuid');

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
    <div class="w-full max-w-2xl">
        <div class="flex flex-col items-center p-6 bg-white rounded-xl shadow-md space-y-4 mb-6" id="user_info_panel">
            <div class="text-center">
                <p class="text-2xl font-semibold text-gray-900">@{username}</p>
                <p class="text-sm text-gray-500">Your uuid (identifier): <code>{uuid}</code></p>
            </div>
        </div>
        <div id="asset_status" class="bg-white rounded-xl shadow-md p-6">
            <TotalAssetTable 
                totalAssetKRWTargetElement="#total-asset-krw" 
                totalAssetBTCTargetElement="#total-asset-btc"
            />
            <AssetTable />
        </div>
    </div>
</main>

<style>
    @font-face {
        font-family: "SF Mono";
        src: url("../../assets/SFMono-Regular.otf");
    }

    @font-face {
        font-family: "SF Pro Display";
        src: url("../../assets/SFProDisplay-Regular.otf");
    }

    #user_info_panel {
        font-family: "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }

    #asset_status {
        font-family: "SF Mono", "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>