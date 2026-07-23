import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readdir, readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { deriveModuleCatalog } from '../../src/catalog/module-catalog.mjs';
import { createReleasedLearningAdapter } from '../../src/contracts/released-learning-adapter.mjs';
import { createSafeViewModel } from '../../src/contracts/safe-view-model.mjs';
import { renderStaticDocument } from '../../src/render/static-document.mjs';
import { derivePortalRoutes } from '../../src/routing/portal-router.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const repositoryRoot = resolve(appRoot, '../..');

test('PTP-RED-A-021 static and React view models share stable fact IDs and escaping', () => {
  const catalog = deriveModuleCatalog(
    createReleasedLearningAdapter({ repositoryRoot }).readRegistry()
  );
  const routes = derivePortalRoutes(catalog);
  const model = createSafeViewModel(routes[0], catalog);
  const html = renderStaticDocument(routes[0], catalog, { scripts: ['/assets/unit.js'] });
  assert.equal((model.factIds?.length ?? 0) > 0, true, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
  for (const factId of model.factIds ?? []) {
    assert.match(html, new RegExp(`data-fact-id="${factId}"`), 'PTP_RED_ROUTE_DERIVATION_ABSENT');
  }
  const structural = {
    authorityKind: 'test-only-structure',
    descriptors: [{ id: 'unit-module', title: '<unit & module>', lessons: [] }]
  };
  const structuralCatalog = deriveModuleCatalog(structural);
  const structuralRoute = derivePortalRoutes(structuralCatalog)[0];
  const escaped = renderStaticDocument(structuralRoute, structuralCatalog);
  assert.doesNotMatch(escaped, /<unit & module>/);
});

test('production build derives thirteen no-JavaScript documents from one registry', async () => {
  execFileSync('npm', ['run', 'build'], { cwd: appRoot, stdio: 'pipe' });
  const files = [];
  async function walk(directory) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const target = resolve(directory, entry.name);
      if (entry.isDirectory()) await walk(target);
      else files.push(target);
    }
  }
  await walk(resolve(appRoot, 'dist'));
  const htmlFiles = files.filter((path) => path.endsWith('.html'));
  assert.equal(htmlFiles.length, 13, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
  for (const htmlPath of htmlFiles) {
    const html = await readFile(htmlPath, 'utf8');
    assert.match(html, /insufficient-evidence\/no-common-grain/, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
    assert.match(html, /không thể hoàn thành|không ghi nhận hoàn thành/i, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
  }
});

test('PTP-RED-A-022 build inventory excludes mutation, storage, cloud, secret, source-map, and test-only bytes', async () => {
  const disallowed = [
    'localStorage',
    'sessionStorage',
    'indexedDB',
    'serviceWorker',
    'AWS_',
    'BEGIN PRIVATE KEY',
    'unit-module',
    'test-only-structure'
  ];
  const files = await readdir(resolve(appRoot, 'dist'), { recursive: true });
  assert.equal(files.some((path) => path.endsWith('.map')), false, 'PTP_RED_REQUEST_POLICY_ABSENT');
  const combined = (
    await Promise.all(
      files
        .filter((path) => /\.(?:html|js|css|json)$/.test(path))
        .map((path) => readFile(resolve(appRoot, 'dist', path), 'utf8'))
    )
  ).join('\n');
  for (const token of disallowed) assert.equal(combined.includes(token), false, 'PTP_RED_REQUEST_POLICY_ABSENT');
});
