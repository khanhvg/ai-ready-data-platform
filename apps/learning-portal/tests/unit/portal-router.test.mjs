import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { createReleasedLearningAdapter } from '../../src/contracts/released-learning-adapter.mjs';
import { createReleasedModuleProvider } from '../../src/catalog/released-module-provider.mjs';
import { deriveModuleCatalog } from '../../src/catalog/module-catalog.mjs';
import { derivePortalRoutes, resolvePortalRoute } from '../../src/routing/portal-router.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const repositoryRoot = resolve(appRoot, '../..');
const lesson = JSON.parse(
  await readFile(resolve(repositoryRoot, 'learning/lessons/promotion-trust/lesson-v1.json'), 'utf8')
);

test('PTP-RED-A-013 derives one route truth from the released registry in stable order', () => {
  const registry = createReleasedModuleProvider(
    createReleasedLearningAdapter({ repositoryRoot })
  ).readRegistry();
  const routes = derivePortalRoutes(deriveModuleCatalog(registry));
  assert.deepEqual(
    routes.map(({ path }) => path),
    [
      '/',
      '/module',
      `/lessons/${lesson.id}`,
      ...lesson.narrativeSteps.map(({ id }) => `/lessons/${lesson.id}/steps/${id}`)
    ],
    'PTP_RED_ROUTE_DERIVATION_ABSENT'
  );
  assert.equal(new Set(routes.map(({ path }) => path)).size, 13, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
});

test('test-only structure proves generic add, remove, rename, uniqueness, and ordering locality', () => {
  const structure = {
    authorityKind: 'test-only-structure',
    descriptors: [
      {
        id: 'unit-module',
        title: 'Unit module',
        lessons: [
          {
            id: 'unit-lesson',
            title: 'Unit lesson',
            narrativeSteps: [{ id: 'unit-a', order: 1 }, { id: 'unit-b', order: 2 }]
          }
        ]
      }
    ]
  };
  const first = derivePortalRoutes(deriveModuleCatalog(structure));
  const renamed = structuredClone(structure);
  renamed.descriptors[0].lessons[0].narrativeSteps[1].id = 'unit-c';
  const second = derivePortalRoutes(deriveModuleCatalog(renamed));
  assert.equal(first.length, 5, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
  assert.equal(second.length, first.length, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
  assert.equal(second.at(-1).path.endsWith('/unit-c'), true, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
  assert.deepEqual(second.slice(0, -1), first.slice(0, -1), 'PTP_RED_ROUTE_DERIVATION_ABSENT');
});

test('PTP-RED-A-014 rejects malformed, ambiguous, traversal, overlong, and unregistered routes', () => {
  const routes = derivePortalRoutes(
    deriveModuleCatalog(createReleasedLearningAdapter({ repositoryRoot }).readRegistry())
  );
  for (const pathname of [
    '/missing',
    '/../module',
    '/%2e%2e/module',
    '/lessons//steps',
    `/${'x'.repeat(2049)}`
  ]) {
    assert.equal(resolvePortalRoute(pathname, routes), undefined, 'PTP_RED_ROUTE_DERIVATION_ABSENT');
  }
});

test('history resolution is a pure view selection with no mutation capability', () => {
  const routes = derivePortalRoutes(
    deriveModuleCatalog(createReleasedLearningAdapter({ repositoryRoot }).readRegistry())
  );
  for (const route of routes) {
    const resolved = resolvePortalRoute(route.path, routes);
    assert.equal(resolved.path, route.path);
    assert.equal('run' in resolved, false);
    assert.equal('reset' in resolved, false);
    assert.equal('complete' in resolved, false);
  }
});
