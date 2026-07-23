import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createReleasedLearningAdapter } from '../src/contracts/released-learning-adapter.mjs';
import { createReleasedModuleProvider } from '../src/catalog/released-module-provider.mjs';
import { deriveModuleCatalog } from '../src/catalog/module-catalog.mjs';
import { derivePortalRoutes } from '../src/routing/portal-router.mjs';
import { renderStaticDocument } from '../src/render/static-document.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const adapter = createReleasedLearningAdapter();
const provider = createReleasedModuleProvider(adapter);
const catalog = deriveModuleCatalog(provider.readRegistry());
const routes = derivePortalRoutes(catalog);
const viteDocument = await readFile(resolve(appRoot, 'dist/index.html'), 'utf8');
const scripts = [...viteDocument.matchAll(/<script[^>]+src="([^"]+)"[^>]*><\/script>/g)].map(
  (match) => match[1]
);

for (const route of routes) {
  const output = route.path === '/' ? 'index.html' : `${route.path.slice(1)}/index.html`;
  const target = resolve(appRoot, 'dist', output);
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, renderStaticDocument(route, catalog, { scripts }), {
    encoding: 'utf8',
    mode: 0o644
  });
}

process.stdout.write(`${JSON.stringify({ routes: routes.length, semanticReady: catalog.semanticReady })}\n`);
