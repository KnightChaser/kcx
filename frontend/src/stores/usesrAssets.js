// userAssets.js
import { writable } from 'svelte/store';

// Define the structure of the user's asset information
export const balances = writable({
    KRW: { amount: 0, estimatedValue: 0, fullname: "South Korean Won" },
    BTC: { amount: 0, estimatedValue: 0, fullname: "Bitcoin" },
    ETH: { amount: 0, estimatedValue: 0, fullname: "Ethereum" },
    XRP: { amount: 0, estimatedValue: 0, fullname: "Ripple" },
});

// Store for total asset value in KRW and its BTC equivalent
export const totalKRW = writable({
    KRW: 0,
    BTC: 0,
});

// This function updates the balances with new data from the API
export function updateBalances(data) {
    balances.update(currentBalances => {
        for (const [currency, amount] of Object.entries(data)) {
            if (currentBalances[currency]) {
                currentBalances[currency].amount = amount;
            } else {
                currentBalances[currency] = { amount, estimatedValue: 0, fullname: currency };
            }
        }
        return currentBalances;
    });
}

// This function updates the total asset values
export function updateTotalKRW(krw, btc = null) {
    totalKRW.update(currentValues => {
        currentValues.KRW = krw;
        if (btc !== null) {
            currentValues.BTC = btc;
        }
        return currentValues;
    });
}
