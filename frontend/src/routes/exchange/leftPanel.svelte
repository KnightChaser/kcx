<script>
    export let marketData;
    export let setSelectedMarket;

    function handleClick(market) {
        setSelectedMarket(market);
    }

    function formatChangeRate(changeRate) {
        return (changeRate * 100).toFixed(2);
    }
</script>

<div class="bg-white p-4 rounded-lg shadow-md border border-gray-500 h-full w-full">
    <h2 class="text-xl font-semibold mb-4 text-gray-800">Markets</h2>
    <div class="overflow-y-auto max-h-full">
        <ul class="space-y-2">
            {#each marketData as market}
                <li>
                    <button
                        type="button"
                        class="flex items-center justify-between w-full p-3 bg-white rounded-md shadow-sm cursor-pointer hover:bg-gray-300"
                        on:click={() => handleClick(market)}
                    >
                        <div class="flex items-center space-x-2">
                            <img src={`/src/assets/currency_logo/${market.market.replace('KRW-', '').toLowerCase()}_logo.png`} alt="Market Icon" class="h-6 w-6 rounded-full">
                            <span class="text-gray-900 font-medium">{market.market.replace('KRW-', '')}</span>
                        </div>
                        <span class={`font-semibold ${market.change_rate > 0 ? 'text-green-500' : 'text-red-500'}`}>
                            {market.change_rate > 0 ? '+' : ''}{formatChangeRate(market.change_rate)}%
                        </span>
                    </button>
                </li>
            {/each}
        </ul>
    </div>
</div>

<style>
    ul::-webkit-scrollbar {
        width: 8px;
    }

    ul::-webkit-scrollbar-thumb {
        background-color: #a0aec0;
        border-radius: 4px;
    }

    ul::-webkit-scrollbar-track {
        background-color: #edf2f7;
    }

    .hover\\:bg-gray-100:hover {
        background-color: #f7fafc;
    }

    ul {
        display: flex;
        flex-direction: column;
        margin: 0;
        padding: 0;
    }

    li {
        list-style-type: none;
    }

    button:hover {
        background-color: #f7fafc;
    }
</style>
