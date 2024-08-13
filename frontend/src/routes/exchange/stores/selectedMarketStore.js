// frontend/src/routes/exchange/stores/selectedMarketStore.js
import { writable } from 'svelte/store';

export const selectedMarketCode = writable('KRW-BTC');  // Initialize with a default value
