// routes/user/functions/deposit.js
// Deposit money(KRW; fiat currency) to user's account as the given amount

import Swal from "sweetalert2";
const token = localStorage.getItem("token")
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

            const response = await fetch(
                `${BACKEND_API_URL}/account/deposit/KRW`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({ KRW }),
                }
            );

            if (!response.ok) {
                // Throw an error if the response is not OK
                throw new Error(await response.text());
            }

            return response.json();
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
