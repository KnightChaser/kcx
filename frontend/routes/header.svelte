<script>
    import { push } from "svelte-spa-router";

    function moveToAnotherPage(path) {
        push(path);
    }
</script>

<nav class="navbar navbar-expand-lg bg-dark border-bottom border-body">
    <div class="container-fluid">
        <a class="navbar-brand"
           href="#/"
           on:click|preventDefault={() => moveToAnotherPage('/')}
           tabindex="0">KXC</a>

        <!-- Right-aligned navigation links -->
        <div class="d-flex justify-content-end" style="width: 100%;">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="/" on:click|preventDefault={() => moveToAnotherPage('/')}
                       tabindex="0">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/login" on:click|preventDefault={() => moveToAnotherPage('/login')}
                       tabindex="0">Login</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/register" on:click|preventDefault={() => moveToAnotherPage('/register')}
                       tabindex="0">Register</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

<style>
    @font-face {
        font-family: "SF Pro Display";
        src: url("../src/assets/SF-Pro-Display-Medium.otf") format("opentype");
    }

    nav {
        font-family: "SF Pro Display";
        background-color: slateblue !important;
    }

    a {
        color: white;
    }
</style>
