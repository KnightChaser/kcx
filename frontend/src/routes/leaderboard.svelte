<!-- /src/leaderboard.svelte -->
<script>
    import { onMount, onDestroy } from "svelte";
    import axios from "axios";
    import Swal from 'sweetalert2';

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    // Variable for leaderboard data
    let leaderboard = [];
    // Cache for profile images
    let imageCache = {};
    let hoverInfo = null;

    // Function to fetch leaderboard data
    async function fetchLeaderboard() {
        try {
            const response = await axios.get(`${BACKEND_API_URL}/statistics/user-leaderboard`);
            const data = response.data;
            leaderboard = await Promise.all(Object.entries(data).map(async ([username, total_asset_value]) => {
                let profileImageUrl = '';

                // Check if the image is already cached
                if (imageCache[username]) {
                    profileImageUrl = imageCache[username];
                } else {
                    try {
                        const imageResponse = await axios.post(`${BACKEND_API_URL}/account/get-profile-image/`, new URLSearchParams({
                            username: username
                        }), {
                            responseType: 'arraybuffer' // Ensure the response is in binary format
                        });

                        // Convert the image data to base64
                        const base64Image = btoa(
                            new Uint8Array(imageResponse.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
                        );
                        profileImageUrl = `data:image/png;base64,${base64Image}`;
                        // Cache the image
                        imageCache[username] = profileImageUrl;
                    } catch (error) {
                        console.error(`Error fetching profile image for ${username}:`, error);
                        // Use default placeholder if profile image is not found
                        profileImageUrl = '';
                    }
                }
                return { username, total_asset_value, profileImageUrl };
            }));
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

    // Get the maximum asset value for relative bar length calculation
    function getMaxAssetValue() {
        return Math.max(...leaderboard.map(user => user.total_asset_value));
    }

    function handleMouseEnter(index) {
        hoverInfo = { index, user: leaderboard[index] };
    }

    function handleMouseLeave() {
        hoverInfo = null;
    }

    function formatCurrency(value) {
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value);
    }

    // Function to get the popup info for each user according to their rank
    function getPopupInfo(index) {
        if (index === 0) {
            // Top user
            const nextUser = leaderboard[index + 1];
            return `${formatCurrency(Math.abs(nextUser.total_asset_value - leaderboard[index].total_asset_value))} more than <code><strong>@${nextUser.username}</strong></code><br>
                    (Top user. No one is richer than <code><strong>@${leaderboard[index].username}</strong></code>!)`;
        } else if (index === leaderboard.length - 1) {
            // Bottom user
            const prevUser = leaderboard[index - 1];
            return `${formatCurrency(prevUser.total_asset_value - leaderboard[index].total_asset_value)} less than <code><strong>@${prevUser.username}</strong></code><br>
                    (Bottom user. No one is poorer than <code><strong>@${leaderboard[index].username}</strong></code>!)`;
        } else {
            // Middle user
            const prevUser = leaderboard[index - 1];
            const nextUser = leaderboard[index + 1];
            return `${formatCurrency(prevUser.total_asset_value - leaderboard[index].total_asset_value)} less than <code><strong>@${prevUser.username}</strong></code>(+1 rank)<br>
                    ${formatCurrency(leaderboard[index].total_asset_value - nextUser.total_asset_value)} more than <code><strong>@${nextUser.username}</strong></code>(-1 rank)`;
        }
    }
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
                    <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Profile</th>
                    <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Username</th>
                    <th class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Total Asset Value (KRW)</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                {#each leaderboard as { username, total_asset_value, profileImageUrl }, index}
                    <tr class="hover:bg-gray-100 relative"
                        on:mouseenter={() => handleMouseEnter(index)}
                        on:mouseleave={handleMouseLeave}>
                        <td class="py-2 px-6 whitespace-nowrap text-center">{index + 1}</td>
                        <td class="py-2 px-6 whitespace-nowrap text-center">
                            {#if profileImageUrl}
                                <img src={profileImageUrl} alt="Profile" class="w-10 h-10 rounded-full mx-auto"/>
                            {:else}
                                <div class="w-10 h-10 rounded-full mx-auto bg-gray-300 flex items-center justify-center text-xl text-gray-600">
                                    ?
                                </div>
                            {/if}
                        </td>
                        <td class="py-2 px-6 whitespace-nowrap text-center">{username}</td>
                        <td class="py-2 px-6 whitespace-nowrap text-right relative">
                            <span>{formatCurrency(total_asset_value)}</span>
                            <div class="absolute inset-0 flex items-end">
                                <div class="h-1" style="width: {total_asset_value / getMaxAssetValue() * 100}%; background: linear-gradient(to right, purple, pink);"></div>
                            </div>
                        </td>
                        {#if hoverInfo && hoverInfo.index === index}
                            <div class="absolute bg-white border border-gray-300 shadow-lg p-2 rounded text-sm z-10" style="left: 50%; transform: translateX(-50%); top: -50%;">
                                {@html getPopupInfo(index)}
                            </div>
                        {/if}
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

    .relative {
        position: relative;
    }
</style>
