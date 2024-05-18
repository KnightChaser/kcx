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
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Market
                    </th>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Change
                    </th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                {#each marketData as market}
                    <tr 
                        class="cursor-pointer hover:bg-gray-100" 
                        on:click={() => handleClick(market)}
                    >
                        <td class="px-4 py-2 whitespace-nowrap flex items-center space-x-2">
                            <img src={`/src/assets/currency_logo/${market.market.replace('KRW-', '').toLowerCase()}_logo.png`} alt="Market Icon" class="h-6 w-6 rounded-full">
                            <span class="text-gray-900 font-medium">{market.market.replace('KRW-', '')}</span>
                        </td>
                        <td class="px-4 py-2 whitespace-nowrap font-semibold {market.signed_change_rate > 0 ? 'text-green-500' : 'text-red-500'}">
                            {market.signed_change_rate > 0 ? '+' : '-'}{formatChangeRate(market.change_rate)}%
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>

<style>
    table {
        width: 100%;
    }

    thead {
        background-color: #f9fafb;
    }

    tr:hover {
        background-color: #f7fafc;
    }

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #a0aec0;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-track {
        background-color: #edf2f7;
    }
</style>
