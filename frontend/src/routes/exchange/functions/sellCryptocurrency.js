// routes/exchange/functions/sellCryptocurrency.js
// Sell cryptocurrency

import axios from 'axios';

const token = localStorage.getItem('token');
const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

export async function sellCryptocurrency(marketCode, amount) {

    try {
        const response = await axios.post(`${BACKEND_API_URL}/api/exchange/trade/sell`, 
            {
                market_code: marketCode,
                amount: amount
            },
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        return response;
    } catch (error) {
        console.error('Failed to sell cryptocurrency', error);
        throw error;
    }

}