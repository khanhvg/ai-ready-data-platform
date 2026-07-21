import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import test from 'node:test';
import { ROOT, contract, scanText, validateChangedPaths, validateEvidenceManifest, validateOwnership } from '../scripts/simple-vite-v3.mjs';

test('V3-07 harness contract closes authority, seven groups, commands, and write paths', () => {
  assert.equal(contract.implementationInputSha, '4cfd01f891655670b5a43a362b1567bcaaf4a824');
  assert.deepEqual(contract.groups, ['V3-01', 'V3-02', 'V3-03', 'V3-04', 'V3-05', 'V3-06', 'V3-07']);
  assert.equal(contract.port, 4175);
  assert.deepEqual(contract.commands.install, ['npm', '--prefix', 'spikes/web/candidates/vite', 'ci', '--ignore-scripts', '--no-audit', '--no-fund']);
  assert.equal(contract.allowedPrefixes.length, 1);
  assert.equal(contract.allowedPrefixes[0], 'spikes/web/evidence/retained/simple-vite-v3/');
  assert.deepEqual(validateChangedPaths(['spikes/web/candidates/next/src/page.jsx', '.github/workflows/v3.yml', 'contracts/data/retail-golden-v1.json']), ['spikes/web/candidates/next/src/page.jsx', '.github/workflows/v3.yml', 'contracts/data/retail-golden-v1.json']);
});

test('V3-07 S3 scanner rejects credentials, private paths, PII, injection, and remote imports', () => {
  const samples = [
    ['token="abcdefghijk"', 'credential'],
    ['-----BEGIN PRIVATE KEY-----', 'privateKey'],
    ['/Users/private/work/repo', 'absolutePrivatePath'],
    ['learner@example.com', 'email'],
    ['element.innerHTML = value', 'unsafeInjection'],
    ['import("https://example.com/a.js")', 'remoteImport'],
  ];
  for (const [sample, id] of samples) assert.ok(scanText(sample).includes(id), id);
  assert.deepEqual(scanText('sanitized aggregate; insufficient-evidence; no-common-grain'), []);
});

test('V3-07 ownership ledger fails closed on foreign port, missing fingerprint, and run mismatch', () => {
  const valid = { pid: 123, processGroup: 123, fingerprint: 'start command', cwd: '.', command: ['node', 'host'], root: 'spikes/web/candidates/vite/dist', port: 4175, runId: 'owned-run', childHandle: true };
  assert.deepEqual(validateOwnership(valid, { runId: 'owned-run' }), []);
  assert.ok(validateOwnership({ ...valid, port: 4174 }, { runId: 'owned-run' }).includes('wrong-port'));
  assert.ok(validateOwnership({ ...valid, fingerprint: '' }, { runId: 'owned-run' }).includes('missing-fingerprint'));
  assert.ok(validateOwnership(valid, { runId: 'foreign-run' }).includes('wrong-run-id'));
});

test('V3-07 retained manifest is closed over exact-head RED, 7/7, redaction, and rollback', () => {
  const base = {
    schemaVersion: 'i5-02-simple-vite-v3-evidence-v1', acceptanceRevision: contract.acceptanceRevision,
    implementationInputSha: contract.implementationInputSha, testedSourceSha: 'a'.repeat(40), testedTreeSha: 'b'.repeat(40),
    groups: contract.groups.map(id => ({ id, result: 'pass' })), redProvenance: { result: 'pass' }, redaction: { result: 'pass' }, cleanupRollback: { result: 'pass' },
    artifactLocators: {
      journeyFacts: ['green/browser-results/chromium-desktop/v3-03-v3-04-journey-facts.json', 'green/browser-results/chromium-narrow/v3-03-v3-04-journey-facts.json'],
      axe: 'green/browser-results/chromium-desktop/v3-05-axe-complete.json',
      noJsInventory: 'green/browser-results/chromium-desktop/v3-06-no-js-inventory.json',
      noJsResponse: 'green/browser-results/chromium-desktop/v3-06-response.html',
    },
    testNameInventory: ['V3-02 contract', 'V3-03 V3-04 journey [chromium-desktop]', 'V3-05 axe [chromium-desktop]', 'V3-06 no-JS [chromium-desktop]', 'V3-03 V3-04 journey [chromium-narrow]'],
    axeSummary: { invocations: 1, critical: 0, serious: 0, findingsRetained: true },
    noJsFacts: { javaScriptEnabled: false, responseBytes: 1, csp: "default-src 'self'", inventoryCount: 13 },
    scanSummary: { result: 'pass', findings: 0 },
    ownedResourceSummary: { result: 'pass', serverCount: 1, port: 4175, cleanup: 'pass', rollbackSimulation: 'pass' },
  };
  assert.deepEqual(validateEvidenceManifest(base), []);
  assert.ok(validateEvidenceManifest({ ...base, groups: base.groups.slice(0, 6) }).includes('groups'));
  assert.ok(validateEvidenceManifest({ ...base, redProvenance: { result: 'fail' } }).includes('red-provenance'));
  assert.ok(validateEvidenceManifest({ ...base, cleanupRollback: { result: 'fail' } }).includes('rollback'));
  for (const [field, failureId] of [
    ['artifactLocators', 'artifact-locators'],
    ['testNameInventory', 'test-name-inventory'],
    ['axeSummary', 'axe-summary'],
    ['noJsFacts', 'no-js-facts'],
    ['scanSummary', 'scan-summary'],
    ['ownedResourceSummary', 'owned-resource-summary'],
  ]) {
    const missing = { ...base };
    delete missing[field];
    assert.ok(validateEvidenceManifest(missing).includes(failureId), `missing ${field} must fail closed as ${failureId}`);
  }
});

test('V3-07 runner contains bounded commands and never imports comparison, native, timer, or cloud paths', () => {
  const source = readFileSync(resolve(ROOT, 'spikes/web/harness/scripts/simple-vite-v3.mjs'), 'utf8');
  assert.match(source, /setTimeout/);
  assert.match(source, /refusing to signal/);
  assert.match(source, /ownedRollbackSentinel/, 'runner must retain evidence that an owned rollback sentinel was removed');
  assert.match(source, /unownedRollbackSentinel/, 'runner must retain evidence that an unowned rollback sentinel was preserved');
  assert.match(source, /retainedPreservation/, 'runner must verify retained evidence survives rollback');
  assert.doesNotMatch(source, /score-anchors|Firefox|webkit|VoiceOver|CuaDriver|terraform|historicalTimer/i);
});
