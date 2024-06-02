<!-- routes/user/profitTable.svelte -->
<script>
    import { onDestroy, onMount } from 'svelte';
    import { CountUp } from "countup.js";
    import { Odometer } from 'odometer_countup';

    export let totalProfit;
    export let totalProfitRate;
    export let totalProfitKRWTargetElement;
    export let totalProfitRateTargetElement;

    let totalProfitKRWCountUp;
    let totalProfitRateCountUp;
    let calculateProfitValueIntervalId;

    // Every 500ms, update the total profit value
    onMount(() => {
        totalProfitKRWCountUp = new CountUp(totalProfitKRWTargetElement, totalProfit, {
            duration: 0.5,
            separator: ",",
            decimal: ".",
            startVal: totalProfit,
            plugin: new Odometer({
                duration: 0.5,
                lastDigitDelay: 0
            })
        });

        totalProfitRateCountUp = new CountUp(totalProfitRateTargetElement, totalProfitRate, {
            duration: 0.15,
            separator: ",",
            decimal: ".",
            decimalPlaces: 3,
            startVal: totalProfitRate,
            plugin: new Odometer({
                duration: 0.15,
                lastDigitDelay: 0
            })
        });

        totalProfitKRWCountUp.start();
        totalProfitRateCountUp.start();

        // Every 500ms, update the total profit value
        calculateProfitValueIntervalId = setInterval(() => {
            totalProfitKRWCountUp.update(totalProfit);
            totalProfitRateCountUp.update(totalProfitRate);
        }, 500);
    });

    // Cleanup
    onDestroy(() => {
        clearInterval(calculateProfitValueIntervalId);
        totalProfitKRWCountUp.reset();
        totalProfitRateCountUp.reset();
    });

</script>

<div class="flex flex-col justify-between pt-8 pb-2 px-4 mb-8 border rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 asset-table w-full">
    <h2 class="text-2xl font-bold">Total Profit</h2>
    <div class="flex justify-between items-end">
        <div class="flex-1"></div>
        <div class="text-right">
            <p class="text-2xl mb-1">
                <b bind:this={totalProfitKRWTargetElement}></b> KRW
            </p>
            <p class="text-lg text-blue-500">
                ≈ <b bind:this={totalProfitRateTargetElement}></b> %
            </p>
        </div>
    </div>
</div>
