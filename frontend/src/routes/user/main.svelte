<!-- user/main.svelte -->

<script>
    import { onMount, onDestroy } from 'svelte';
    import { get } from 'svelte/store';
    import Swal from 'sweetalert2';
    import { push } from 'svelte-spa-router';
    import { balances, totalKRW, updateBalances, updateTotalKRW } from '../../stores/usesrAssets';
    import { CountUp } from "countup.js";
    import { Odometer } from 'odometer_countup';

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    const username = localStorage.getItem('username');

    // Fetch user's asset information from the backend
    async function getBalance() {
        try {
            const response = await fetch(`${BACKEND_API_URL}/account/balance`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            });
            if (!response.ok) throw new Error("Failed to fetch balances");

            // Update the balances store with the fetched data
            const data = await response.json();
            balances.update((b) => {
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

    // Calculate the estimated asset value in KRW
    // Executed after fetching the balance information
    async function calculateAssetValueInKRW() {
        const localBalances = get(balances); // Get a snapshot of the current state
        const marketCodeList = Object.keys(localBalances)
            .filter((currency) => currency !== "KRW")
            .map((currency) => `KRW-${currency}`)
            .join(",");

        const tickerInformation = await getTickerInformation(marketCodeList);

        // Total asset value in KRW; First, add the KRW balance
        totalKRW.update((b) => {
            b.KRW = localBalances.KRW.amount;
            return b;
        });

        // Update the balances store with the estimated value
        balances.update((b) => {
            tickerInformation.forEach((ticker) => {
                const currency = ticker.market.split("-")[1]; // "ETH-KRW" -> "ETH"
                const estimatedValue =
                    parseFloat(ticker.trade_price) * b[currency].amount;
                b[currency].estimatedValue = estimatedValue;

                // Add the estimated value to the total asset value in KRW
                totalKRW.update((b) => {
                    b.KRW += estimatedValue;
                    return b;
                });
            });
            return b;
        });

        // Calculate the BTC equivalent of the total asset value in KRW
        let btcPriceInKRW = await getBTCPriceInKRW();
        totalKRW.update((b) => {
            b.BTC = b.KRW / btcPriceInKRW;
            return b;
        });
    }

    // Fetch ticker information from UpBit OpenAPI
    async function getTickerInformation(marketCodeListString) {
        const response = await fetch(
            `https://api.upbit.com/v1/ticker?markets=${marketCodeListString}`
        );
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
        const response = await fetch(
            "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
        );
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

    // This function wraps the call to getBalance and calculateAssetValueInKRW with error handling
    async function fetchDataAndUpdate() {
        try {
            await getBalance();  // This will automatically update the balances store
            await calculateAssetValueInKRW();  // This needs to be implemented in assetUtils.js based on your app's logic
        } catch (error) {
            Swal.fire({
                title: 'Error',
                text: error.message,
                icon: 'error',
                confirmButtonText: 'OK',
            });
            push('/login');
        }
    }

    let totalAssetKRWTargetElement;
    let totalAssetKRWCountUp;
    let totalAssetBTCTargetElement;
    let totalAssetBTCCountUp;
    let getBalanaceIntervalId;
    let calculateAssetValueInKRWIntervalId;

    onMount(async () => {
        getBalance();
        calculateAssetValueInKRW();

        // Initialize the CountUp instances for total asset value in KRW and BTC
        totalAssetKRWCountUp = new CountUp(
            totalAssetKRWTargetElement,
            get(totalKRW).KRW,
            {
                duration: 1.5,
                separator: ",",
                decimal: ".",
                startVal: get(totalKRW).KRW,
                plugin: new Odometer({
                    duration: 1.5,
                    lastDigitDelay: 0
                })
            },
        );

        totalAssetBTCCountUp = new CountUp(
            totalAssetBTCTargetElement,
            get(totalKRW).BTC,
            {
                duration: 1.0,
                separator: ",",
                decimal: ".",
                decimalPlaces: 8,
                startVal: get(totalKRW).BTC,
                plugin: new Odometer({
                    duration: 1.0,
                    lastDigitDelay: 0
                })
            },
        );
        
        // Start the initial animation
        totalAssetKRWCountUp.start();
        
        // Subscribe to totalKRW changes
        totalKRW.subscribe(($totalKRW) => {
            if (
                totalAssetKRWCountUp &&
                $totalKRW.KRW !== totalAssetKRWCountUp.endVal
            ) {
                totalAssetKRWCountUp.update($totalKRW.KRW);
            }

            if (
                totalAssetBTCCountUp &&
                $totalKRW.BTC !== totalAssetBTCCountUp.endVal
            ) {
                totalAssetBTCCountUp.update($totalKRW.BTC);
            }
        });

        // Update the balances store with the fetched data every second
        getBalanaceIntervalId = setInterval(getBalance, 500);
        calculateAssetValueInKRWIntervalId = setInterval(calculateAssetValueInKRW, 500);
    });

    // If the user moves another page, clear the interval
    // So that the interval does not continue to run in the background, even though the user logs out
    onDestroy(() => {
        clearInterval(getBalanaceIntervalId);
        clearInterval(calculateAssetValueInKRWIntervalId);
    });

</script>

<main class="p-6">
    <h1 class="text-2xl mb-6"><b>{username}</b>'s assets</h1>

    <!-- Total asset component or markup -->
    <div class="flex flex-col justify-between pt-8 pb-2 px-4 mb-8 border rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
        <h2 class="text-2xl font-bold">Total Asset</h2>
        <div class="flex justify-between items-end">
            <div class="flex-1"></div>
            <div class="text-right">
                <p class="text-2xl mb-1">
                    <b bind:this={totalAssetKRWTargetElement}>{$totalKRW.KRW}</b> KRW
                </p>
                <p class="text-sm text-blue-500">
                    ≈ <b bind:this={totalAssetBTCTargetElement}>{$totalKRW.BTC}</b> BTC
                </p>
            </div>
        </div>
    </div>

    <!-- Asset information per type as a table -->
    <div class="overflow-x-auto">
        <table class="min-w-full">
            <thead>
                <tr class="text-left">
                    <th class="px-4 py-2">Assets</th>
                    <th class="px-4 py-2 text-right">Amount</th>
                    <th class="px-4 py-2 text-right">Value</th>
                </tr>
            </thead>
            <tbody>
                {#each Object.entries($balances) as [currency, { amount, estimatedValue, fullname }]}
                    <tr class="border-t">
                        <td class="px-4 py-2 flex items-center">
                            <img src="/src/assets/currency_logo/{currency.toLowerCase()}_logo.png" alt="{currency} logo" class="h-8 w-8 mr-3"/>
                            <span>{fullname}</span>
                        </td>
                        <td class="px-4 py-2 text-right">{amount.toFixed(8)}</td>
                        <td class="px-4 py-2 text-right">
                            {#if currency !== "KRW"}
                                ≈ {estimatedValue.toLocaleString()} KRW
                            {/if}
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</main>

<style>
    /* Add your styles here */
</style>