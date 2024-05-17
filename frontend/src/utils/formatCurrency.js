export function formatCurrency(value) {
    if (value >= 1000)
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value);
    if (value >= 100)
        // With one decimal places
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW', minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(value);
    if (value >= 1)
        // With two decimal places
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value);
    else
        // With four decimal places
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW', minimumFractionDigits: 4, maximumFractionDigits: 4 }).format(value);
}
