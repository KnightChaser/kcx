<!-- components/totalAssetTable.svelte -->
<!-- Show the entire asset estimation in KRW and BTC -->
<script>
    import { onDestroy, onMount } from 'svelte';
    import { totalKRW } from '../stores/usesrAssets';
    import { CountUp } from "countup.js";
    import { Odometer } from 'odometer_countup';

    export let totalAssetKRWTargetElement;
    export let totalAssetBTCTargetElement;

    let totalAssetKRWCountUp;
    let totalAssetBTCCountUp;
    let calculateAssetValueInKRWIntervalId;

    // Every 500ms, update the total asset value
    onMount(() => {
        totalAssetKRWCountUp = new CountUp(totalAssetKRWTargetElement, $totalKRW.KRW, {
            duration: 1.5,
            separator: ",",
            decimal: ".",
            startVal: $totalKRW.KRW,
            plugin: new Odometer({
                duration: 1.5,
                lastDigitDelay: 0
            })
        });

        totalAssetBTCCountUp = new CountUp(totalAssetBTCTargetElement, $totalKRW.BTC, {
            duration: 1.0,
            separator: ",",
            decimal: ".",
            decimalPlaces: 8,
            startVal: $totalKRW.BTC,
            plugin: new Odometer({
                duration: 1.0,
                lastDigitDelay: 0
            })
        });

        totalAssetKRWCountUp.start();
        totalAssetBTCCountUp.start();

        // React to store updates
        totalKRW.subscribe(($totalKRW) => {
            totalAssetKRWCountUp.update($totalKRW.KRW);
            totalAssetBTCCountUp.update($totalKRW.BTC);
        });

        // Every 500ms, update the total asset value
        calculateAssetValueInKRWIntervalId = setInterval(() => {
            totalAssetKRWCountUp.update($totalKRW.KRW);
            totalAssetBTCCountUp.update($totalKRW.BTC);
        }, 500);
    });

    // Cleanup
    onDestroy(() => {
        clearInterval(calculateAssetValueInKRWIntervalId);
        totalAssetKRWCountUp.reset();
        totalAssetBTCCountUp.reset();
    });

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
