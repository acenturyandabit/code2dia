import { defineConfig } from 'vite'
import tsconfigPaths from 'vite-tsconfig-paths'
export default defineConfig({
    server:{
        port: 3429
    },
    plugins:[
        tsconfigPaths()
    ]
});