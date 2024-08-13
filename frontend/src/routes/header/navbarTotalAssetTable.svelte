<!-- components/navbarTotalAssetTable.svelte -->
<script>
    import { onMount, onDestroy } from "svelte";
    import { writable } from "svelte/store";
    import { totalKRW } from "../../stores/usesrAssets.js";
    import { sessionValidityCheck } from "../../utils/sessionValidityCheck.js";
    import { fetchDataAndUpdate } from "../../utils/fetchAssetDataAndUpdate.js";

    let totalAssetValueElement;
    let fetchAssetDataAndUpdateIntervalId;
    let navbarTotalAssetTableSetIntervalId;
    let localTotalKRW = writable(0);

    function updateTotalAssetValue(newVal) {
        if (isNaN(newVal)) {
            console.error("Error: Retrieved value is NaN");
            fetchDataAndUpdate(); // Retry fetching data in case of NaN (some error happened during fetching data)
        } else {
            localTotalKRW.set(newVal);
        }
    }

    onMount(() => {
        try {
            // Subscribe to store changes to update the value
            totalKRW.subscribe(($totalKRW) => {
                updateTotalAssetValue($totalKRW.KRW);
            });

            // Fetch data every 1 second
            fetchAssetDataAndUpdateIntervalId = setInterval(() => {
                try {
                    sessionValidityCheck();
                    fetchDataAndUpdate();
                } catch (error) {
                    console.error("Error fetching data and updating:", error);
                }
            }, 1000);

            // Update local store every 1 second
            navbarTotalAssetTableSetIntervalId = setInterval(() => {
                updateTotalAssetValue($totalKRW.KRW);
            }, 500);
        } catch (error) {
            console.error("Error during onMount:", error);
        }
    });

    onDestroy(() => {
        try {
            clearInterval(fetchAssetDataAndUpdateIntervalId);
            clearInterval(navbarTotalAssetTableSetIntervalId);
        } catch (error) {
            console.error("Error during component destruction:", error);
        }
    });
</script>

<div class="bg-white rounded-lg shadow pl-2 pr-2 py-2 flex flex-col items-center" id="navbar_total_asset_table">
    <p class="text-gray-700 text-sm mb-1 font-bold">Total Asset Value</p>
    <div class="text-gray-800 text-lg font-extrabold xl">
        ₩{Math.round($localTotalKRW).toLocaleString()}
    </div>
</div>

<style>
    .bg-white {
        background: linear-gradient(145deg, #f8f8f8, #ffffff);
    }
    .shadow {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    #navbar_total_asset_table {
        font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", monospace;
    }
</style>
