import assert from 'node:assert/strict';
import test from 'node:test';
import { loadPortalCatalog } from '../../src/sources/portal-source-loader.mjs';
import { derivePortalRoutes, resolvePortalRoute } from '../../src/routing/portal-router.mjs';

const routes = derivePortalRoutes(loadPortalCatalog());
test('router derives the exact bounded 38-route catalog', () => {
  assert.equal(routes.length, 38);
  assert.equal(routes.filter(({kind})=>kind==='module').length,20);
  assert.equal(routes.filter(({kind})=>kind==='lab').length,3);
  assert.equal(routes.filter(({kind})=>kind==='promotion-step').length,10);
  assert.equal(new Set(routes.map(({path})=>path)).size,38);
  for(const route of routes) assert.equal(resolvePortalRoute(route.path,routes),route);
});

test('router rejects unknown, ambiguous, encoded, traversal, and overlong paths', () => {
  for(const path of ['/unknown','/curriculum//f01','/../curriculum','/%2e%2e/curriculum',`/${'x'.repeat(2049)}`]) assert.equal(resolvePortalRoute(path,routes),undefined);
});
