<!-- components/navbarTotalAssetTable.svelte -->
<script>
    import { onMount, onDestroy } from "svelte";
    import { sessionValidityCheck } from "../utils/sessionValidityCheck";
    import { totalKRW } from "../stores/usesrAssets";
    import { CountUp } from "countup.js";
    import { Odometer } from "odometer_countup";
    import { fetchDataAndUpdate } from "../utils/fetchAssetDataAndUpdate";

    let totalAssetValueElement;
    let navbarTotalAssetTableCountUp;
    let fetchAssetDataAndUpdateIntervalId;
    let navbarTotalAssetTableSetIntervalId;

    // There are possibilities that the total asset value is NaN due to 
    // the asynchronous nature of the fetchAssetDataAndUpdate function and other unpredictable reasons.
    // Therefore, we need to handle the case where the total asset value is NaN thoroughly.
    onMount(() => {
        try {
            navbarTotalAssetTableCountUp = new CountUp(
                totalAssetValueElement,
                $totalKRW.KRW,
                {
                    duration: 0.5,
                    separator: ",",
                    decimal: ".",
                    prefix: "₩",
                    startVal: $totalKRW.KRW,
                    plugin: new Odometer({
                        duration: 0.5,
                        lastDigitDelay: 0,
                    }),
                }
            );
            navbarTotalAssetTableCountUp.start();

            // Subscribe to store changes to update countup
            totalKRW.subscribe(($totalKRW) => {
                try {
                    if (isNaN($totalKRW.KRW)) {
                        throw new Error("Retrieved value is NaN");
                    }
                    navbarTotalAssetTableCountUp.update($totalKRW.KRW);
                } catch (error) {
                    console.error("Error updating total asset value:", error);
                }
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

            // Fetch data every 1 second
            navbarTotalAssetTableSetIntervalId = setInterval(() => {
                try {
                    if (isNaN($totalKRW.KRW)) {
                        throw new Error("Retrieved value is NaN");
                    }
                    // Prevent the total asset value from being NaN
                    navbarTotalAssetTableCountUp.update($totalKRW.KRW);
                } catch (error) {
                    // If error occurs, leave the log and continue refreshing
                    console.error("Error updating total asset value:", error);
                }
            }, 500);
        } catch (error) {
            console.error("Error initializing CountUp:", error);
        }
    });
    
    onDestroy(() => {
        try {
            navbarTotalAssetTableCountUp.reset();
            clearInterval(fetchAssetDataAndUpdateIntervalId);
            clearInterval(navbarTotalAssetTableSetIntervalId);
        } catch (error) {
            console.error("Error during component destruction:", error);
        }
    });
</script>

<div class="bg-white rounded-lg shadow pl-2 pr-2 py-2 flex flex-col items-center">
    <p class="text-gray-700 text-sm mb-1">Total Asset Value</p>
    <div
        class="text-gray-800 text-lg font-semibold xl"
        bind:this={totalAssetValueElement}
    ></div>
</div>
