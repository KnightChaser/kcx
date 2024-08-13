<!-- frontend/src/routes/accounts/user/cryptoAssetTile.svelte  -->

<script>
    export let assetName;
    export let amount;
    export let averageUnitPrice;
    export let currentPrice;
    export let profit;
    export let profitRate;

    import { formatAmount } from "../../../../utils/formatAmount";
    import { formatCurrency } from "../../../../utils/formatCurrency";

    function getAssetLogo(assetName) {
        return `/src/assets/currency_logo/${assetName.toLowerCase()}_logo.png`;
    }

    const assetLogo = getAssetLogo(assetName);
</script>

<div class="border p-4 rounded-lg shadow-md cryptoAssetTile">
    <div class="flex items-center mb-4">
        <img src={assetLogo} alt={assetName} class="w-8 h-8 mr-2" />
        <span class="text-2xl font-semibold align-middle">{assetName}</span>
    </div>
    <table class="w-full text-sm">
        <tr>
            <td class="pr-2 font-medium">Amount</td>
            <td class="text-right">{@html formatAmount(amount)}</td>
        </tr>
        <tr>
            <td class="pr-2 font-medium">Entry Price</td>
            <td class="text-right">{@html averageUnitPrice !== 0 ? formatCurrency(averageUnitPrice) : '-'}</td>
        </tr>
        <tr>
            <td class="pr-2 font-medium">Current Price</td>
            <td class="text-right">{@html currentPrice !== 0 ? formatCurrency(currentPrice) : '-'}</td>
        </tr>
        <tr>
            <td class="pr-2 font-medium">Profit</td>
            <td class="text-right">{@html profit !== 0 ? formatCurrency(profit) : '-'}<br>
                                        {profitRate !== 0 ? '(' + profitRate.toString() + '%)' : ''}
            </td>
        </tr>
    </table>
</div>

<style>
    .cryptoAssetTile {
        font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", monospace;
        background-color: #fcfcfc;
    }
    table {
        width: 100%;
    }
    td {
        padding: 2px 0;
    }
</style>
