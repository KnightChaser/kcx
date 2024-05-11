<!-- user/main.svelte -->

<script>
    import { onMount } from "svelte";
    import { writable, get } from "svelte/store";
    import Swal from "sweetalert2";
    import { push } from "svelte-spa-router";
    import { NumberFlip } from "number-flip";

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    // Store for user's asset information
    const balances = writable({
        KRW: { amount: 0, estimatedValue: 0 },
        BTC: { amount: 0, estimatedValue: 0 },
        ETH: { amount: 0, estimatedValue: 0 },
        XRP: { amount: 0, estimatedValue: 0 },
    });

    // Store for total asset value in KRW
    const totalKRW = writable({
        KRW: 0,
        BTC: 0,     // BTC equivalent of the total asset value in KRW
    })
    const username = localStorage.getItem("username");

    // Fetch user's asset information from the backend
    async function getBalance() {
        try {
            const response = await fetch(`${BACKEND_API_URL}/account/balance`, {
                method: "GET",
                headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
            });
            if (!response.ok) throw new Error("Failed to fetch balances");

            // Update the balances store with the fetched data
            const data = await response.json();
            balances.update(b => {
                // Update the balances store with the fetched data
                for (const [currency, amount] of Object.entries(data)) {
                    if (b[currency]) {
                        b[currency].amount = amount;
                    } else {
                        b[currency] = { amount, estimatedValue: 0 }; // Initialize properly if not existing
                    }
                }
                return b;
            });
        } catch (error) {
            Swal.fire({
                title: "Error",
                text: error.message,
                icon: "error",
                confirmButtonText: "OK",
            });
            push("/login");
        }
    }

    // Fetch ticker information from UpBit OpenAPI
    async function getTickerInformation(marketCodeListString) {
        const response = await fetch(`https://api.upbit.com/v1/ticker?markets=${marketCodeListString}`);
        if (!response.ok) {
            Swal.fire({
                title: "Error",
                text: "Failed to get ticker information from UpBit OpenAPI",
                icon: "error",
                confirmButtonText: "OK",
            });
            return [];
        }
        return response.json();
    }

    // Return the current Bitcoin price in KRW (Only returns the price)
    async function getBTCPriceInKRW() {
        const response = await fetch("https://api.upbit.com/v1/ticker?markets=KRW-BTC");
        if (!response.ok) {
            Swal.fire({
                title: "Error",
                text: "Failed to get BTC price from UpBit OpenAPI",
                icon: "error",
                confirmButtonText: "OK",
            });
            return 0;
        }
        const data = await response.json();
        return data[0].trade_price;
    }

    // Calculate the estimated asset value in KRW
    // Executed after fetching the balance information
    async function calculateAssetValueInKRW() {
        const localBalances = get(balances); // Get a snapshot of the current state
        const marketCodeList = Object.keys(localBalances)
            .filter(currency => currency !== "KRW")
            .map(currency => `KRW-${currency}`)
            .join(",");

        const tickerInformation = await getTickerInformation(marketCodeList);

        // Total asset value in KRW; First, add the KRW balance
        totalKRW.update(b => {
            b.KRW = localBalances.KRW.amount;
            return b;
        });

        // Update the balances store with the estimated value
        balances.update(b => {
            tickerInformation.forEach(ticker => {
                const currency = ticker.market.split("-")[1];   // "ETH-KRW" -> "ETH"
                const estimatedValue = parseFloat(ticker.trade_price) * b[currency].amount;
                b[currency].estimatedValue = estimatedValue;

                // Add the estimated value to the total asset value in KRW
                totalKRW.update(b => {
                    b.KRW += estimatedValue;
                    return b;
                });
            });
            return b;
        });

        // Calculate the BTC equivalent of the total asset value in KRW
        let btcPriceInKRW = await getBTCPriceInKRW();
        totalKRW.update(b => {
            b.BTC = b.KRW / btcPriceInKRW;
            return b;
        });
    }

    onMount(async () => {
        getBalance();
        calculateAssetValueInKRW();

        // Update the balances store with the fetched data every second
        setInterval(getBalance, 500);
        setInterval(calculateAssetValueInKRW, 500);
    });
</script>

<style>
    main {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>

<main class="p-6">
    <h1 class="text-2xl mb-6"><b>{username}</b>'s asset</h1>

    <!-- Total asset panel -->
    <div class="flex flex-col justify-between pt-8 pb-2 px-4 mb-8 border rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
        <h2 class="text-2xl font-bold">Total Asset</h2>
        <div class="flex justify-between items-end">
            <div class="flex-1"></div> <!-- This is to push the text to the right -->
            <div class="text-right">
                <!-- Total asset value in KRW -->
                
                <!-- Total asset value in BTC -->
                <p class="text-sm text-blue-500">≈ <b>{$totalKRW.BTC.toFixed(8).toLocaleString()}</b> BTC</p>
            </div>
        </div>
    </div>

    <!-- Asset information per type -->
    <div class="flex items-center py-8 px-4 border rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {#each Object.entries($balances) as [currency, {amount, estimatedValue}]}
            <div class="flex flex-col p-3 border rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
                <!-- Image and title -->
                <div class="flex items-center mb-4">
                    <img src="/src/assets/currency_logo/{currency.toLowerCase()}_logo.png" alt="{currency} logo" class="h-8 w-8 mr-3">
                    <h4 class="font-semibold">{currency}</h4>
                </div>
                <!-- Asset amount -->
                <p class="text-lg mb-1 text-right">{currency === 'KRW' ? amount.toLocaleString() : amount.toLocaleString()} {currency}</p>
                <!-- Estimated value -->
                {#if currency !== 'KRW'}
                    <p class="text-sm text-blue-500 text-right">≈ <b>{Math.round(estimatedValue).toLocaleString()}</b> KRW</p>
                {/if}
            </div>
            {/each}
        </div>
    </div>
</main>