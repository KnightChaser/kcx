<!-- frontend/src/routes/user/userInfoTable.svelte -->

<script>
    import Swal from "sweetalert2";
    import { onMount } from "svelte";
    import axios from "axios";

    import { depositKRW } from "./functions/deposit";
    import { withdrawKRW } from "./functions/withdraw";
    import { profileImageSetter } from "./settings/functions/profileImageSetter";
    import { browser } from "$app/environment";
    import { auth } from "../../../stores/auth";
    
    const username = auth.getUsername();
    const uuid = auth.getUuid();
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    let profileImageUrl = '';

    onMount(async () => {
        // Fetch user profile image
        try {
            const response = await axios.post(`${BACKEND_API_URL}/account/get-profile-image/`, new URLSearchParams({
                username: username
            }), {
                responseType: 'arraybuffer' // Ensure the response is in binary format
            });

            // We get the image data in binary format, so we need to convert it to base64
            const base64Image = btoa(
                new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
            );

            profileImageUrl = `data:image/png;base64,${base64Image}`;
        } catch (error) {
            console.error("Error fetching user profile image:", error);
            profileImageUrl = ''; // No profile image found, use default
        }
    });

    function moveToAnotherPage(path) {
        if (browser) {
            window.location.href = path;
        }
    }   
</script>

<div class="w-full mb-6">
    <div class="flex flex-col items-center p-6 bg-white rounded-xl shadow-md space-y-4" id="user_info_panel">
        <div class="text-center">
            {#if profileImageUrl}
                <img src={profileImageUrl} alt="Profile" class="w-32 h-32 rounded-full mx-auto mb-4"/>
            {:else}
                <div class="w-32 h-32 rounded-full mx-auto mb-4 bg-gray-300 flex items-center justify-center text-4xl text-gray-600">
                    ?
                </div>
            {/if}
            <p class="text-2xl font-semibold text-gray-900">@{username}</p>
            <p class="text-sm text-gray-500">Your uuid (identifier): <code>{uuid}</code></p>
        </div>
        <!-- Buttons container -->
        <div class="flex space-x-4">
            <!-- Deposit -->
            <button
                class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
                on:click={depositKRW}>
                Deposit
            </button>
            <!-- Withdraw -->
            <button
                class="px-4 py-2 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-opacity-75"
                on:click={withdrawKRW}>
                Withdraw
            </button>
            <!-- Deposit/Withdraw History -->
            <button
                class="px-4 py-2 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75"
                on:click|preventDefault={() => moveToAnotherPage("/accounts/user/depositHistory")}>
                Wallet history
            </button>
            <!-- Crypto trade(buy/sell) history -->
            <button
                class="px-4 py-2 bg-yellow-500 text-white font-semibold rounded-lg shadow-md hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-75"
                on:click|preventDefault={() => moveToAnotherPage("/accounts/user/cryptoTradeHistory")}>
                Crypto trade history
            </button>
            <!-- User asset tracking -->
            <button
                class="px-4 py-2 bg-indigo-500 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-75"
                on:click|preventDefault={() => moveToAnotherPage("/accounts/user/assetTracking")}>
                Asset tracking
            </button>
            <!-- Settings -->
            <button
                class="px-4 py-2 bg-gray-500 text-white font-semibold rounded-lg shadow-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-75"
                on:click|preventDefault={() => moveToAnotherPage("/accounts/user/settings")}>
                Settings
            </button>
        </div>
    </div>
</div>

<style>
    #user_info_panel {
        font-family: "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>
