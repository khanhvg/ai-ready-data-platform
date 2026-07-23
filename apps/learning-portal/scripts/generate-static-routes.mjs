import { copyFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadPortalCatalog, repositoryRoot } from '../src/sources/portal-source-loader.mjs';
import { derivePortalRoutes } from '../src/routing/portal-router.mjs';
import { renderStaticDocument } from '../src/render/static-document.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const catalog = loadPortalCatalog();
const routes = derivePortalRoutes(catalog);
const viteDocument = await readFile(resolve(appRoot, 'dist/index.html'), 'utf8');
const scripts = [...viteDocument.matchAll(/<script[^>]+src="([^"]+)"[^>]*><\/script>/g)].map((match) => match[1]);
const styles = [...viteDocument.matchAll(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"[^>]*>/g)].map((match) => match[1]);

for (const route of routes) {
  const target = resolve(appRoot, 'dist', route.path === '/' ? 'index.html' : `${route.path.slice(1)}/index.html`);
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, renderStaticDocument(route, catalog, { scripts, styles }), { encoding: 'utf8', mode: 0o644 });
}
const architectureRoot = resolve(appRoot, 'dist/architecture');
await mkdir(architectureRoot, { recursive: true });
for (const view of catalog.architecture.views) {
  for (const extension of ['svg','txt']) await copyFile(resolve(repositoryRoot, `architecture/expansions/i5-06/rendered/${view.id}.${extension}`), resolve(architectureRoot, `${view.id}.${extension}`));
}
process.stdout.write(`${JSON.stringify({ routes: routes.length, ...catalog.counts, manualOnly: true })}\n`);
