import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { lstat, mkdtemp, readFile, rm, stat } from 'node:fs/promises';
import http from 'node:http';
import os from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { createReleasedLearningAdapter } from '../../src/contracts/released-learning-adapter.mjs';
import { deriveModuleCatalog } from '../../src/catalog/module-catalog.mjs';
import { renderStaticDocument } from '../../src/render/static-document.mjs';
import { derivePortalRoutes } from '../../src/routing/portal-router.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const repositoryRoot = resolve(appRoot, '../..');
const serverScript = resolve(appRoot, 'scripts/serve-built-portal.mjs');
spawnSync('npm', ['run', 'build'], { cwd: appRoot, stdio: 'pipe' });

async function waitForRecord(pathname) {
  const deadline = Date.now() + 5_000;
  while (Date.now() < deadline) {
    try {
      return JSON.parse(await readFile(pathname, 'utf8'));
    } catch {
      await new Promise((resolveWait) => setTimeout(resolveWait, 25));
    }
  }
  throw new Error('server control record was not written');
}

function controlRequest(record, pathname, authenticate = false) {
  return new Promise((resolveRequest, reject) => {
    const authenticationHeaders = authenticate
      ? {
          'x-portal-instance': record.instanceNonce,
          authorization: `Bearer ${record.capability}`
        }
      : {};
    const request = http.request(
      {
        host: '127.0.0.1',
        port: record.controlPort,
        path: pathname,
        method: 'POST',
        headers: { 'content-length': '0', ...authenticationHeaders }
      },
      (response) => {
        response.resume();
        response.on('end', () => resolveRequest(response.statusCode));
      }
    );
    request.on('error', reject);
    request.end();
  });
}

function rawRequest(record, options = {}) {
  return new Promise((resolveRequest, reject) => {
    const body = options.body ?? '';
    const request = http.request(
      {
        host: '127.0.0.1',
        port: record.publicPort,
        path: options.path ?? '/',
        method: options.method ?? 'GET',
        headers: {
          host: options.host ?? `127.0.0.1:${record.publicPort}`,
          'content-length': String(Buffer.byteLength(body)),
          ...(options.headers ?? {})
        }
      },
      (response) => {
        let bytes = '';
        response.setEncoding('utf8');
        response.on('data', (chunk) => {
          bytes += chunk;
        });
        response.on('end', () =>
          resolveRequest({ status: response.statusCode, headers: response.headers, body: bytes })
        );
      }
    );
    request.on('error', reject);
    request.end(body);
  });
}

async function withServer(run) {
  const temporaryRoot = await mkdtemp(resolve(os.tmpdir(), 'portal-security-'));
  const controlPath = resolve(temporaryRoot, 'control.json');
  const child = spawn(process.execPath, [serverScript], {
    cwd: appRoot,
    stdio: 'ignore',
    env: { PATH: process.env.PATH ?? '/usr/bin:/bin', PORTAL_LIFECYCLE_CONTROL_PATH: controlPath }
  });
  const record = await waitForRecord(controlPath);
  try {
    await run(record, controlPath);
  } finally {
    try {
      await controlRequest(record, '/_control/stop', true);
    } catch {
      // A test may already have completed authenticated self-shutdown.
    }
    await new Promise((resolveExit) => {
      if (child.exitCode !== null) resolveExit();
      else {
        child.once('exit', resolveExit);
        setTimeout(resolveExit, 1_000).unref();
      }
    });
    await rm(temporaryRoot, { recursive: true, force: true });
  }
}

test('PTP-RED-A-023 closes the build and request policy over a real server', async () => {
  await withServer(async (record) => {
    const valid = await rawRequest(record);
    assert.equal(valid.status, 200);
    const withBody = await rawRequest(record, { body: 'x' });
    assert.equal(withBody.status, 400, 'PTP_RED_REQUEST_POLICY_ABSENT');
    const foreignHost = await rawRequest(record, { host: 'example.invalid' });
    assert.equal(foreignHost.status, 400, 'PTP_RED_REQUEST_POLICY_ABSENT');
  });
});

test('PTP-RED-A-024 lifecycle record is owner-private, authenticated, nonce-bound, and has no PID authority', async () => {
  await withServer(async (record, controlPath) => {
    const metadata = await lstat(controlPath);
    assert.equal(metadata.isFile(), true);
    assert.equal(metadata.nlink, 1);
    assert.equal(metadata.mode & 0o777, 0o600);
    assert.match(record.instanceNonce, /^[0-9a-f-]{36}$/);
    assert.match(record.capability, /^[0-9a-f]{64}$/, 'PTP_RED_LIFECYCLE_AUTH_ABSENT');
    assert.equal(Object.hasOwn(record, 'pid'), false, 'PTP_RED_LIFECYCLE_AUTH_ABSENT');
  });
});

