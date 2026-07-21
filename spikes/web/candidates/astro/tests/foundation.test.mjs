import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import test from 'node:test';

const root = resolve(import.meta.dirname, '../../../../..');
const candidate = resolve(root, 'spikes/web/candidates/astro');
test('ASTRO-FOUNDATION-001 pins the frozen native mode and exact supply chain', () => {
  const pkg = JSON.parse(readFileSync(resolve(candidate, 'package.json')));
  assert.deepEqual(pkg.dependencies, {'@astrojs/react':'6.0.1',astro:'7.1.3',react:'19.2.7','react-dom':'19.2.7'});
  assert.deepEqual(pkg.devDependencies, {'@axe-core/playwright':'4.12.1','@playwright/test':'1.61.1'});
});
test('ASTRO-FIXTURE-001 reads all four tracked inputs directly without copies', () => {
  const adapter = readFileSync(resolve(candidate, 'src/lib/fixture.mjs'), 'utf8');
  for (const path of ['contracts/data/retail-golden-v1.json','contracts/data/promotion-trust-v1.yaml','tests/fixtures/learning/promotion-trust/evidence-v1.json','tests/fixtures/learning/promotion-trust/manifest.json']) assert.match(adapter, new RegExp(path.replaceAll('/', '\\/')));
  assert.doesNotMatch(adapter, /5282cc6698c34e5d|synthetic-promotion/);
});
test('ASTRO-SEMANTIC-001 emits ten acts, four grains, bounded conclusion and no authority', () => {
  const html = readFileSync(resolve(candidate, 'dist/index.html'), 'utf8');
  assert.equal((html.match(/data-act=/g) ?? []).length, 10);
  for (const grain of ['promo_name, channel','carrier, region_name','reason, category_name, region_name','scenario']) assert.match(html, new RegExp(grain));
  assert.match(html, /insufficient-evidence/); assert.match(html, /no-common-grain/);
  assert.doesNotMatch(html, /completed|promotion_caused|attributed_to/i);
  assert.ok(existsSync(resolve(candidate, 'dist/_astro')));
});
