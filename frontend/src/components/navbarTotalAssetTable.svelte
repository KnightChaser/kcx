<!-- frontend/src/components/navbarTotalAssetTable.svelte  -->

<script>
    import { onMount, onDestroy } from "svelte";
    import { totalKRW } from "../stores/usesrAssets";
    import { sessionValidityCheck } from "../utils/sessionValidityCheck";
    import { fetchDataAndUpdate } from "../utils/fetchAssetDataAndUpdate";

    let totalAssetValueElement;
    let fetchAssetDataAndUpdateIntervalId;

    onMount(() => {
        // Fetch data every 1 second
        fetchAssetDataAndUpdateIntervalId = setInterval(() => {
            try {
                sessionValidityCheck();
                fetchDataAndUpdate();
            } catch (error) {
                console.error("Error fetching data and updating:", error);
            }
        }, 1000);

        // Subscribe to store changes to update the displayed value
        totalKRW.subscribe($totalKRW => {
            if (!isNaN($totalKRW.KRW)) {
                totalAssetValueElement.innerText = formatCurrency($totalKRW.KRW);
            } else {
                console.error("Error: Retrieved value is NaN");
                fetchDataAndUpdate(); // Retry fetching data in case of NaN
            }
        });
    });

    onDestroy(() => {
        clearInterval(fetchAssetDataAndUpdateIntervalId);
    });

    // Function to format the number with localization
    function formatCurrency(value) {
        return new Intl.NumberFormat('ko-KR', {
            style: 'currency',
            currency: 'KRW',
            minimumFractionDigits: 0
        }).format(value);
    }
</script>

<div class="bg-white rounded-lg shadow pl-2 pr-2 py-2 flex flex-col items-center">
    <p class="text-gray-700 text-sm mb-1">Total Asset Value</p>
    <div class="text-gray-800 text-lg font-semibold xl" bind:this={totalAssetValueElement}></div>
</div>

<style>
    .bg-white {
        background: linear-gradient(145deg, #f8f8f8, #ffffff);
    }
</style>
