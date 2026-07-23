import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { loadPortalCatalog } from './src/sources/portal-source-loader.mjs';

const virtualId = 'virtual:portal-catalog';
const resolvedVirtualId = `\0${virtualId}`;

export default defineConfig({
  plugins: [
    {
      name: 'portal-authority-loader',
      resolveId(id) { return id === virtualId ? resolvedVirtualId : undefined; },
      load(id) { return id === resolvedVirtualId ? `export default ${JSON.stringify(loadPortalCatalog())};` : undefined; }
    },
    react()
  ],
  base: '/',
  build: { outDir: 'dist', emptyOutDir: true, sourcemap: false, manifest: true, assetsInlineLimit: 0 },
  server: { host: '127.0.0.1' }
});
