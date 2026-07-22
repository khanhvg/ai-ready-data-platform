import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { provideReleasedModules } from "./src/catalog/released-module-provider.mjs";

const catalog = { modules: await provideReleasedModules() };

export default defineConfig({
  plugins: [react()],
  define: { "globalThis.__PORTAL_CATALOG__": JSON.stringify(catalog) },
  build: { sourcemap: false, manifest: true, assetsInlineLimit: 0, rollupOptions: { output: { entryFileNames: "assets/portal-[hash].js", assetFileNames: "assets/portal-[hash][extname]" } } },
  server: { host: "127.0.0.1" }
});
