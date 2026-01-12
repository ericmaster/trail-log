import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		allowedHosts: [
			'localhost',
			'127.0.0.1',
			'0.0.0.0',
			'trail-log-dev.ericmaster.ninja',
			'trail-log.ericmaster.ninja'
		],
		proxy: {
			'/api': {
				target: 'http://backend:8000',
				changeOrigin: true
			}
		}
	}
});
