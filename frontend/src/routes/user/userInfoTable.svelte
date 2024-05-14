<!-- routes/user/userInfoTable.svelte -->

<script>
    import Swal from "sweetalert2";
    const username = localStorage.getItem('username');
    const token = localStorage.getItem('token');
    const uuid = localStorage.getItem('uuid');
    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
    import { depositKRW } from "./functions/deposit";
    import { widthdrawKRW } from "./functions/withdrawl";

</script>

<div class="w-full max-w-2xl mb-6">
    <div class="flex flex-col items-center p-6 bg-white rounded-xl shadow-md space-y-4" id="user_info_panel">
        <div class="text-center">
            <p class="text-2xl font-semibold text-gray-900">@{username}</p>
            <p class="text-sm text-gray-500">Your uuid (identifier): <code>{uuid}</code></p>
        </div>
        <!-- Buttons container -->
        <div class="flex space-x-4">
            <!-- Deposit -->
            <button
                class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg -md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
                on:click={depositKRW}>
                Deposit
            </button>
            <!-- Withdrawl -->
            <button
                class="px-4 py-2 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-opacity-75"
                on:click={widthdrawKRW}>
                Withdraw
            </button>
        </div>
    </div>
</div>

<style>
    #user_info_panel {
        font-family: "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>