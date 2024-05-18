<!-- src/routes/exchange/rightPanel.svelte  -->

<script>
    import { formatCurrency } from '../../utils/formatCurrency';
    import { balances } from '../../stores/usesrAssets';
    import { handleBuy, handleSell } from './functions/buySellHandler';

    export let selectedMarketCodeUnit;
    export let availableBalance;
    export let currentPrice;

    let size = 0;
    let totalValue = 0;
    let sliderValue = 0;  // Slider value to bind with input

    // Get the user's KRW balance
    $: krwBalance = $balances.KRW.amount;
    $: totalValue = size * currentPrice;

    const handleSliderChange = (event) => {
        sliderValue = event.target.value;
        totalValue = sliderValue * krwBalance;
        size = totalValue / currentPrice;
    };

    const handleSizeChange = () => {
        totalValue = size * currentPrice;
        sliderValue = totalValue / krwBalance;
    };
</script>

<div class="col-span-3 bg-white p-4 border-gray-300 space-y-4">
    <div class="p-4 rounded border border-gray-300 bg-white shadow-sm">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Place Order</h2>
        <div class="space-y-4">
            <div>
                <label for="size" class="block text-sm font-medium leading-6 text-gray-900">Size</label>
                <div class="relative mt-2 rounded-md shadow-sm">
                    <input type="number" bind:value={size} on:input={handleSizeChange} id="size" class="block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6" placeholder="0.00">
                    <div class="absolute inset-y-0 right-0 flex items-center">
                        <span class="text-gray-500 sm:text-sm pr-3">{selectedMarketCodeUnit}</span>
                    </div>
                </div>
            </div>
            <div>
                <input type="range" min="0" max="1" step="0.2" bind:value={sliderValue} on:input={handleSliderChange} class="w-full">
                <div class="flex justify-between text-xs text-gray-500 mt-1">
                    <span>0%</span>
                    <span>20%</span>
                    <span>40%</span>
                    <span>60%</span>
                    <span>80%</span>
                    <span>100%</span>
                </div>
            </div>
            <table class="w-full">
                <tbody class="divide-y divide-gray-200">
                    <tr>
                        <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Total Value</td>
                        <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                            {formatCurrency(totalValue)} 
                            <div class="text-sm text-gray-500">({(totalValue / currentPrice).toFixed(4)} {selectedMarketCodeUnit})</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Available Balance</td>
                        <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                            {formatCurrency(krwBalance)} 
                            <div class="text-sm text-gray-500">({(krwBalance / currentPrice).toFixed(4)} {selectedMarketCodeUnit})</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Available {selectedMarketCodeUnit}</td>
                        <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                            {availableBalance.toFixed(4)} {selectedMarketCodeUnit}
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="flex space-x-2">
                <button on:click={() => handleBuy(selectedMarketCodeUnit, size, currentPrice)} class="bg-blue-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500">BUY</button>
                <button on:click={() => handleSell(selectedMarketCodeUnit, size, currentPrice)} class="bg-red-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-red-500">SELL</button>
            </div>
        </div>
    </div>

    <div class="p-4 rounded border border-gray-300 bg-white shadow-sm">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Your order history</h2>
        <p class="text-gray-500">Your order</p>
    </div>
</div>