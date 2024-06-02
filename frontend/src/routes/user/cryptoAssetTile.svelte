<!-- routes/user/CryptoAssetTile.svelte -->
<script>
    export let assetName;
    export let amount;
    export let averageUnitPrice;
</script>

<div class="border p-4 rounded-lg shadow-md">
    <h3 class="text-lg font-semibold">{assetName}</h3>
    <p>Amount: {amount}</p>
    <p>Avg. Unit Price: {averageUnitPrice}</p>
</div>
