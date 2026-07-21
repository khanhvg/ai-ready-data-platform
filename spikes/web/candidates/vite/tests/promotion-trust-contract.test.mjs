import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import test from 'node:test';

const root = resolve(import.meta.dirname, '../../../../..');
const candidate = resolve(root, 'spikes/web/candidates/vite');
const contractPath = resolve(candidate, 'src/lesson-contract.mjs');
const identities = {
  'contracts/data/retail-golden-v1.json': 'f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc',
  'contracts/data/promotion-trust-v1.yaml': 'c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe',
  'tests/fixtures/learning/promotion-trust/evidence-v1.json': '2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5',
  'tests/fixtures/learning/promotion-trust/manifest.json': '0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341',
};
const expectedGrains = [
  ['promotion', 'promo_name × channel', 'Promotion aggregates cannot identify fulfillment, returns, or data-quality causes.'],
  ['fulfillment', 'carrier × region_name', 'No shared key permits attribution to a promotion.'],
  ['returns', 'reason × category_name × region_name', 'No shared key permits attribution to a promotion.'],
  ['data-quality', 'scenario', 'Scenario evidence is independent and does not establish a cause.'],
];

async function lessonContract() {
  assert.equal(existsSync(contractPath), true, 'src/lesson-contract.mjs must exist before GREEN');
  const module = await import(`${new URL(`file://${contractPath}`).href}?v3-contract-test`);
  assert.ok(module.lessonContract, 'lessonContract named export is required');
  return module.lessonContract;
}

test('V3-02 fixture SHA-256 identities and independent source grains are exact', () => {
  for (const [path, expected] of Object.entries(identities)) {
    assert.equal(createHash('sha256').update(readFileSync(resolve(root, path))).digest('hex'), expected, path);
  }
  const evidence = JSON.parse(readFileSync(resolve(root, 'tests/fixtures/learning/promotion-trust/evidence-v1.json')));
  assert.deepEqual(evidence.sources.map(({ grain }) => grain.join(' × ')), expectedGrains.map(([, grain]) => grain));
  assert.deepEqual(evidence.decision, { reason: 'no-common-grain', value: 'insufficient-evidence' });
  assert.equal(evidence.sources.some(({ grain }) => grain.includes('promotion_id')), false);
});

test('V3-02 lesson contract names the Vietnamese representative entry and four evidence limitations', async () => {
  const contract = await lessonContract();
  assert.equal(contract.language, 'vi');
  assert.equal(contract.title, 'Can this promotion headline be trusted?');
  assert.equal(contract.notice, 'TRACKED REAL FIXTURE — UNSCORED — CANNOT COMPLETE');
  assert.deepEqual(contract.grains.map(({ id, value, limitation }) => [id, value, limitation]), expectedGrains);
});

test('V3-02 controlled failure, conclusion, reset baseline, and reflection are exact and non-attributing', async () => {
  const contract = await lessonContract();
  assert.equal(contract.status.baseline, 'Exploration is reversible and unverified.');
  assert.equal(contract.status.failure, 'Controlled failure: no common grain; no answer, attribution, completion, or score saved.');
  assert.equal(contract.status.reset, 'Reset: baseline restored; no answer, attribution, completion, or score persisted.');
  assert.deepEqual(contract.decision, { value: 'insufficient-evidence', reason: 'no-common-grain' });
  assert.deepEqual(contract.relationships, []);
  assert.deepEqual(contract.attribution, []);
  assert.equal(contract.reflection, 'Reflection: What additional common-grain evidence would be needed before making a causal claim?');
  assert.equal(contract.noJsResetLimitation, 'Without JavaScript, reset is unavailable; all facts remain in their baseline state.');
});

test('V3-02 authored fallback exposes the complete contract in response bytes before React', async () => {
  const html = readFileSync(resolve(candidate, 'index.html'), 'utf8');
  const contract = await lessonContract();
  assert.match(html, /<html\s+lang="vi"/);
  for (const token of [contract.title, contract.notice, contract.status.baseline, ...contract.grains.flatMap(g => [g.value, g.limitation]), contract.decision.value, contract.decision.reason, contract.noJsResetLimitation, contract.reflection]) {
    assert.ok(html.includes(token), `missing static fallback token: ${token}`);
  }
  assert.match(html, /data-testid="lesson-entry"/);
  assert.match(html, /data-testid="lesson-status"/);
  assert.doesNotMatch(html, /dangerouslySetInnerHTML|\bonclick\s*=|https?:\/\//i);
});
