import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({mode}) => {
    process.env = loadEnv(mode, process.cwd())
    return {
        plugins: [react()],
        base: process.env.BASE_URL
    }
})
