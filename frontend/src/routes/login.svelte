<script>
    import { push } from "svelte-spa-router";
    import { onMount } from "svelte";
    import { auth } from "../stores/auth.js";
    import Swal from "sweetalert2";
    
    let username = "";
    let password = "";
    let errorMessage = "";

    async function login() {
        try {
            const response = await fetch('http://localhost:8000/account/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                if (response.status === 401 || response.status === 404) {
                    Swal.fire({
                        title: 'Who are you?',
                        text: 'Invalid username or password',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                    return;
                } 

                // if the error is not 401 or 404, throw an error
                throw new Error(await response.text());
            }

            const user = await response.json();
            if (response.status === 200) {
                Swal.fire({
                    title: 'Success',
                    text: `Welcome back, ${username}!`,
                    icon: 'success',
                    confirmButtonText: 'OK',
                    allowOutsideClick: false
                }).then((result) => {
                    // Save the JWT token to the local storage
                    auth.login(user.access_token);
                    
                    // redirect to the home page
                    if (result.isConfirmed) {
                        // Move to the exchange page
                        push('/exchange/main');
                    }
                });
            }
        } catch (error) {
            errorMessage = error.message;
        }
    }
</script>

<main>
    <div class="container mt-5">
        <h1>Login</h1>
        <h5>Oh, who's there?</h5>
        {#if errorMessage}
            <div class="alert alert-danger" role="alert">
                {errorMessage}
            </div>
        {/if}
        <form on:submit|preventDefault={login}>
            <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" bind:value={username} class="form-control" id="username" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" bind:value={password} class="form-control" id="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</main>

<style>
    * {
        font-family: 'SF Pro Display', sans-serif;
    }
    
    main {
        max-width: 320px;
        margin: auto;
    }
</style>
