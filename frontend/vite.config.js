import { defineConfig } from 'vite';
import svelte from '@sveltejs/vite-plugin-svelte';
import { mkcert } from 'vite-plugin-mkcert';

export default defineConfig({
  plugins: [svelte(), mkcert()],
  server: {
    https: true,
    host: true,
    port: 5173,
  },
});
