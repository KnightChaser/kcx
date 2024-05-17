<script>
    import { formatCurrency } from '../../utils/formatCurrency';
    import { balances } from '../../stores/usesrAssets';
    export let selectedMarketCodeUnit;
    export let availableBalance;

    $: krwBalance = $balances.KRW.amount;
</script>

<div class="col-span-3 bg-white p-4 rounded border border-gray-400 space-y-4">
    <div class="p-4 rounded border border-gray-400 bg-white">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Place Order</h2>
        <div class="space-y-4">
            <div class="space-y-2">
                <input type="text" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Target price (KRW)" aria-label="Target price (KRW)">
            </div>
            <div class="space-y-2">
                <input type="text" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Size" aria-label="Size">
            </div>
            <div class="space-y-2">
                <input type="text" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Take profit (KRW)" aria-label="Take profit (KRW)">
            </div>
            <div class="space-y-2">
                <input type="text" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Stop loss (KRW)" aria-label="Stop loss (KRW)">
            </div>
            <div class="space-y-2">
                <p class="block text-sm text-gray-700">Available Balance</p>
                <p class="text-lg font-semibold text-gray-800">{formatCurrency(krwBalance)}</p>
            </div>
            <div class="space-y-2">
                <p class="block text-sm text-gray-700">Available {selectedMarketCodeUnit}</p>
                <p class="text-lg font-semibold text-gray-800">{availableBalance} {selectedMarketCodeUnit}</p>
            </div>
            <div class="flex space-x-2">
                <button class="bg-blue-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500">BUY</button>
                <button class="bg-red-500 text-white w-full py-2 rounded hover:shadow-lg transition-shadow duration-300 focus:outline-none focus:ring-2 focus:ring-red-500">SELL</button>
            </div>
        </div>
    </div>

    <div class="p-4 rounded border border-gray-400 bg-white">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Your order history</h2>
        <p class="text-gray-500">Your order</p>
    </div>
</div>
