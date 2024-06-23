<script>
    import { onMount, onDestroy } from "svelte";
    import axios from "axios";
    import Swal from 'sweetalert2';
    import { browser } from '$app/environment';
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Popover } from 'flowbite-svelte';
    import { BadgeCheckOutline } from 'flowbite-svelte-icons';

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;
    const ADMIN_ACCOUNT_ID = import.meta.env.VITE_ADMIN_ACCOUNT_ID

    // Variable for leaderboard data
    let leaderboard = [];
    // Cache for profile images
    let imageCache = {};

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
                        // Suppress the error if the image is not found
                        if (error.response && error.response.status === 404) {
                            profileImageUrl = '';
                        } else {
                            console.error(`Error fetching profile image for ${username}:`, error);
                        }
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

    function formatCurrency(value) {
        return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value);
    }
</script>

<main class="container mx-auto p-6 bg-gray-50 min-h-screen">
    <div class="max-w-6xl mx-auto bg-white rounded-xl shadow-md p-6 space-y-6" id="leaderboard">
        <div class="flex justify-between items-center" id="leaderboard_table_header">
            <h2 class="text-2xl font-semibold text-gray-900">Leaderboard</h2>
        </div>

        <div class="overflow-x-auto">
            <Table striped={true} class="min-w-full bg-white border border-gray-200 table-auto" style="font-family: SF Mono">
                <TableHead class="bg-gray-50">
                    <TableHeadCell class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Rank</TableHeadCell>
                    <TableHeadCell class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Profile</TableHeadCell>
                    <TableHeadCell class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Username</TableHeadCell>
                    <TableHeadCell class="py-3 px-6 text-xs text-gray-500 uppercase tracking-wider text-center font-bold">Total Asset Value (KRW)</TableHeadCell>
                </TableHead>
                <TableBody class="bg-white divide-y divide-gray-200">
                    {#each leaderboard as { username, total_asset_value, profileImageUrl }, index}
                        <TableBodyRow class="hover:bg-gray-100 relative" id={"leaderboard-row-" + index}>
                            <TableBodyCell class="py-2 px-6 whitespace-nowrap text-center">{index + 1}</TableBodyCell>
                            <TableBodyCell class="py-2 px-6 whitespace-nowrap text-center">
                                {#if profileImageUrl}
                                    <img src={profileImageUrl} alt="Profile" class="w-10 h-10 rounded-full mx-auto"/>
                                {:else}
                                    <div class="w-10 h-10 rounded-full mx-auto bg-gray-300 flex items-center justify-center text-xl text-gray-600">
                                        ?
                                    </div>
                                {/if}
                            </TableBodyCell>
                            <TableBodyCell class="py-2 px-6 whitespace-nowrap text-center">
                                {#if username === ADMIN_ACCOUNT_ID}
                                    <span class="text-blue-500 font-semibold">{username}</span>
                                    <BadgeCheckOutline class="w-6 h-6 text-blue-500 inline-block ml-2" id="administrator_badge"/>
                                    <Popover target="administrator_badge" position="bottom-start" class="bg-white shadow-md rounded-lg p-2">
                                        <p class="text-sm text-gray-600">Webpage administrator</p>
                                    </Popover>
                                {:else}
                                    <span>{username}</span>
                                {/if}
                            </TableBodyCell>
                            <TableBodyCell class="py-2 px-6 whitespace-nowrap text-right relative">
                                <span>{formatCurrency(total_asset_value)}</span>
                                <div class="absolute inset-0 flex items-end">
                                    <div class="h-1" style="width: {total_asset_value / getMaxAssetValue() * 100}%; background: linear-gradient(to right, purple, pink);"></div>
                                </div>
                            </TableBodyCell>
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        </div>
    </div>
</main>

<style>
    #leaderboard_table_header {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
        margin-bottom: 1rem;
    }
</style>
