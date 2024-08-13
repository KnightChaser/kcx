// frontend/src/utils/formatCurrency.js

export function formatCurrency(value) {
    if (Math.abs(value) >= 1000)
        // Without decimal places
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value);
    if (Math.abs(value) >= 100)
        // With one decimal places
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW', minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(value);
    if (Math.abs(value) >= 1)
        // With two decimal places
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value);
    else
        // With four decimal places
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW', minimumFractionDigits: 4, maximumFractionDigits: 4 }).format(value);
}
