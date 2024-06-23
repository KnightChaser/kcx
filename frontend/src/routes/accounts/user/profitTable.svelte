<!-- frontend/src/routes/accounts/user/profiltTable.svelte  -->
<script>
    import { onDestroy, onMount } from 'svelte';

    export let totalProfit;
    export let totalProfitRate;
    export let totalProfitKRWTargetElement;
    export let totalProfitRateTargetElement;

    let calculateProfitValueIntervalId;

    // Every 500ms, update the total profit value
    onMount(() => {
        // Update the values immediately
        updateValues();

        // Every 500ms, update the total profit value
        calculateProfitValueIntervalId = setInterval(() => {
            updateValues();
        }, 500);
    });

    // Cleanup
    onDestroy(() => {
        clearInterval(calculateProfitValueIntervalId);
    });

    function updateValues() {
        if (totalProfitKRWTargetElement) {
            totalProfitKRWTargetElement.innerText = formatCurrency(totalProfit);
        }
        if (totalProfitRateTargetElement) {
            totalProfitRateTargetElement.innerText = totalProfitRate.toFixed(3);
        }
    }

    // Function to format the number with localization
    function formatCurrency(value) {
        return new Intl.NumberFormat('ko-KR', {
            style: 'currency',
            currency: 'KRW',
            minimumFractionDigits: 0
        }).format(value);
    }
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
