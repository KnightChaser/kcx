// userAssets.js
import { writable } from 'svelte/store';

// Define the structure of the user's asset information
export const balances = writable({
    KRW: { amount: 0, estimatedValue: 0, fullname: "South Korean Won" },        // fiat currency
    ADA: { amount: 0, estimatedValue: 0, fullname: "Cardano" },
    AVAX: { amount: 0, estimatedValue: 0, fullname: "Avalanche" },
    BCH: { amount: 0, estimatedValue: 0, fullname: "Bitcoin Cash" },
    BTC: { amount: 0, estimatedValue: 0, fullname: "Bitcoin" },
    DOT: { amount: 0, estimatedValue: 0, fullname: "Polkadot" },
    ETC: { amount: 0, estimatedValue: 0, fullname: "Ethereum Classic" },
    ETH: { amount: 0, estimatedValue: 0, fullname: "Ethereum" },
    HBAR: { amount: 0, estimatedValue: 0, fullname: "Hedera Hashgraph" },
    LINK: { amount: 0, estimatedValue: 0, fullname: "Chainlink" },
    MATIC: { amount: 0, estimatedValue: 0, fullname: "Polygon" },
    NEAR: { amount: 0, estimatedValue: 0, fullname: "NEAR Protocol" },
    SHIB: { amount: 0, estimatedValue: 0, fullname: "Shiba Inu" },
    SOL: { amount: 0, estimatedValue: 0, fullname: "Solana" },
    TRX: { amount: 0, estimatedValue: 0, fullname: "TRON" },
    XEC: { amount: 0, estimatedValue: 0, fullname: "eCash" },
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
