// userAssets.js
import { writable } from 'svelte/store';

// Define the structure of the user's asset information
export const balances = writable({
    KRW:        { amount: 0, estimatedValue: 0, fullname: "South Korean Won" },        // fiat currency
    AAVE:       { amount: 0, estimatedValue: 0, fullname: "Aave" },                   // cryptocurrency
    ADA:        { amount: 0, estimatedValue: 0, fullname: "Cardano" },
    AVAX:       { amount: 0, estimatedValue: 0, fullname: "Avalanche" },
    BAT:        { amount: 0, estimatedValue: 0, fullname: "Basic Attention Token" },
    BCH:        { amount: 0, estimatedValue: 0, fullname: "Bitcoin Cash" },
    BTC:        { amount: 0, estimatedValue: 0, fullname: "Bitcoin" },
    BTG:        { amount: 0, estimatedValue: 0, fullname: "Bitcoin Gold" },
    BTT:        { amount: 0, estimatedValue: 0, fullname: "BitTorrent" },
    DOT:        { amount: 0, estimatedValue: 0, fullname: "Polkadot" },
    EOS:        { amount: 0, estimatedValue: 0, fullname: "EOS" },
    ETC:        { amount: 0, estimatedValue: 0, fullname: "Ethereum Classic" },
    ETH:        { amount: 0, estimatedValue: 0, fullname: "Ethereum" },
    HBAR:       { amount: 0, estimatedValue: 0, fullname: "Hedera Hashgraph" },
    LINK:       { amount: 0, estimatedValue: 0, fullname: "Chainlink" },
    MANA:       { amount: 0, estimatedValue: 0, fullname: "Decentraland" },
    MATIC:      { amount: 0, estimatedValue: 0, fullname: "Polygon" },
    NEAR:       { amount: 0, estimatedValue: 0, fullname: "NEAR Protocol" },
    NEO:        { amount: 0, estimatedValue: 0, fullname: "NEO" },
    ONT:        { amount: 0, estimatedValue: 0, fullname: "Ontology" },
    QTUM:       { amount: 0, estimatedValue: 0, fullname: "Quantum" },
    SAND:       { amount: 0, estimatedValue: 0, fullname: "Sandbox" },
    SBD:        { amount: 0, estimatedValue: 0, fullname: "Steem Dollars" },
    SC:         { amount: 0, estimatedValue: 0, fullname: "Siacoin" },
    SHIB:       { amount: 0, estimatedValue: 0, fullname: "Shiba Inu" },
    SOL:        { amount: 0, estimatedValue: 0, fullname: "Solana" },
    STORJ:      { amount: 0, estimatedValue: 0, fullname: "Storage" },
    STRAX:      { amount: 0, estimatedValue: 0, fullname: "Stratis" },
    SUI:        { amount: 0, estimatedValue: 0, fullname: "Sui" },
    TFUEL:      { amount: 0, estimatedValue: 0, fullname: "Theta Fuel" },
    THETA:      { amount: 0, estimatedValue: 0, fullname: "Theta Token" },
    TRX:        { amount: 0, estimatedValue: 0, fullname: "TRON" },
    VET:        { amount: 0, estimatedValue: 0, fullname: "VeChain" },
    WAVES:      { amount: 0, estimatedValue: 0, fullname: "Waves" },
    XEC:        { amount: 0, estimatedValue: 0, fullname: "eCash" },
    XEM:        { amount: 0, estimatedValue: 0, fullname: "NEM" },
    XLM:        { amount: 0, estimatedValue: 0, fullname: "Stellar Lumen" },
    XRP:        { amount: 0, estimatedValue: 0, fullname: "Ripple" },
    XTZ:        { amount: 0, estimatedValue: 0, fullname: "Tezos" },
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
