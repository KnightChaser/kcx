import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import commonjs from '@rollup/plugin-commonjs';

export default defineConfig({
	plugins: [
		sveltekit(),
		commonjs()
	],
	server: {
		port: 5173,
		host: true
	}
});
