<!-- frontend/src/routes/hallOfFame/+page.svelte -->
<script>
    import { Card } from 'flowbite-svelte';

    let hallOfFame = [
        {
            place: 1,
            name: '<a href="https://www.github.com/n0paew" target="_blank" class="text-blue-500">n0paew</a>',
            description: 'The first person who found the vulnerability in this website, exploting the lack of verification procedures. Thank you for your contribution! (Reference: <a href="https://github.com/KnightChaser/kcx/issues/3" target="_blank" class="text-blue-500">GitHub Issue - Crypto trade API exploitation due to the lack of verification</a>)',
            date: '2024-06-26',
            imageUrl: `/images/hallOfFame/n0paew.jpg`
        },
        {
            place: 2,
            name: 'Hyeonsu Cha',
            description: 'Exploited the imperfect server deployment configuration, which took over the server account through unmanaged JWT. Thank you for your contribution!',
            date: '2024-06-27',
            imageUrl: '/images/hallOfFame/Hyeonsu Cha.jpg'
        },
        {
            place: 3,
            name: '<a href="https://x.com/real_as3617" target="_blank" class="text-blue-500">as3617</a>',
            description: 'Found a lack of market code(ticker) validity check, which allowed the attacker can insert invalid transaction data to the database. Thank you for your contribution! (Reference: <a href="https://github.com/KnightChaser/kcx/commit/1d22926a35fc98b3a0b9bd13fd08a159f9a49b28" target="_blank" class="text-blue-500">GitHub Commit - Fix the market code(ticker) validity check</a>)',
            date: '2024-06-27',
            imageUrl: '/images/hallOfFame/as3617.jpg'
        },
        {
            place: 4,
            name: '',
            description: '',
            date: '',
            imageUrl: ''
        },
        {
            place: 5,
            name: '',
            description: '',
            date: '',
            imageUrl: ''
        },
        {
            place: 6,
            name: '',
            description: '',
            date: '',
            imageUrl: ''
        }
    ];
</script>

<div class="flex flex-wrap justify-center items-center min-h-screen bg-gray-100 p-4" id="hallOfFameCards">
    {#each hallOfFame as person}
        <div class="w-full sm:w-1/2 lg:w-1/3 p-4">
            <Card class="max-w-none w-full h-full">
                {#if person.name}
                    <img src={person.imageUrl} alt={person.name} class="rounded-t-lg">
                    <div class="p-4">
                        <h5 class="text-2xl font-bold tracking-tight text-gray-900">{@html person.name}</h5>
                        <p class="font-normal text-gray-700">{@html person.description}</p>
                        <p class="text-sm text-gray-500">{person.date}</p>
                    </div>
                {:else}
                    <div class="p-4 text-center">
                        <h5 class="text-2xl font-bold tracking-tight text-gray-400">Place {person.place}</h5>
                        <p class="font-normal text-gray-400">No entry. But you can be the next one!</p>
                    </div>
                {/if}
            </Card>
        </div>
    {/each}
</div>

<style>
    #hallOfFameCards {
        font-family: "SF Mono", "SF Pro Icons", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>