<!-- frontend/src/routes/components/totalAssetTable.svelte -->
<!-- Show the entire asset estimation in KRW and BTC -->
<script>
    import { onDestroy, onMount } from 'svelte';
    import { totalKRW } from '../../../stores/usesrAssets';

    export let totalAssetKRWTargetElement;
    export let totalAssetBTCTargetElement;

    let calculateAssetValueInKRWIntervalId;

    // Every 500ms, update the total asset value
    onMount(() => {
        // Update the values immediately
        updateValues();

        // React to store updates
        totalKRW.subscribe($totalKRW => {
            updateValues();
        });

        // Every 500ms, update the total asset value
        calculateAssetValueInKRWIntervalId = setInterval(() => {
            updateValues();
        }, 500);
    });

    // Cleanup
    onDestroy(() => {
        clearInterval(calculateAssetValueInKRWIntervalId);
    });

    function updateValues() {
        if (totalAssetKRWTargetElement) {
            totalAssetKRWTargetElement.innerText = formatCurrency($totalKRW.KRW);
        }
        if (totalAssetBTCTargetElement) {
            totalAssetBTCTargetElement.innerText = formatBTC($totalKRW.BTC);
        }
    }

    function formatCurrency(value) {
        return Math.round(value).toLocaleString();
    }

    function formatBTC(value) {
        return value.toFixed(8);
    }
</script>

<div class="flex flex-col justify-between pt-8 pb-2 px-4 mb-8 border rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 asset-table w-full">
    <h2 class="text-2xl font-bold">Total Asset</h2>
    <div class="flex justify-between items-end">
        <div class="flex-1"></div>
        <div class="text-right">
            <p class="text-2xl mb-1">
                <b bind:this={totalAssetKRWTargetElement}></b> KRW
            </p>
            <p class="text-sm text-blue-500">
                ≈ <b bind:this={totalAssetBTCTargetElement}></b> BTC
            </p>
        </div>
    </div>
</div>
