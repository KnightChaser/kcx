// automaticLogout.js
// If the user is authenticated, this module will automatically log them out after a certain period of inactivity.
// If the user runs out of session time, they will be redirected to the login page after receiving the message.

import { push } from "svelte-spa-router";
import { auth } from "../stores/auth";
import Swal from "sweetalert2";

// Decode the JWT token into a JSON object
function decodeJWT(token) {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload); // Parse the JSON payload
}

// Check the validity of the session, and log out the user if the session has expired
export function sessionValidityCheck() {
    // Get the token from the local storage
    const token = localStorage.getItem("token");
    if (!token)
        console.error("Token not found in the local storage");

    // Decode the token to get the expiration time
    // And calculate the remaining time until the token expires
    const expirationTime = decodeJWT(token).exp * 1000;
    const remainingTime = expirationTime - Date.now();
    if (remainingTime <= 0) {
        Swal.fire({
            title: "Session Expired",
            text: "Please log in again",
            icon: "info",
            confirmButtonText: "OK",
        });
        auth.logout();
        push("/login");
        return;
    } else {
        // Set a timer to automatically log out the user when the token expires
        return;
    }
}