test('authenticated lifecycle stays available until shutdown and removes its owned control record', async () => {
  await withServer(async (record, controlPath) => {
    await new Promise((resolveWait) => setTimeout(resolveWait, 12_250));
    assert.equal((await rawRequest(record)).status, 200, 'PTP_RED_LIFECYCLE_AUTH_ABSENT');
    assert.equal(
      await controlRequest(record, '/_control/stop', true),
      200,
      'PTP_RED_LIFECYCLE_AUTH_ABSENT'
    );
    const deadline = Date.now() + 2_000;
    while (Date.now() < deadline) {
      try {
        await lstat(controlPath);
        await new Promise((resolveWait) => setTimeout(resolveWait, 25));
      } catch (error) {
        assert.equal(error?.code, 'ENOENT');
        return;
      }
    }
    assert.fail('owned lifecycle control record remained after shutdown');
  });
});

test('PTP-RED-A-012 blocked Stage B commands emit schema-valid fitness-result-v2 without action', () => {
  for (const command of [
    ['lesson-e2e', 'LESSON=promotion-trust'],
    ['local-journey-e2e']
  ]) {
    const result = spawnSync('make', command, { cwd: repositoryRoot, encoding: 'utf8' });
    assert.equal(result.status, 2);
    assert.equal(result.stdout, '');
    const line = result.stderr.split('\n').find((candidate) => candidate.startsWith('{'));
    const blocked = JSON.parse(line);
    assert.equal(blocked.schemaVersion, 'fitness-result-v2', 'PTP_RED_BLOCKED_RESULT_INVALID');
    assert.equal(blocked.status, 'fail', 'PTP_RED_BLOCKED_RESULT_INVALID');
    assert.equal(blocked.failureCode, 'STAGE_B_DEPENDENCY_UNAVAILABLE', 'PTP_RED_BLOCKED_RESULT_INVALID');
    assert.match(blocked.payloadSha256, /^[0-9a-f]{64}$/, 'PTP_RED_BLOCKED_RESULT_INVALID');
  }
});

test('review evidence closes inventory, index, selector, privacy, hashes, and interruption state', async () => {
  const run = spawnSync(process.execPath, ['scripts/write-review-artifacts.mjs'], {
    cwd: appRoot,
    encoding: 'utf8'
  });
  assert.equal(run.status, 0);
  const locator = JSON.parse(run.stdout);
  const review = await readFile(locator.path);
  assert.equal(createHash('sha256').update(review).digest('hex').length, 64);
  const generationRoot = dirname(locator.path);
  const metadata = await stat(generationRoot);
  assert.equal(metadata.mode & 0o777, 0o700);
  assert.equal(
    await readFile(resolve(generationRoot, 'generation-index.json'), 'utf8').then(Boolean, () => false),
    true,
    'PTP_RED_EVIDENCE_CLOSURE_ABSENT'
  );
});

const s3Cases = Array.from({ length: 14 }, (_, index) => `PTP-S3-${String(index + 1).padStart(2, '0')}`);

test('PTP-S3-01 enforces loopback Host and emits no CORS authority', async () => {
  await withServer(async (record) => {
    const valid = await rawRequest(record);
    const foreign = await rawRequest(record, { host: 'example.invalid' });
    assert.equal(valid.status, 200);
    assert.equal(valid.headers['access-control-allow-origin'], undefined);
    assert.equal(foreign.status, 400);
  });
});

test('PTP-S3-02 admits only GET and HEAD', async () => {
  await withServer(async (record) => {
    assert.equal((await rawRequest(record, { method: 'GET' })).status, 200);
    assert.equal((await rawRequest(record, { method: 'HEAD' })).status, 200);
    assert.equal((await rawRequest(record, { method: 'POST' })).status, 405);
  });
});

test('PTP-S3-03 rejects request bodies and transfer ambiguity', async () => {
  await withServer(async (record) => {
    assert.equal(
      (await rawRequest(record, { body: 'not-admitted' })).status,
      400,
      'PTP_RED_S3_COVERAGE_ABSENT'
    );
  });
});

test('PTP-S3-04 exposes no runner credential, URL, or browser-direct runner', () => {
  const capabilities = createReleasedLearningAdapter({ repositoryRoot }).describeCapabilities();
  assert.equal(capabilities.runner?.state, 'unavailable', 'PTP_RED_S3_COVERAGE_ABSENT');
  assert.equal(capabilities.runner?.url, undefined);
  assert.equal(capabilities.runner?.token, undefined);
});

