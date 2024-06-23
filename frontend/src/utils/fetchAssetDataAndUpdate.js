// frontend/src/utils/fetchAssetDataAndUpdate.js

import { redirect } from "@sveltejs/kit"; 
import Swal from "sweetalert2";
import { getBalance, calculateAssetValueInKRW } from "./userAssets.js";

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
        redirect("/login");
    }
}
