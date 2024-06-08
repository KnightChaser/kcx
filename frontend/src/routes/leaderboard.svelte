<!-- /src/leaderboard.svelte -->
<script>
    import { onMount, onDestroy } from "svelte";
    import axios from "axios";
    import Swal from 'sweetalert2';

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    // Variable for leaderboard data
    let leaderboard = [];

    // Function to fetch leaderboard data
    async function fetchLeaderboard() {
        try {
            const response = await axios.get(`${BACKEND_API_URL}/statistics/user-leaderboard`);
            leaderboard = response.data;
        } catch (error) {
            console.error("Error fetching leaderboard data:", error);
            Swal.fire({
                icon: 'error',
                title: 'Failed to fetch leaderboard',
                text: error.message,
            });
        }
    }

    // Fetch leaderboard data on component mount and reload every 5 seconds
    let fetchInterval;

    onMount(() => {
        fetchLeaderboard();
        fetchInterval = setInterval(fetchLeaderboard, 5000);
    });

    onDestroy(() => {
        clearInterval(fetchInterval);
    });
</script>

<div class="w-full max-w-6xl mx-auto p-6 bg-white rounded-xl shadow-md space-y-6" id="leaderboard">
    <div class="flex justify-between items-center" id="leaderboard_table_header">
        <h2 class="text-2xl font-semibold text-gray-900">Leaderboard</h2>
        <button 
            class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75"
            on:click={() => window.location.href = '/'}>
            Back to Home Page
        </button>
    </div>

    <div class="overflow-x-auto">
        <table class="min-w-full bg-white border border-gray-200 table-auto">
            <thead class="bg-gray-50">
                <tr>
                    <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Rank</th>
                    <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Username</th>
                    <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Total Asset Value (KRW)</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                {#each Object.entries(leaderboard) as [username, total_asset_value], index}
                    <tr class="hover:bg-gray-100">
                        <td class="py-2 px-6 whitespace-nowrap text-center">{index + 1}</td>
                        <td class="py-2 px-6 whitespace-nowrap text-center">{username}</td>
                        <td class="py-2 px-6 whitespace-nowrap text-right">{new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(total_asset_value)}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>

<style>
    #leaderboard_table_header {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
        margin-bottom: 1rem;
    }

    table {
        font-family: "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono", monospace;
        width: 100%;
    }

    th, td {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }

    td {
        white-space: nowrap;
    }

    .table-auto th, .table-auto td {
        min-width: 150px;
    }
</style>
