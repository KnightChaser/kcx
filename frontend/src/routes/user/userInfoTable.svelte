<script>
    const username = localStorage.getItem('username');
    const uuid = localStorage.getItem('uuid');
</script>

<div class="w-full max-w-2xl mb-6">
    <div class="flex flex-col items-center p-6 bg-white rounded-xl shadow-md space-y-4" id="user_info_panel">
        <div class="text-center">
            <p class="text-2xl font-semibold text-gray-900">@{username}</p>
            <p class="text-sm text-gray-500">Your uuid (identifier): <code>{uuid}</code></p>
        </div>
    </div>
</div>

<style>
    #user_info_panel {
        font-family: "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", sans-serif;
    }
</style>