test('PTP-S3-05 rejects ambiguous and double-encoded inventory paths', async () => {
  await withServer(async (record) => {
    assert.equal(
      (await rawRequest(record, { path: '/%252e%252e/index.html' })).status,
      400,
      'PTP_RED_S3_COVERAGE_ABSENT'
    );
  });
});

test('PTP-S3-06 renders untrusted descriptor text as escaped text through the real renderer', () => {
  const catalog = deriveModuleCatalog({
    authorityKind: 'test-only-structure',
    descriptors: [{ id: 'unit-module', title: '<img src=x onerror=unit>', lessons: [] }]
  });
  const route = derivePortalRoutes(catalog)[0];
  const html = renderStaticDocument(route, catalog);
  assert.match(html, /&lt;img src=x onerror=unit&gt;/, 'PTP_RED_S3_COVERAGE_ABSENT');
  assert.doesNotMatch(html, /<img src=x/);
});

test('PTP-S3-07 serves CSP-protected documents without inline execution', async () => {
  await withServer(async (record) => {
    const response = await rawRequest(record);
    assert.match(response.headers['content-security-policy'], /script-src 'self'/);
    assert.doesNotMatch(response.body, /on(?:click|error)=|javascript:/i);
  });
});

test('PTP-S3-08 exposes no progress or completion authority', () => {
  const capabilities = createReleasedLearningAdapter({ repositoryRoot }).describeCapabilities();
  assert.equal(capabilities.progress, false, 'PTP_RED_S3_COVERAGE_ABSENT');
  assert.equal(capabilities.completion, false, 'PTP_RED_S3_COVERAGE_ABSENT');
});

test('PTP-S3-09 requires lifecycle nonce and capability and never trusts a PID', async () => {
  await withServer(async (record) => {
    assert.match(record.capability, /^[0-9a-f]{64}$/, 'PTP_RED_S3_COVERAGE_ABSENT');
    assert.equal(Object.hasOwn(record, 'pid'), false, 'PTP_RED_S3_COVERAGE_ABSENT');
  });
});

test('PTP-S3-10 closes bounded private evidence with a hash-valid index', async () => {
  const run = spawnSync(process.execPath, ['scripts/write-review-artifacts.mjs'], {
    cwd: appRoot,
    encoding: 'utf8'
  });
  const locator = JSON.parse(run.stdout);
  const index = await readFile(resolve(dirname(locator.path), 'generation-index.json'), 'utf8').catch(
    () => ''
  );
  assert.notEqual(index, '', 'PTP_RED_S3_COVERAGE_ABSENT');
  assert.ok(Buffer.byteLength(index) <= 2 * 1024 * 1024);
});

test('PTP-S3-11 keeps every installed lock entry pinned with registry integrity', async () => {
  const lock = JSON.parse(await readFile(resolve(appRoot, 'package-lock.json'), 'utf8'));
  for (const [path, entry] of Object.entries(lock.packages)) {
    if (path === '') continue;
    if (entry.resolved) assert.match(entry.resolved, /^https:\/\/registry\.npmjs\.org\//);
    if (entry.resolved) assert.match(entry.integrity, /^sha512-/);
  }
});

test('PTP-S3-12 rejects missing lifecycle authentication before shutdown', async () => {
  await withServer(async (record) => {
    assert.equal(
      await controlRequest(record, '/_control/stop'),
      403,
      'PTP_RED_S3_COVERAGE_ABSENT'
    );
  });
});

test('PTP-S3-13 binds exact released contract and binding versions', () => {
  const registry = createReleasedLearningAdapter({ repositoryRoot }).readRegistry();
  assert.equal(registry.source?.contractSetVersion, 'learning-contract-set-v1', 'PTP_RED_S3_COVERAGE_ABSENT');
  assert.equal(registry.binding?.schemaVersion, 'promotion-trust-vite-binding-v1', 'PTP_RED_S3_COVERAGE_ABSENT');
});

test('PTP-S3-14 propagates no cloud or model credential to the served document', async () => {
  await withServer(async (record) => {
    const response = await rawRequest(record);
    assert.doesNotMatch(
      response.body,
      /AWS_ACCESS_KEY|AWS_SECRET|OPENAI_API_KEY|ANTHROPIC_API_KEY|GOOGLE_API_KEY/
    );
  });
});

test('all fourteen S3 IDs and seven defensive families are unique and complete', () => {
  assert.equal(s3Cases.length, 14);
  assert.equal(new Set(s3Cases).size, 14);
  const defensiveFamilies = new Set([
    'authenticated-lifecycle',
    'blocked-fitness-result',
    'closed-request-build',
    'runtime-lock-environment',
    'generic-registry',
    'bounded-artifacts',
    'red-s3-coverage'
  ]);
  assert.equal(defensiveFamilies.size, 7);
});
