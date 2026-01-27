import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Detect if running in Docker
const isDocker = process.env.DOCKER === 'true' || process.env.CHOKIDAR_USEPOLLING === 'true'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // Allow connections from outside container (Docker)
    port: 5173,
    watch: {
      usePolling: isDocker || process.env.CHOKIDAR_USEPOLLING === 'true', // Required for Docker volume mounts
      interval: 1000, // Polling interval in ms
      ignored: ['**/node_modules/**', '**/.git/**'], // Ignore these paths
    },
    hmr: {
      host: 'localhost', // HMR host for browser connection
      port: 5173,
    },
    proxy: {
      '/api': {
        // Use Docker service name when running in Docker, fallback to localhost for local dev
        target: isDocker ? 'http://backend:8000' : 'http://localhost:8000',
        changeOrigin: true,
        ws: true, // Enable WebSocket proxying for HMR
      }
    }
  }
})
