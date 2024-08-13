// routes/user/functions/withdraw.js
// Withdraw money(KRW; fiat currency) from user's account as the given amount

import Swal from "sweetalert2";
import axios from "axios";
import { auth } from "../../../../stores/auth";

const token = auth.getToken();
const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

// Withdraw money (KRW; fiat currency)
export async function withdrawKRW() {
    Swal.fire({
        title: "Withdraw Money",
        text: "How much money do you want to withdraw? (KRW)",
        input: "text",
        inputAttributes: {
            autocapitalize: "off",
        },
        showCancelButton: true,
        confirmButtonText: "Withdraw",
        showLoaderOnConfirm: true,
        preConfirm: async (KRW) => {
            // Input validation, if any, return an error message and retry
            if (isNaN(KRW) || KRW <= 0) {
                Swal.showValidationMessage("Please enter a valid amount");
                return;
            }

            try {
                const response = await axios.post(
                    `${BACKEND_API_URL}/account/withdraw/KRW`,
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
                // Withdrawal was forbidden (403) due to the administrator's policy.
                if (error.response && error.response.status === 403) {
                    Swal.showValidationMessage(
                        "Withdrawal is forbidden due to the administrator's policy. Contact the administrator for more information."
                    );
                    return;
                }
                
                // Throw an error if the response is not OK
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
                html: `Successfully withdrawn, now you have <b>${Number(
                    result.value.KRW
                ).toLocaleString()} KRW</b> in your account!`,
                icon: "success",
                confirmButtonText: "OK",
            });
        }
    });
}
