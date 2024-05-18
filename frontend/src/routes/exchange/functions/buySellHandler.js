// routes/exchange/functions/sellCryptocurrency.js
// Handle buying and selling cryptocurrencies acccording to the user request to the backend server(FastAPI)

import { formatCurrency } from '../../../utils/formatCurrency';
import { buyCryptocurrency } from './buycryptocurrency';
import { sellCryptocurrency } from './sellCryptocurrency';
import Swal from 'sweetalert2';

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
                html: 'Successfully bought the cryptocurrency<br>' + 
                    'Bought: <strong>' + response.data.amount + ' ' + selectedMarketCodeUnit + '</strong><br>' +
                    'Price: <strong>' + formatCurrency(response.data.price) + '</strong><br>' +
                    'Total cost: <strong>' + formatCurrency(response.data.total_price) + '</strong><br>' +
                    'Fee: <strong>' + formatCurrency(response.data.fee) + '</strong>',
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
                html: 'Successfully sold the cryptocurrency<br>' + 
                    'Sold: <strong>' + response.data.amount + ' ' + selectedMarketCodeUnit + '</strong><br>' +
                    'Price: <strong>' + formatCurrency(response.data.price) + '</strong><br>' +
                    'Total: <strong>' + formatCurrency(response.data.total_price) + '</strong><br>' +
                    'Fee: <strong>' + formatCurrency(response.data.fee) + '</strong>',
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
