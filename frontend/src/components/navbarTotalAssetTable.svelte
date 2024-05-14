<!-- components/navbarTotalAssetTable -->
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

    onMount(() => {
        navbarTotalAssetTableCountUp = new CountUp(
            totalAssetValueElement,
            $totalKRW.KRW,
            {
                duration: 1.5,
                separator: ",",
                decimal: ".",
                prefix: "₩",
                startVal: $totalKRW.KRW,
                plugin: new Odometer({
                    duration: 1.5,
                    lastDigitDelay: 0,
                }),
            }
        );
        navbarTotalAssetTableCountUp.start();

        // Subscribe to store changes to update countup
        totalKRW.subscribe(($totalKRW) => {
            navbarTotalAssetTableCountUp.update($totalKRW.KRW);
        });

        fetchAssetDataAndUpdateIntervalId = setInterval(() => {
            sessionValidityCheck();
            fetchDataAndUpdate();
        }, 1000);

        // Fetch data every 1 second
        navbarTotalAssetTableSetIntervalId = setInterval(() => {
            navbarTotalAssetTableCountUp.update($totalKRW.KRW);
        }, 500);
    });
    
    onDestroy(() => {
        navbarTotalAssetTableCountUp.reset();
        clearInterval(fetchAssetDataAndUpdateIntervalId);
        clearInterval(navbarTotalAssetTableSetIntervalId);
    });
</script>

<div class="bg-white rounded-lg shadow pl-2 pr-2 py-2 flex flex-col items-center">
    <p class="text-gray-700 text-sm mb-1">Total Asset Value</p>
    <div
        class="text-gray-800 text-lg font-semibold xl"
        bind:this={totalAssetValueElement}
    ></div>
</div>