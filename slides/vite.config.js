import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  assetsInclude: ['**/*.md', '**/*.png'],
  resolve: { alias: { mqtt: 'mqtt/dist/mqtt.js', }, },
  server: {
    host: '0.0.0.0',
}
})
