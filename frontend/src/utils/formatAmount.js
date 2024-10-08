// frontend/src/utils/formatAmount.js

// Helper to format amounts with trailing zeros in gray
// Might be useful for displaying cryptocurrency amounts
export function formatAmount(currency, amount) {
    // Handle the case where currency is not provided
    if (amount === undefined) {
        amount = currency;
        currency = '';
    }
    
    let formatted = amount.toFixed(8).toLocaleString();
    let [main, decimals] = formatted.split(".");
    if (decimals) {
        let significant = decimals.replace(/0+$/, "");
        let zeros = decimals.slice(significant.length);
        return `${main}.<span style="color: gray;">${significant}</span><span style="color: lightgray;">${zeros}</span> ${currency}`;
    }
    return formatted + " " + currency;
}
