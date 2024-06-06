// routes/exchange/functions/sellCryptocurrency.js

import { formatCurrency } from '../../../utils/formatCurrency';
import { buyCryptocurrency } from './buycryptocurrency';
import { sellCryptocurrency } from './sellCryptocurrency';
import Swal from 'sweetalert2';

// Helper function to limit decimal points
const formatCryptoAmount = (amount) => {
    return parseFloat(amount).toFixed(6);
};

const formatKRWAmount = (amount) => {
    return Math.floor(amount).toLocaleString();
};

export const handleBuy = async (selectedMarketCodeUnit, size, currentPrice) => {
    try {
        if (isNaN(size) || size === 0) {
            Swal.fire('Error', 'Size must be a non-zero number', 'error');
            return;
        }

        const response = await buyCryptocurrency(selectedMarketCodeUnit, size);
        if (response.status === 200) {
            Swal.fire({
                title: 'Success',
                html: `<div style="font-family: 'SF Pro Display';">
                          Successfully bought the cryptocurrency<br>
                          Bought: <strong>${formatCryptoAmount(response.data.amount)} ${selectedMarketCodeUnit}</strong><br>
                          Price: <strong>${formatKRWAmount(response.data.price)} KRW</strong><br>
                          Total cost: <strong>${formatKRWAmount(response.data.total_price)} KRW</strong><br>
                          Fee: <strong>${formatKRWAmount(response.data.fee)} KRW</strong>
                       </div>`,
                icon: 'success',
                showCancelButton: true,
                confirmButtonText: 'OK',
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
            });
        }
    } catch (error) {
        Swal.fire({
            title: 'Error',
            text: 'Failed to buy the cryptocurrency. Check your balance and try again.',
            icon: 'error',
            confirmButtonText: 'OK',
            confirmButtonColor: '#3085d6',
        });
    }
};

export const handleSell = async (selectedMarketCodeUnit, size, currentPrice) => {
    try {
        if (isNaN(size) || size === 0) {
            Swal.fire('Error', 'Size must be a non-zero number', 'error');
            return;
        }

        const response = await sellCryptocurrency(selectedMarketCodeUnit, size);
        if (response.status === 200) {
            Swal.fire({
                title: 'Success',
                html: `<div style="font-family: 'SF Pro Display';">
                          Successfully sold the cryptocurrency<br>
                          Sold: <strong>${formatCryptoAmount(response.data.amount)} ${selectedMarketCodeUnit}</strong><br>
                          Price: <strong>${formatKRWAmount(response.data.price)} KRW</strong><br>
                          Total: <strong>${formatKRWAmount(response.data.total_price)} KRW</strong><br>
                          Fee: <strong>${formatKRWAmount(response.data.fee)} KRW</strong>
                       </div>`,
                icon: 'success',
                showCancelButton: true,
                confirmButtonText: 'OK',
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
            });
        }
    } catch (error) {
        Swal.fire({
            title: 'Error',
            text: 'Failed to sell the cryptocurrency. Check your balance and try again.',
            icon: 'error',
            confirmButtonText: 'OK',
            confirmButtonColor: '#3085d6',
        });
    }
};
