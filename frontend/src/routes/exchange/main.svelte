<!-- routes/exchange/main.svelte (exchange main) -->

<script>
    import Router from 'svelte-spa-router';
</script>

<main class="h-screen bg-gray-100 font-sans">
    <!-- Content -->
    <div class="grid grid-cols-12 gap-4 p-4">
        <!-- Left Panel -->
        <div class="col-span-2 bg-white p-4 rounded border border-gray-400">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">Markets</h2>
            <ul class="space-y-2">
                <li class="text-red-500 hover:text-red-700 cursor-pointer">BTC -0.33%</li>
                <li class="text-red-500 hover:text-red-700 cursor-pointer">ETH -1.22%</li>
                <li class="text-green-500 hover:text-green-700 cursor-pointer">XRP +0.95%</li>
                <!-- Add more market items here -->
            </ul>
        </div>

        <!-- Center Panel -->
        <div class="col-span-7 bg-white p-4 rounded border border-gray-400">
            <div class="flex justify-between items-center mb-4">
                <div class="flex items-center space-x-2">
                    <img src="src/assets/currency_logo/btc_logo.png" alt="Market Icon" class="h-6 w-6 rounded-full">
                    <h2 class="text-2xl font-semibold text-gray-800">BTC</h2>
                    <h2 class="text-2xl font-semibold text-gray-800">(Bitcoin)</h2>
                </div>
                <div class="space-y-1 text-right">
                    <span class="text-2xl block text-gray-800">36,689,120 KRW</span>
                    <span class="text-red-500 block">-241,130 -0.65%</span>
                </div>
            </div>

            <!-- Info Panel -->
            <div class="p-2 rounded mb-4 border border-gray-400">
                <div class="grid grid-cols-3 gap-4 text-center">
                    <div>
                        <p class="text-sm text-gray-500">24h High</p>
                        <p class="text-lg font-semibold text-gray-800">37,462,790 KRW</p>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500">24h Low</p>
                        <p class="text-lg font-semibold text-gray-800">35,500,000 KRW</p>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500">24h Volume (KRW)</p>
                        <p class="text-lg font-semibold text-gray-800">20,457,354,710 KRW</p>
                    </div>
                </div>
            </div>

            <!-- Trading Chart Area -->
            <div class="p-4 rounded h-80 border border-gray-400 bg-white">
                <p class="text-center text-gray-500">Trading chart here</p>
            </div>
        </div>

        <!-- Right Panel -->
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
                        <label class="block text-sm text-gray-700">Available Balance</label>
                        <p class="text-lg font-semibold text-gray-800">1,000,000 KRW</p>
                    </div>
                    <div class="space-y-2">
                        <label class="block text-sm text-gray-700">Available BTC</label>
                        <p class="text-lg font-semibold text-gray-800">0.5 BTC</p>
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
    </div>
</main>

<style>
    main {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
