import { createHash } from 'node:crypto';
import { readFileSync, realpathSync, statSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), '../../../..'));
const M2 = '24be3b34c6b0fcdbd07c5800dcab349054e34713';
const FULL_SHA = /^[0-9a-f]{40}$/;
export const EXPECTED_IDENTITIES = {
  'contracts/data/retail-golden-v1.json': ['f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc', '2bdd653ced3ce3f69652d2b873f21699e1e1fc81'],
  'contracts/data/promotion-trust-v1.yaml': ['c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe', '876789d549276b44a6e64cc4c9a471886fd2752b'],
  'tests/fixtures/learning/promotion-trust/evidence-v1.json': ['2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5', '6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0'],
  'tests/fixtures/learning/promotion-trust/manifest.json': ['0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341', 'a4b32032962f5f787d733f7de8cf657491944e37'],
};
const GRAINS = [
  ['promo_name', 'channel'],
  ['carrier', 'region_name'],
  ['reason', 'category_name', 'region_name'],
  ['scenario'],
];

function add(failures, id, condition, reason) {
  if (!condition) failures.push({ id, reason });
}

function equal(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

export function validateBarrierSnapshot(snapshot) {
  const failures = [];
  const paths = Object.keys(EXPECTED_IDENTITIES);
  add(failures, 'BARRIER-B-ABSENT', equal(Object.keys(snapshot.identities ?? {}), paths), 'all four exact tracked paths must be present once');
  add(failures, 'BARRIER-B-ANCESTRY', snapshot.mergeSha === M2 && snapshot.mergeIsAncestor === true, 'exact M2 must be an ancestor of the tested tree');
  const actualEntries = paths.map((path) => snapshot.identities?.[path]);
  const crossed = actualEntries.every((identity) => Array.isArray(identity) && identity.length === 2)
    && actualEntries.some((identity, index) => equal(identity, EXPECTED_IDENTITIES[paths.find((path) => equal(EXPECTED_IDENTITIES[path], identity))]) && !equal(identity, EXPECTED_IDENTITIES[paths[index]]));
  add(failures, 'BARRIER-B-CROSSED', !crossed, 'SHA/blob identities may not be crossed between paths');
  add(failures, 'BARRIER-B-TAMPER', actualEntries.some((identity) => !Array.isArray(identity)) || crossed || paths.every((path) => equal(snapshot.identities?.[path], EXPECTED_IDENTITIES[path])), 'each observed SHA-256 and Git blob must match M2');
  const manifest = snapshot.manifest ?? {};
  add(failures, 'BARRIER-B-SCHEMA', manifest.schemaVersion === 'promotion-trust-fixture-manifest-v2' && manifest.portableSchemaValid === true && manifest.portableIntegrityValid === true && manifest.testedTreeIsAncestor === true, 'closed v2 manifest and portable attestation integrity must validate');
  add(failures, 'BARRIER-B-PORTABLE', manifest.integrityScope === 'local-artifact-integrity-only' && manifest.publisherAuthenticity === 'externally-attested-not-claimed', 'portable consumption is local-integrity-only and must not launder publisher authenticity');
  const semantics = snapshot.semantics ?? {};
  add(failures, 'BARRIER-B-ATTRIBUTION', (semantics.crossGrainRelationships ?? []).length === 0 && (semantics.attributionBearingFields ?? []).length === 0, 'cross-grain relationships and attribution-bearing fields are forbidden');
  add(failures, 'BARRIER-B-STALE', paths.every((path) => snapshot.recordedDigests?.[path] === EXPECTED_IDENTITIES[path][0]), 'recorded handoff digests must match current observed bytes');
  add(failures, 'BARRIER-B-GRAINS', equal(semantics.grains, GRAINS) && semantics.conclusion === 'insufficient-evidence' && semantics.reason === 'no-common-grain', 'four exact independent grains and bounded conclusion are required');
  add(failures, 'BARRIER-B-CLEAN', snapshot.trackedClean === true && (snapshot.issueOwnedPathsChanged ?? []).length === 0, 'Issue #7 may not modify dependency-owned inputs');
  return { ok: failures.length === 0, failures };
}

function git(args) { return execFileSync('git', args, { cwd: ROOT, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim(); }
function sha(path) { return createHash('sha256').update(readFileSync(resolve(ROOT, path))).digest('hex'); }
function canonical(value) {
  if (value === null || typeof value === 'boolean' || typeof value === 'string') return JSON.stringify(value);
  if (typeof value === 'number' && Number.isFinite(value)) return JSON.stringify(Object.is(value, -0) ? 0 : value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
  throw new Error('BARRIER-B-SCHEMA: non-canonical JSON value');
}
function payloadHash(value) { const { integrity: _ignored, ...payload } = value; return createHash('sha256').update(canonical(payload)).digest('hex'); }
function exactKeys(value, keys) { return value && equal(Object.keys(value).sort(), [...keys].sort()); }

function portableValid(manifest) {
  const p = manifest.portableRunAttestation;
  if (!p || !exactKeys(p, ['schemaVersion', 'testedTreeSha', 'sourceBundleVerification', 'runs', 'timing', 'equality', 'integrityScope', 'publisherAuthenticity', 'integrity'])) return false;
  if (p.schemaVersion !== 'promotion-trust-portable-run-attestation-v1' || !FULL_SHA.test(p.testedTreeSha ?? '') || !Array.isArray(p.runs) || p.runs.length !== 2) return false;
  if (p.integrity?.canonicalization !== 'rfc8785-jcs-v1' || p.integrity?.algorithm !== 'sha-256' || payloadHash(p) !== p.integrity?.payloadSha256) return false;
  if (p.runs[0].runId === p.runs[1].runId || p.runs[0].finishedMonotonicNs > p.runs[1].startedMonotonicNs) return false;
  if (p.runs.some((run) => run.testedTreeSha !== p.testedTreeSha || run.durationMs !== Math.floor((run.finishedMonotonicNs - run.startedMonotonicNs) / 1e6) || run.durationMs > 300000 || run.projectionSha256 !== run.coreSha256?.['projection.json'])) return false;
  return p.runs[0].projectionSha256 === p.runs[1].projectionSha256
    && p.runs[0].normalizedRawSha256 === p.runs[1].normalizedRawSha256
    && p.timing?.runsSequential === true && p.timing?.maxRunDurationMs === 300000
    && p.timing?.maxPairDurationMs === 600000 && p.timing?.pairDurationMs <= 600000;
}

export function buildBarrierSnapshot(mergeSha = M2) {
  const identities = {};
  for (const path of Object.keys(EXPECTED_IDENTITIES)) {
    const info = statSync(resolve(ROOT, path), { throwIfNoEntry: false });
    if (info?.isFile()) identities[path] = [sha(path), git(['rev-parse', `HEAD:${path}`])];
  }
  const manifest = JSON.parse(readFileSync(resolve(ROOT, 'tests/fixtures/learning/promotion-trust/manifest.json'), 'utf8'));
  const evidence = JSON.parse(readFileSync(resolve(ROOT, 'tests/fixtures/learning/promotion-trust/evidence-v1.json'), 'utf8'));
  let mergeIsAncestor = false;
  let testedTreeIsAncestor = false;
  try { git(['merge-base', '--is-ancestor', mergeSha, 'HEAD']); mergeIsAncestor = true; } catch {}
  try { git(['merge-base', '--is-ancestor', manifest.testedTreeSha, 'HEAD']); testedTreeIsAncestor = true; } catch {}
  const changed = git(['diff', '--name-only', '8869b9238704719caff5140d9412bb7bebcecc6f...HEAD', '--', ...Object.keys(EXPECTED_IDENTITIES)]).split('\n').filter(Boolean);
  const portable = manifest.portableRunAttestation ?? {};
  return {
    mergeSha,
    mergeIsAncestor,
    trackedClean: changed.length === 0,
    issueOwnedPathsChanged: changed,
    identities,
    manifest: {
      schemaVersion: manifest.schemaVersion,
      portableSchemaValid: portableValid(manifest),
      portableIntegrityValid: payloadHash(portable) === portable.integrity?.payloadSha256,
      integrityScope: portable.integrityScope,
      publisherAuthenticity: portable.publisherAuthenticity,
      testedTreeIsAncestor,
    },
    semantics: {
      grains: evidence.sources?.map((source) => source.grain),
      conclusion: evidence.decision?.value,
      reason: evidence.decision?.reason,
      crossGrainRelationships: evidence.relationships ?? [],
      attributionBearingFields: Object.keys(evidence).filter((key) => /caus|attribut/i.test(key)),
    },
    recordedDigests: Object.fromEntries(Object.entries(identities).map(([path, [digest]]) => [path, digest])),
  };
}

function main() {
  const index = process.argv.indexOf('--merge-sha');
  const mergeSha = index === -1 ? M2 : process.argv[index + 1];
  if (!FULL_SHA.test(mergeSha ?? '')) throw new Error('BARRIER-B-ANCESTRY: merge SHA must be full lowercase hex');
  const snapshot = buildBarrierSnapshot(mergeSha);
  const result = validateBarrierSnapshot(snapshot);
  process.stdout.write(`${JSON.stringify({ schemaVersion: 'i5-02-barrier-b-result-v1', resultStatus: result.ok ? 'pass' : 'fail', barrierB: result.ok ? 'closed-executable-pass' : 'open-not-passed', issue6MergeSha: mergeSha, snapshot, failures: result.failures }, null, 2)}\n`);
  if (!result.ok) process.exitCode = 1;
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) main();
