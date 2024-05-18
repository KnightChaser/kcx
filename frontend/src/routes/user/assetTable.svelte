<!-- routes/user/assetTable.js  -->
<!-- Getting the asset table per asset -->

<script>
    import { balances } from "../../stores/usesrAssets"; 
    import { formatAmount } from "../../utils/formatAmount.js";
</script>

<div class="overflow-x-auto w-full">
    <table class="min-w-full">
        <thead class="bg-gray-50">
            <tr class="text-left">
                <th class="px-4 py-2 whitespace-nowrap">Assets</th>
                <th class="px-4 py-2 text-right whitespace-nowrap">Symbol</th>
                <th class="px-4 py-2 text-right whitespace-nowrap">Amount</th>
                <th class="px-4 py-2 text-right whitespace-nowrap">Value</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {#each Object.entries($balances) as [currency, { amount, estimatedValue, fullname }]}
                <tr class="border-t">
                    <td class="px-4 py-2 flex items-center whitespace-nowrap">
                        <img src="/src/assets/currency_logo/{currency.toLowerCase()}_logo.png" alt="{currency} logo" class="h-8 w-8 mr-3" />
                        <span class="truncate">{fullname}</span>
                    </td>
                    <td class="px-4 py-2 text-right whitespace-nowrap">{currency}</td>
                    <td class="px-4 py-2 text-right whitespace-nowrap">
                        {@html formatAmount(amount)}
                    </td>
                    <td class="px-4 py-2 text-right whitespace-nowrap">
                        {#if currency !== "KRW"}
                            <p class="text-sm text-blue-500">
                                ≈ <b>{Math.round(estimatedValue).toLocaleString()}</b> KRW
                            </p>
                        {/if}
                    </td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>
