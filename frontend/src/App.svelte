<script>
    let username = "";
    let password = "";

    // Handle login
    async function handleLogin() {
        let response = await fetch("http://localhost:8000/account/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            let data = await response.json();
            alert(`Welcome ${data.username}`);
        } else {
            alert("Invalid credentials");
        }
    }
</script>

<h1>Login</h1>
<input type="text" bind:value={username} placeholder="Username" />
<input type="password" bind:value={password} placeholder="Password" />
<button on:click={handleLogin}>Login</button>
