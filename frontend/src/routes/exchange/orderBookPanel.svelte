<script>
    export let selectedMarket;
</script>

<div class="bg-white h-full rounded border border-gray-400">
    {#if selectedMarket}
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Order Book</h2>
        <!-- Add your order book content here -->
        <div>
            <p class="text-gray-500">Order book content for {selectedMarket.market}</p>
            <!-- This is just a placeholder; replace with actual order book data -->
        </div>
    {:else}
        <p class="text-center text-gray-500">Loading...</p>
    {/if}
</div>
