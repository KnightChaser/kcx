// routes/exchange/functions/buyCryptocurrency.js
// Purchase cryptocurrency

import axios from 'axios';
import { auth } from '../../../stores/auth';

const token = auth.getToken();
const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

export async function buyCryptocurrency(marketCode, amount) {

    try {
        const response = await axios.post(`${BACKEND_API_URL}/exchange/trade/buy`, 
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
        console.error('Failed to buy cryptocurrency', error);
        throw error;
    }
}
