import fs from "node:fs/promises";
import path from "node:path";
import { provideReleasedModules } from "../src/catalog/released-module-provider.mjs";
import { createModuleCatalog } from "../src/catalog/module-catalog.mjs";
import { PUBLIC_ROUTES, resolveRoute } from "../src/routing/portal-router.mjs";
import { renderStaticDocument } from "../src/render/static-document.mjs";

const appRoot = path.resolve(import.meta.dirname, "..");
const dist = path.join(appRoot, "dist");
const manifest = JSON.parse(await fs.readFile(path.join(dist, ".vite/manifest.json"), "utf8"));
const entry = manifest["index.html"];
if (!entry?.file || !entry.css?.length) throw new Error("BUILD_ASSET_MANIFEST_INVALID");
const catalog = createModuleCatalog(await provideReleasedModules());
for (const route of PUBLIC_ROUTES) {
  const directory = route === "/" ? dist : path.join(dist, route.slice(1));
  await fs.mkdir(directory, { recursive: true });
  const html = renderStaticDocument(resolveRoute(route), catalog, { script: `/${entry.file}`, style: `/${entry.css[0]}` });
  await fs.writeFile(path.join(directory, "index.html"), html, { flag: "w", mode: 0o644 });
}
await fs.writeFile(path.join(dist, "404.html"), renderStaticDocument({ kind: "not-found", path: "/404" }, catalog, { script: `/${entry.file}`, style: `/${entry.css[0]}` }), { mode: 0o644 });
const files = [];
async function walk(dir) { for (const item of await fs.readdir(dir, { withFileTypes: true })) { const absolute = path.join(dir, item.name); if (item.isSymbolicLink()) throw new Error("OUTPUT_ALIAS_FORBIDDEN"); if (item.isDirectory()) await walk(absolute); else if (item.isFile()) files.push(absolute); else throw new Error("OUTPUT_SPECIAL_FILE_FORBIDDEN"); } }
await walk(dist);
let total = 0;
for (const file of files) { const stat = await fs.stat(file); if (stat.size > 1024 * 1024) throw new Error("OUTPUT_FILE_LIMIT_EXCEEDED"); total += stat.size; if (file.endsWith(".map")) throw new Error("SOURCE_MAP_FORBIDDEN"); }
if (files.length > 128 || total > 16 * 1024 * 1024) throw new Error("OUTPUT_LIMIT_EXCEEDED");
console.log(JSON.stringify({ routes: PUBLIC_ROUTES.length, files: files.length, bytes: total }));
