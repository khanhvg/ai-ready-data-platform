import assert from 'node:assert/strict';
import test from 'node:test';
import { pathToFileURL } from 'node:url';

const CHECKER_URL = pathToFileURL(new URL('../scripts/barrier-b-check.mjs', import.meta.url).pathname).href;
const M2 = '24be3b34c6b0fcdbd07c5800dcab349054e34713';
const identities = {
  'contracts/data/retail-golden-v1.json': ['f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc', '2bdd653ced3ce3f69652d2b873f21699e1e1fc81'],
  'contracts/data/promotion-trust-v1.yaml': ['c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe', '876789d549276b44a6e64cc4c9a471886fd2752b'],
  'tests/fixtures/learning/promotion-trust/evidence-v1.json': ['2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5', '6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0'],
  'tests/fixtures/learning/promotion-trust/manifest.json': ['0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341', 'a4b32032962f5f787d733f7de8cf657491944e37'],
};

function valid() {
  return {
    mergeSha: M2,
    mergeIsAncestor: true,
    trackedClean: true,
    issueOwnedPathsChanged: [],
    identities: structuredClone(identities),
    manifest: {
      schemaVersion: 'promotion-trust-fixture-manifest-v2',
      portableSchemaValid: true,
      portableIntegrityValid: true,
      integrityScope: 'local-artifact-integrity-only',
      publisherAuthenticity: 'externally-attested-not-claimed',
      testedTreeIsAncestor: true,
    },
    semantics: {
      grains: [
        ['promo_name', 'channel'],
        ['carrier', 'region_name'],
        ['reason', 'category_name', 'region_name'],
        ['scenario'],
      ],
      conclusion: 'insufficient-evidence',
      reason: 'no-common-grain',
      crossGrainRelationships: [],
      attributionBearingFields: [],
    },
    recordedDigests: Object.fromEntries(Object.entries(identities).map(([path, [sha256]]) => [path, sha256])),
  };
}

async function checker() {
  try { return await import(CHECKER_URL); }
  catch (error) {
    if (error?.code === 'ERR_MODULE_NOT_FOUND') assert.fail('BARRIER-B-RED: missing live Barrier B checker');
    throw error;
  }
}

async function fails(id, mutate) {
  const { validateBarrierSnapshot } = await checker();
  const snapshot = valid();
  mutate(snapshot);
  const result = validateBarrierSnapshot(snapshot);
  assert.equal(result.ok, false);
  assert.deepEqual(result.failures.map((failure) => failure.id), [id]);
}

test('BARRIER-B-ABSENT rejects an absent dependency input', () => fails('BARRIER-B-ABSENT', (s) => { delete s.identities[Object.keys(identities)[0]]; }));
test('BARRIER-B-ANCESTRY rejects an unmerged M2', () => fails('BARRIER-B-ANCESTRY', (s) => { s.mergeIsAncestor = false; }));
test('BARRIER-B-CROSSED rejects crossed path identities', () => fails('BARRIER-B-CROSSED', (s) => { const keys = Object.keys(identities); [s.identities[keys[0]], s.identities[keys[1]]] = [s.identities[keys[1]], s.identities[keys[0]]]; }));
test('BARRIER-B-TAMPER rejects a changed SHA or blob', () => fails('BARRIER-B-TAMPER', (s) => { s.identities[Object.keys(identities)[2]][0] = '0'.repeat(64); }));
test('BARRIER-B-SCHEMA rejects schema-invalid v2 input', () => fails('BARRIER-B-SCHEMA', (s) => { s.manifest.portableSchemaValid = false; }));
test('BARRIER-B-PORTABLE rejects non-portable or authenticity-laundered input', () => fails('BARRIER-B-PORTABLE', (s) => { s.manifest.integrityScope = 'publisher-authenticity'; }));
test('BARRIER-B-ATTRIBUTION rejects attribution-bearing cross-grain input', () => fails('BARRIER-B-ATTRIBUTION', (s) => { s.semantics.attributionBearingFields = ['promotion_caused_returns']; }));
test('BARRIER-B-STALE rejects stale recorded digests', () => fails('BARRIER-B-STALE', (s) => { s.recordedDigests[Object.keys(identities)[3]] = 'f'.repeat(64); }));
test('BARRIER-B-GRAINS requires four exact independent grains and bounded conclusion', () => fails('BARRIER-B-GRAINS', (s) => { s.semantics.grains[1] = ['promo_name', 'carrier']; }));
test('BARRIER-B-CLEAN rejects Issue #7 edits to dependency-owned paths', () => fails('BARRIER-B-CLEAN', (s) => { s.issueOwnedPathsChanged = [Object.keys(identities)[0]]; }));
