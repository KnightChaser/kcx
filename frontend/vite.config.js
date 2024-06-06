import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import fs from 'fs';

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    https: {
      key: fs.readFileSync('./certs/example_local_key.pem'),
      cert: fs.readFileSync('./certs/example_local_cert.pem')
    }
  },
  plugins: [svelte()],
})