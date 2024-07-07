<!-- frontend/src/routes/accounts/user/settings/+page.svelte -->
<script>
    import { Button, Label } from 'flowbite-svelte';
    import { auth } from '../../../../stores/auth';
    import { onMount } from 'svelte';
    import axios from 'axios';
    import Swal from 'sweetalert2';
    import { profileImageSetter } from './functions/profileImageSetter';

    const BACKEND_API_URL = import.meta.env.VITE_BACKEND_API_URL;

    let user = {
        username: auth.getUsername(),
        email: auth.getEmail(),
        password: '*****', // Not to be shown in plain text
        profilePicture: 'https://via.placeholder.com/500',
        uuid: auth.getUuid()
    };

    onMount(async () => {
        try {
            const response = await axios.post(`${BACKEND_API_URL}/account/get-profile-image/`, new URLSearchParams({
                username: auth.getUsername()
            }), {
                responseType: 'arraybuffer' // Ensure the response is in binary format
            });

            // We get the image data in binary format, so we need to convert it to base64
            const base64Image = btoa(
                new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
            );

            user.profilePicture = `data:image/png;base64,${base64Image}`;
        } catch (error) {
            console.error("Error fetching user profile image:", error);
            // No profile image found, use default
            user.profilePicture = 'https://via.placeholder.com/500';
        }
    });

    function handleChangeAlert() {
        Swal.fire({
            icon: 'info',
            title: 'Change Feature',
            text: 'This feature is not implemented yet.'
        });
    }
</script>

<style>
    .profile-picture {
        width: 300px;
        height: 300px;
        border-radius: 50%;
        cursor: pointer;
        /* shadow */
        box-shadow: 0 0 0 4px #fff, 0 0 0 6px #7C3AED;
    }

    #user_settings {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }

    .info-group {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #f9fafb;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }

    .info-text {
        flex: 1;
        margin-right: 1rem;
        color: #374151;
    }

    .info-button {
        flex-shrink: 0;
        background-color: #3b82f6; /* Blue background color */
        color: #ffffff; /* White text color */
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        cursor: pointer;
    }

    .info-button:hover {
        background-color: #2563eb; /* Darker blue on hover */
    }
</style>

<div class="w-full max-w-4xl mx-auto p-6 bg-white rounded-xl shadow-md mt-6" id="user_settings">
    <div class="mb-6">
        <h1 class="text-3xl font-bold">User Settings</h1>
    </div>
    <div class="flex flex-col md:flex-row md:justify-between">
        <div class="flex flex-col space-y-4 md:flex-grow">
            <div>
                <Label for="uuid" class="mb-2">User UUID</Label>
                <div class="info-group">
                    <span id="uuid" class="info-text">{user.uuid}</span>
                </div>
            </div>
            <div>
                <Label for="username" class="mb-2">Username</Label>
                <div class="info-group">
                    <span id="username" class="info-text">{user.username}</span>
                </div>
            </div>
            <div>
                <Label for="email" class="mb-2">Email</Label>
                <div class="info-group">
                    <span id="email" class="info-text">{user.email}</span>
                    <button on:click={handleChangeAlert} class="info-button">Change</button>
                </div>
            </div>
            <div>
                <Label for="password" class="mb-2">Password</Label>
                <div class="info-group">
                    <span id="password" class="info-text">{user.password}</span>
                    <button on:click={handleChangeAlert} class="info-button">Change</button>
                </div>
            </div>
        </div>
        <div class="flex flex-col items-center mt-6 md:mt-0 md:ml-6">
            <button on:click={profileImageSetter} class="profile-picture-button mb-2">
                <img src={user.profilePicture} alt="Click to change" class="profile-picture" />
            </button>
            <Button color="blue" class="mb-2">Change Profile Picture</Button>
            <p class="text-sm text-gray-500">Click the image to change the profile picture!</p>
        </div>
    </div>
</div>
