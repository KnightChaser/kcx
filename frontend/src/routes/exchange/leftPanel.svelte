<!-- Left Panel -->
        <div class="col-span-2 bg-white p-4 rounded border border-gray-400">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">Markets</h2>
            <ul class="space-y-2">
                {#each marketData as market}
                    <button 
                        class="cursor-pointer"
                        class:text-red-500={market.change === 'FALL'}
                        class:text-green-500={market.change === 'RISE'}
                        on:click={() => {
                            selectedMarket = market;
                            selectedMarketCodeUnit = market.market.split('-')[1].toUpperCase();
                        }}
                    >
                        {market.market.replace('KRW-', '')} {market.change === 'FALL' ? '-' : '+'}{(market.change_rate * 100).toFixed(2)}%
                    </button>
                {/each}
            </ul>
        </div>
