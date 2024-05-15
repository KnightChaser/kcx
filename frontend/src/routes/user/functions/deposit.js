// routes/user/functions/deposit.js
// Deposit money(KRW; fiat currency) to user's account as the given amount

import Swal from "sweetalert2";
import axios from "axios";

const token = localStorage.getItem("token");
const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

// Deposit money (KRW; fiat currency)
export async function depositKRW() {
    // Ask how much money to deposit (KRW)
    Swal.fire({
        title: "Deposit Money",
        text: "How much money do you want to deposit? (KRW)",
        input: "text",
        inputAttributes: {
            autocapitalize: "off",
        },
        showCancelButton: true,
        confirmButtonText: "Deposit",
        showLoaderOnConfirm: true,
        preConfirm: async (KRW) => {
            // Input validation, if any, return an error message and retry
            if (isNaN(KRW) || KRW <= 0) {
                Swal.showValidationMessage("Please enter a valid amount");
                return;
            }

            try {
                const response = await axios.post(
                    `${BACKEND_API_URL}/account/deposit/KRW`,
                    { KRW },
                    {
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                return response.data;
            } catch (error) {
                // Show an error message if the response is not OK
                Swal.showValidationMessage(
                    `Request failed: ${error.response ? error.response.data : error.message}`
                );
            }
        },
        allowOutsideClick: () => !Swal.isLoading(),
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Success",
                html: `Successfully deposited, now you have <b>${Number(
                    result.value.KRW
                ).toLocaleString()} KRW</b> in your account!`,
                icon: "success",
                confirmButtonText: "OK",
            });
        }
    });
}
