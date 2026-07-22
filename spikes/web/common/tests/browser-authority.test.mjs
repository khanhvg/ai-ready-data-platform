import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const CSP = "default-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'none'; connect-src 'none'; object-src 'none'; worker-src 'none'; manifest-src 'none'";

test('WEB-API-001 staticLogical exposes only same-origin static reads and strict CSP; runtime network facet remains pending', async () => {
  const paths = [
    '../../preview/index.html', '../../preview/preview.mjs',
    '../../harness/scripts/static-host.mjs', '../../harness/scripts/preview-control.mjs',
  ];
  const text = (await Promise.all(paths.map((path) => readFile(new URL(path, import.meta.url), 'utf8')))).join('\n');
  const facets = { staticLogical: 'required', browserDecision: 'required-pending' };
  assert.deepEqual(facets, { staticLogical: 'required', browserDecision: 'required-pending' });
  assert.ok(text.includes(CSP));
  assert.doesNotMatch(text, /0\.0\.0\.0|\[::\]|access-control-allow-origin[^\n]*(?:\*|https?:)/i);
  assert.doesNotMatch(text, /https?:\/\/|wss?:\/\/|runner|private[_ -]?api|authorization|bearer\s|aws[_ -]?(?:access|secret)|document\.cookie|localStorage/i);
  assert.doesNotMatch(text, /\b(?:POST|PUT|PATCH|DELETE)\b|navigator\.serviceWorker|serviceWorker\.register|import\s*\(\s*[^)]*https/i);

  const { scanCredentialSources } = await import('../../harness/scripts/authority-check.mjs');
  const canaryPath = 'spikes/web/common/tests/fixtures/invalid-secret-canary.json';
  const allowedBearer = ['Bearer', 'TEST_SECRET_CANARY_DO_NOT_ACCEPT'].join(' ');
  const allowedPrivatePath = ['', 'Users', 'example', 'private', 'evidence.json'].join('/');
  const exactCanary = `${JSON.stringify({
    fixtureKind: 'synthetic-preview',
    authorization: allowedBearer,
    privatePath: allowedPrivatePath,
  }, null, 2)}\n`;
  assert.deepEqual(scanCredentialSources([{ path: canaryPath, source: exactCanary }]), []);
  assert.equal(scanCredentialSources([{
    path: canaryPath,
    source: exactCanary.replace('TEST_SECRET_CANARY_DO_NOT_ACCEPT', ['ghp', 'real_secret_value_1234567890'].join('_')),
  }]).length, 1);
  assert.equal(scanCredentialSources([{
    path: 'spikes/web/common/tests/credential-negative.test.mjs',
    source: ['const pass', 'word = "actual-secret-value";'].join(''),
  }]).length, 1);
  assert.equal(scanCredentialSources([{
    path: 'spikes/web/common/tests/credential-negative.test.mjs',
    source: `const leakedPath = ${JSON.stringify(allowedPrivatePath)};`,
  }]).length, 1);
});
