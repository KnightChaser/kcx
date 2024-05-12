// utils/fetchAssetDataAndUpdate.js

import Swal from "sweetalert2";
import { push } from "svelte-spa-router";
import { getBalance, calculateAssetValueInKRW } from "./userAssets";

export async function fetchDataAndUpdate() {
    try {
        await getBalance();                     // This will automatically update the balances store
        await calculateAssetValueInKRW();       // This updates totalKRW and recalculates estimated values
    } catch (error) {
        Swal.fire({
            title: "Error",
            text: error.message,
            icon: "error",
            confirmButtonText: "OK",
        });
        push("/login");                         // Redirect to login page
    }
}
