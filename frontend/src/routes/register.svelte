<!-- register.svelte (Applying user registration) -->

<script>
    import { onMount } from "svelte";
    import { push } from "svelte-spa-router";
    import Swal from "sweetalert2";

    let username = "";
    let email = "";
    let password = "";
    let confirmPassword = "";
    let acceptTerms = false;

    const submitForm = async () => {
        if (password !== confirmPassword) {
            Swal.fire({
                title: "Error",
                text: "Passwords do not match.",
                icon: "error",
            });
            return;
        }
        if (!acceptTerms) {
            Swal.fire({
                title: "Error",
                text: "Accept the terms & condition to proceed.",
                icon: "error",
            });
            return;
        }

        const response = await fetch(
            "http://localhost:8000/account/register/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, email, password }),
            }
        );

        if (!response.ok) {
            const data = await response.json();
            Swal.fire({
                title: "Error",
                text: data.detail,
                icon: "error",
            });
            return;
        }

        // Account created successfully
        const data = await response.json();
        Swal.fire({
            title: "Success",
            text: "Account created successfully.",
            icon: "success",
            confirmButtonText: "Go to login",
            allowOutsideClick: false,
        }).then((result) => {
            if (result.isConfirmed) {
                push("/login");
            }
        });
    };
</script>

<main class="container mt-5" id="registration_form">
    <h2>Register</h2>
    <form on:submit|preventDefault={submitForm}>
        <div class="mb-3">
            <label for="username" class="form-label">ID</label>
            <input
                type="text"
                class="form-control"
                id="username"
                bind:value={username}
                required
            />
        </div>
        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
                type="email"
                class="form-control"
                id="email"
                bind:value={email}
                required
            />
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
                type="password"
                class="form-control"
                id="password"
                bind:value={password}
                required
            />
        </div>
        <div class="mb-3">
            <label for="confirmPassword" class="form-label"
                >Confirm Password</label
            >
            <input
                type="password"
                class="form-control"
                id="confirmPassword"
                bind:value={confirmPassword}
                required
            />
        </div>
        <div class="accordion" id="accordionPanelsStayOpenExample">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button
                        class="accordion-button"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#panelsStayOpen-collapseOne"
                        aria-expanded="true"
                        aria-controls="panelsStayOpen-collapseOne"
                    >
                        Terms & Conditions
                    </button>
                </h2>
                <div
                    id="panelsStayOpen-collapseOne"
                    class="accordion-collapse collapse show"
                >
                    <div class="accordion-body">
                        By clicking the "Register" button, you agree to this condition.<br>
                        <strong>First</strong>, any abusing or inappropriate behavior is strictly prohibited.<br>
                        <strong>Second</strong>, you must not share your account information with others.<br>
                        <strong>Third</strong>, you have not to leak any security vulnerabilities to the public(If you find any, please report it to the administrator immediately.)
                    </div>
                </div>
            </div>
        </div>
        <div class="mb-3 form-check">
            <input
                type="checkbox"
                class="form-check-input"
                id="acceptTerms"
                bind:checked={acceptTerms}
            />
            <label class="form-check-label" for="acceptTerms"
                >I accept the terms and conditions</label
            >
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
    </form>
</main>

<style>
    * {
        max-width: 600px;
        margin: auto;
    }

    #registration_form {
        font-family: "SF Pro Display", "Arial", sans-serif;
    }
</style>
