// utils/userAssets.js
// Handling user assets (balances and total asset value) in a separate file

import { get } from "svelte/store";
import { totalKRW } from "../stores/usesrAssets";
import { push } from "svelte-spa-router";
import { balances } from "../stores/usesrAssets";
import Swal from "sweetalert2";
import axios from "axios";

const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

// Fetch user's asset information from the backend
export async function getBalance() {
    try {
        const response = await axios(`${BACKEND_API_URL}/account/balance`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
        });

        if (response.status !== 200) 
            throw new Error("Failed to fetch balances");

        // Update the balances store with the fetched data
        const data = response.data;

        // Remove any existing data whose keys ends with "_average_unit_price"
        // It's not an asset, it's just an average unit price
        for (const key in data) {
            if (key.endsWith("_average_unit_price")) {
                delete data[key];
            }
        }

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

// Fetch ticker information from UpBit OpenAPI
async function getTickerInformation(marketCodeListString) {
    const response = await axios(
        `https://api.upbit.com/v1/ticker?markets=${marketCodeListString}`
    )
    if (response.status !== 200) {
        Swal.fire({
            title: "Error",
            text: "Failed to get ticker information from UpBit OpenAPI",
            icon: "error",
            confirmButtonText: "OK",
        });
        return [];
    }

    return response.data;
}

// Calculate the estimated asset value in KRW
// Executed after fetching the balance information
export async function calculateAssetValueInKRW() {
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

// Return the current Bitcoin price in KRW (Only returns the price)
async function getBTCPriceInKRW() {
    const response = await axios(
        "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    );
    
    if (response.status !== 200) {
        Swal.fire({
            title: "Error",
            text: "Failed to get BTC price from UpBit OpenAPI",
            icon: "error",
            confirmButtonText: "OK",
        });
        return 0;
    }

    return response.data[0].trade_price;
}
