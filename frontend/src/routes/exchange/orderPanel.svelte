<!-- frontend/src/routes/exchange/orderPanel.svelte -->

<script>
    import { balances } from "../../stores/usesrAssets";
    import { formatCurrency } from "../../utils/formatCurrency";
    import { selectedMarketCode } from './stores/selectedMarketStore.js';
    import { derived } from 'svelte/store';
    import { handleBuy, handleSell } from "./functions/buySellHandler";

    export let availableBalance;
    export let currentPrice;

    let size = 0;
    let totalValue = 0;
    let sliderValue = 0;
    let mode = 'buy';  // Mode: 'buy' or 'sell'

    const selectedMarketCodeUnit = derived(selectedMarketCode, ($selectedMarketCode) => $selectedMarketCode.split('-')[1].toUpperCase());

    $: krwBalance = $balances.KRW.amount;

    const handleSliderChange = (event) => {
        sliderValue = event.target.value;
        calculateValues();
    };

    const handleSizeChange = (event) => {
        size = parseFloat(event.target.value.replace(/,/g, ''));
        totalValue = Math.floor(size * currentPrice);
        sliderValue = mode === 'buy' ? totalValue / krwBalance : size / availableBalance;
    };

    const handleTotalValueChange = (event) => {
        totalValue = parseFloat(event.target.value.replace(/,/g, ''));
        size = totalValue / currentPrice;
        sliderValue = mode === 'buy' ? totalValue / krwBalance : size / availableBalance;
    };

    const setPercentage = (percentage) => {
        sliderValue = percentage / 100;
        calculateValues();
    };

    const calculateValues = () => {
        if (mode === 'buy') {
            totalValue = Math.floor(sliderValue * krwBalance);
            size = totalValue / currentPrice;
        } else {
            size = sliderValue * availableBalance;
            totalValue = Math.floor(size * currentPrice);
        }
    };

    const switchMode = (newMode) => {
        mode = newMode;
        resetValues();
    };

    const resetValues = () => {
        sliderValue = 0;
        size = 0;
        totalValue = 0;
        calculateValues();
    };

    const formatWithCommas = (value) => {
        const parts = value.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        return parts.join(".");
    };
</script>

<div class="p-4 bg-white border-gray-300 space-y-4">
    <div class="p-4 rounded border border-gray-300 bg-white shadow-sm">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Place Order</h2>
        <div class="flex justify-center mb-4">
            <button on:click={() => switchMode('buy')} class={`px-4 py-2 rounded-l ${mode === 'buy' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>Buy</button>
            <button on:click={() => switchMode('sell')} class={`px-4 py-2 rounded-r ${mode === 'sell' ? 'bg-red-500 text-white' : 'bg-gray-200'}`}>Sell</button>
        </div>
        <div class="space-y-4">
            <div class="flex space-x-4">
                <div class="flex-1">
                    <label for="totalValue" class="block text-sm font-medium leading-6 text-gray-900">Total Value</label>
                    <div class="relative mt-2 rounded-md shadow-sm">
                        <input type="text" value={formatWithCommas(totalValue)} on:input={handleTotalValueChange} id="totalValue" class="block w-full text-right rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6" placeholder="0.00" />
                        <div class="absolute inset-y-0 right-0 flex items-center">
                            <span class="text-gray-500 sm:text-sm pr-3">KRW</span>
                        </div>
                    </div>
                </div>
                <div class="flex-1">
                    <label for="size" class="block text-sm font-medium leading-6 text-gray-900">Size</label>
                    <div class="relative mt-2 rounded-md shadow-sm">
                        <input type="text" value={formatWithCommas(size)} on:input={handleSizeChange} id="size" class="block w-full text-right rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6" placeholder="0.00">
                        <div class="absolute inset-y-0 right-0 flex items-center">
                            <span class="text-gray-500 sm:text-sm pr-3">{$selectedMarketCodeUnit}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <input type="range" min="0" max="1" step="0.01" bind:value={sliderValue} on:input={handleSliderChange} class="w-full">
                <div class="flex justify-between text-xs text-gray-500 mt-1">
                    <span>0%</span>
                    <span>10%</span>
                    <span>20%</span>
                    <span>30%</span>
                    <span>40%</span>
                    <span>50%</span>
                    <span>60%</span>
                    <span>70%</span>
                    <span>80%</span>
                    <span>90%</span>
                    <span>100%</span>
                </div>
            </div>
            <div class="flex justify-between space-x-2 mt-2">
                <button on:click={() => setPercentage(20)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">20%</button>
                <button on:click={() => setPercentage(40)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">40%</button>
                <button on:click={() => setPercentage(60)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">60%</button>
                <button on:click={() => setPercentage(80)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">80%</button>
                <button on:click={() => setPercentage(100)} class="w-1/5 py-2 bg-gray-200 rounded hover:bg-gray-300">100%</button>
            </div>
            <table class="w-full mt-4">
                <tbody class="divide-y divide-gray-200">
                    <tr>
                        <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Available Balance</td>
                        <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                            {formatWithCommas(Math.floor(krwBalance))} KRW 
                            <div class="text-sm text-gray-500">(≈ {formatWithCommas((krwBalance / currentPrice).toFixed(4))} {$selectedMarketCodeUnit})</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="px-4 py-2 text-sm font-medium text-gray-900 w-1/3">Available {$selectedMarketCodeUnit}</td>
                        <td class="px-4 py-2 text-sm text-right text-gray-900 font-semibold w-2/3">
                            {formatWithCommas(availableBalance.toFixed(4))} {$selectedMarketCodeUnit}
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="flex space-x-2">
                <button on:click={() => mode === 'buy' ? handleBuy($selectedMarketCodeUnit, size, currentPrice) : handleSell($selectedMarketCodeUnit, size, currentPrice)} class={`bg-${mode === 'buy' ? 'blue' : 'red'}-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-${mode === 'buy' ? 'blue' : 'red'}-500`}>Proceed Order</button>
            </div>
        </div>
    </div>
</div>
