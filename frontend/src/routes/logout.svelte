<!-- Handle logout -->
<script>
    import { onMount } from 'svelte';
    import { push } from "svelte-spa-router";
    import { auth } from "../stores/auth.js";
    import Swal from "sweetalert2";

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
                localStorage.removeItem('username');
                localStorage.removeItem('email');

                push('/');
            } else {
                push('/'); 
            }
        });
    });
</script>