<!-- /src/welcome.svelte  -->

<!-- A welcome page for who didn't log in (website introduction page)  -->
<script>
    let isChecked = false;
    import TotalTransactionAmountPanel from "./welcomePageComponents/totalTransactionAmountPanel.svelte";
</script>

<section class="wrapper">
    <div class={isChecked ? "hero dark" : "hero"}></div>
    <div class="content">
        <TotalTransactionAmountPanel />
        <h1 class="h1--scalingSize" data-text="An awesome title">
            KCX
        </h1>
        <h3>
            Free-From-Risk simulated cryptocurrency trading platform
        </h3>
        <input type="checkbox" id="switch" bind:checked={isChecked} />
    </div>
</section>

<style>
    * {
        font-family: "SF Pro Display", "SF Pro Icons", "Helvetica Neue",
            "Helvetica", "Arial", sans-serif;
    }

    /* the background effect */
    /* houdini */
    @property --blink-opacity {
        syntax: "<number>";
        inherits: false;
        initial-value: 1;
    }

    @keyframes blink-animation {
        0%,
        100% {
            opacity: var(--blink-opacity, 1);
        }
        50% {
            opacity: 0;
        }
    }

    /*base*/
    :root {
        font-family: Inter, sans-serif;
        --stripe-color: #fff;
        --bg: var(--stripe-color);
        --maincolor: var(--bg);
    }

    :global(body) {
        width: 100vw;
        min-height: 100vh;
        display: flex;
        place-content: center;
        place-items: flex-start center;
        background: var(--bg);
    }

    /*custom*/
    @keyframes smoothBg {
        from {
            background-position:
                50% 50%,
                50% 50%;
        }
        to {
            background-position:
                350% 50%,
                350% 50%;
        }
    }

    .wrapper {
        width: 100%;
        height: auto;
        position: relative;
    }
    
    .hero {
        width: 100%;
        height: 100%;
        min-height: 100vh;
        position: relative;
        display: flex;
        place-content: center;
        place-items: center;
        --stripes: repeating-linear-gradient(
            100deg,
            var(--stripe-color) 0%,
            var(--stripe-color) 7%,
            transparent 10%,
            transparent 12%,
            var(--stripe-color) 16%
        );
        --rainbow: repeating-linear-gradient(
            100deg,
            #60a5fa 10%,
            #e879f9 15%,
            #60a5fa 20%,
            #5eead4 25%,
            #60a5fa 30%
        );
        background-image: var(--stripes), var(--rainbow);
        background-size: 300%, 200%;
        background-position:
            50% 50%,
            50% 50%;
        filter: blur(10px) invert(100%);
        mask-image: radial-gradient(
            ellipse at 100% 0%,
            black 40%,
            transparent 70%
        );
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        background-image: var(--stripes), var(--rainbow);
        background-size: 200%, 100%;
        animation: smoothBg 60s linear infinite;
        background-attachment: fixed;
        mix-blend-mode: difference;
    }

    .content {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        display: flex;
        place-content: center;
        place-items: center;
        flex-flow: column;
        gap: 4.5%;
        text-align: center;
        mix-blend-mode: difference;
        -webkit-mix-blend-mode: difference;
        filter: invert(1);
    }

    .h1--scalingSize {
        font-size: calc(1rem + 5vw);
        position: relative;
    }

    #switch {
        appearance: none;
        -webkit-appearance: none;
        opacity: 0;
    }

    @keyframes animSwitch {
        50% {
            transform: scale(1.2);
            font-weight: 900;
        }
    }

    :has(:checked) .hero,
    :has(:checked) .hero::after {
        filter: blur(10px) opacity(50%) saturate(200%);
    }

    :has(:checked) {
        --stripe-color: #000;
    }
</style>
