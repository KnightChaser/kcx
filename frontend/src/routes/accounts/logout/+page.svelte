<!-- frontend/src/routes/accounts/logout/+page.svelte -->

<!-- Handle logout -->
<script>
    import { onMount } from 'svelte';
    import { auth } from '../../../stores/auth';
    import Swal from "sweetalert2";
    import { browser } from '$app/environment';

    onMount(() => {
        Swal.fire({
            title: 'Time to say bye bye?',
            text: 'You are about to log out',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes',
            cancelButtonText: 'No'
        }).then((result) => {
            if (result.isConfirmed) {
                auth.logout();

                // Remove the username and email from the local storage
                if (browser) {
                    localStorage.removeItem('username');
                    localStorage.removeItem('email');

                    // Redirect to the main page
                    location.href = '/';
                }
            } else {
                // Redirect to the main page
                if (browser) {
                    location.href = '/';
                }   
            }
        });
    });
</script>