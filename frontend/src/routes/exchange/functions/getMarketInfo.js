// routes/exchange/functions/getMarketInfo.js
import axios from 'axios';
const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

// Get the list of markets
export const getMarketListInfo = async () => {
    try {
        const response = await axios.get(`${BACKEND_API_URL}/exchange/market/list`);
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

// Get the ticker information of the given markets
export const getAllAvailableMarketsInfo = async () => {
    const marketList = await getMarketListInfo();
    const markets = marketList.map((market) => `KRW-${market}`);
    const marketRequestString = markets.join(',');
    try {
        const response = await axios.request({
            url: `${BACKEND_API_URL}/exchange/market/ticker`,
            method: 'GET',
            params: { markets: marketRequestString }
        });
        return response.data;
    } catch (error) {
        console.error(error);
    }
}
