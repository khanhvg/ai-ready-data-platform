import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";
import { provideReleasedModules } from "../src/catalog/released-module-provider.mjs";
import { createModuleCatalog } from "../src/catalog/module-catalog.mjs";
import { publicRoutes, resolveRoute } from "../src/routing/portal-router.mjs";
import { renderStaticDocument } from "../src/render/static-document.mjs";

const appRoot = path.resolve(import.meta.dirname, "..");
const dist = path.join(appRoot, "dist");
const inventoryPath = path.join(dist, ".portal-build-inventory.json");
const sha256 = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const readRegular = async (file) => { const stat = await fs.lstat(file); if (!stat.isFile() || stat.isSymbolicLink() || stat.nlink !== 1 || stat.uid !== process.getuid()) throw new Error("OUTPUT_ALIAS_FORBIDDEN"); const bytes = await fs.readFile(file); return { stat, bytes }; };
const manifestEntry = await readRegular(path.join(dist, ".vite/manifest.json"));
const manifest = JSON.parse(manifestEntry.bytes.toString("utf8"));
const entry = manifest["index.html"];
if (!entry?.file || entry.css?.length !== 1) throw new Error("BUILD_ASSET_MANIFEST_INVALID");
const catalog = createModuleCatalog(await provideReleasedModules());
const routes = publicRoutes(catalog);
for (const route of routes) {
  const directory = route === "/" ? dist : path.join(dist, route.slice(1));
  await fs.mkdir(directory, { recursive: true, mode: 0o755 });
  const html = renderStaticDocument(resolveRoute(route, catalog), catalog, { script: `/${entry.file}`, style: `/${entry.css[0]}` });
  await fs.writeFile(path.join(directory, "index.html"), html, { flag: "w", mode: 0o644 });
}
await fs.writeFile(path.join(dist, "404.html"), renderStaticDocument({ kind: "not-found", path: "/404" }, catalog, { script: `/${entry.file}`, style: `/${entry.css[0]}` }), { flag: "w", mode: 0o644 });

const paths = [];
async function walk(directory) {
  const parent = await fs.lstat(directory); if (!parent.isDirectory() || parent.isSymbolicLink() || parent.uid !== process.getuid()) throw new Error("OUTPUT_DIRECTORY_UNSAFE");
  for (const item of await fs.readdir(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, item.name);
    if (absolute === inventoryPath) continue;
    if (item.isSymbolicLink()) throw new Error("OUTPUT_ALIAS_FORBIDDEN");
    if (item.isDirectory()) await walk(absolute); else if (item.isFile()) paths.push(absolute); else throw new Error("OUTPUT_SPECIAL_FILE_FORBIDDEN");
  }
}
await walk(dist);
const routeFiles = new Map(routes.map((route) => [route, route === "/" ? "index.html" : `${route.slice(1)}/index.html`]));
const servedUrls = new Map();
for (const [url, file] of routeFiles) servedUrls.set(file, [url]);
servedUrls.set("404.html", ["/__not_found__"]);
for (const file of [entry.file, ...entry.css]) servedUrls.set(file, [`/${file}`]);
let total = 0;
const files = [];
for (const absolute of paths.sort()) {
  const { stat, bytes } = await readRegular(absolute);
  const relative = path.relative(dist, absolute).split(path.sep).join("/");
  if (stat.size > 1024 * 1024) throw new Error("OUTPUT_FILE_LIMIT_EXCEEDED");
  if (relative.endsWith(".map")) throw new Error("SOURCE_MAP_FORBIDDEN");
  total += stat.size;
  files.push({ path: relative, bytes: stat.size, sha256: sha256(bytes), urls: servedUrls.get(relative) ?? [] });
}
if (files.length > 128 || total > 16 * 1024 * 1024) throw new Error("OUTPUT_LIMIT_EXCEEDED");
for (const file of servedUrls.keys()) if (!files.some((row) => row.path === file)) throw new Error(`BUILD_SERVED_FILE_MISSING:${file}`);
const packageBytes = (await readRegular(path.join(appRoot, "package.json"))).bytes;
const lockBytes = (await readRegular(path.join(appRoot, "package-lock.json"))).bytes;
const npmCli = path.resolve(path.dirname(process.execPath), "../lib/node_modules/npm/bin/npm-cli.js");
const npmBytes = (await readRegular(npmCli)).bytes;
const nodeBytes = (await readRegular(process.execPath)).bytes;
const npmVersion = spawnSync(process.execPath, [npmCli, "--version"], { encoding: "utf8", env: {} });
if (npmVersion.status !== 0) throw new Error("NPM_RUNTIME_UNAVAILABLE");
const inventory = { schemaVersion: "portal-build-inventory-v1", node: process.versions.node, npm: npmVersion.stdout.trim(), nodeBinarySha256: sha256(nodeBytes), npmCliSha256: sha256(npmBytes), packageJsonSha256: sha256(packageBytes), lockSha256: sha256(lockBytes), viteManifestSha256: sha256(manifestEntry.bytes), production: true, routes, files };
await fs.rm(inventoryPath, { force: true });
await fs.writeFile(inventoryPath, JSON.stringify(inventory), { flag: "wx", mode: 0o600 });
console.log(JSON.stringify({ routes: routes.length, files: files.length, bytes: total, buildInventorySha256: sha256(await fs.readFile(inventoryPath)) }));
