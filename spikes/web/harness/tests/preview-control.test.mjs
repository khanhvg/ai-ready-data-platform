import assert from 'node:assert/strict';
import { once } from 'node:events';
import { createConnection, createServer } from 'node:net';
import { spawnSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const INPUT_SHA = '0c73f4712c8ac7902042735ff1da96ef1e5285a3';
const IMMUTABLE_ANCESTORS = [
  'e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9',
  '0890c4abab46f81d110be6cbd6de3560e631a735',
  'a39251d45a56124322b9143ad16b926b2656073b',
  'f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c',
  'e440c5855732d5d8f5d634e3cc1359c010cc5ed3',
  '0486642528b9a6ba8e96cee18d6eda76c3b5deb9',
];
const FIXTURE_DIGEST = 'sha256:572c052ff546d19dab35ef988bba8da7ecc70b808c7c91caeea7fd453703c9de';
const NOTICE = 'SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE';
const controlUrl = new URL('../scripts/preview-control.mjs', import.meta.url);
const hostUrl = new URL('../scripts/static-host.mjs', import.meta.url);
const repoRoot = new URL('../../../..', import.meta.url).pathname;

async function control() {
  return import(controlUrl);
}

async function host() {
  return import(hostUrl);
}

function command(args) {
  return spawnSync(process.execPath, [controlUrl.pathname, ...args], {
    cwd: repoRoot,
    encoding: 'utf8',
    timeout: 12_000,
  });
}

async function listen() {
  const server = createServer((socket) => socket.end('still-owned-by-test'));
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  return { server, port: server.address().port };
}

async function connect(port) {
  const socket = createConnection({ host: '127.0.0.1', port });
  await once(socket, 'connect');
  socket.end();
}

function validLocator(port = 4174) {
  return {
    pid: 4242,
    processGroup: 4242,
    processStartFingerprint: 'start:123456',
    commandHash: 'sha256:preview-command',
    cwd: 'repo-relative:root',
    realRoot: 'spikes/web/preview',
    host: '127.0.0.1',
    port,
    runId: 'gate-a-lifecycle-test',
    fixtureDigest: FIXTURE_DIGEST,
    implementationInput: INPUT_SHA,
  };
}

test('GA-LIFE-001 invalid port/no scan — lifecycle rejects invalid ports without scanning or selecting a replacement', async () => {
  const { validatePort } = await control();
  for (const value of ['0', '-1', '65536', '4174.5', 'abc', '', 0, 65536]) {
    assert.deepEqual(validatePort(value), { ok: false, code: 'INVALID_PORT' });
  }
});

test('GA-LIFE-002 occupied test-owned port/no signal — lifecycle failure never signals or replaces the listener', async (t) => {
  const { server, port } = await listen();
  t.after(() => server.close());
  const result = command(['start', '--lesson', 'promotion-trust', '--port', String(port), '--implementation-input', INPUT_SHA]);
  assert.notEqual(result.status, 0);
  assert.match(`${result.stdout}\n${result.stderr}`, /PORT_OCCUPIED/);
  assert.equal(server.listening, true);
  await connect(port);
  assert.equal(server.listening, true);
});

test('GA-LIFE-003 fixed 10-second timeout/scoped attempted-group cleanup', async () => {
  const { READINESS_TIMEOUT_MS, awaitReadiness } = await control();
  assert.equal(READINESS_TIMEOUT_MS, 10_000);
  const stopped = [];
  const result = await awaitReadiness({
    runId: 'timeout-test',
    deadlineMs: READINESS_TIMEOUT_MS,
    probe: async () => ({ ready: false }),
    clock: (() => { let now = 0; return () => (now += 5_000); })(),
    stopAttemptProcessGroup: async (processGroup) => stopped.push(processGroup),
    attemptedProcessGroup: 8123,
  });
  assert.deepEqual(result, { ok: false, code: 'READINESS_TIMEOUT', timeoutMs: 10_000 });
  assert.deepEqual(stopped, [8123]);

  let now = 0;
  const lateStopped = [];
  const late = await awaitReadiness({
    runId: 'late-ready-test',
    deadlineMs: READINESS_TIMEOUT_MS,
    probe: async () => {
      now = READINESS_TIMEOUT_MS + 1;
      return { ready: true, runId: 'late-ready-test' };
    },
    clock: () => now,
    wait: async () => {},
    stopAttemptProcessGroup: async (processGroup) => lateStopped.push(processGroup),
    attemptedProcessGroup: 8125,
  });
  assert.deepEqual(late, { ok: false, code: 'READINESS_TIMEOUT', timeoutMs: 10_000 });
  assert.deepEqual(lateStopped, [8125]);
});

test('GA-LIFE-004 surviving attempted process is reported', async () => {
  const { awaitReadiness } = await control();
  const result = await awaitReadiness({
    runId: 'timeout-survivor',
    deadlineMs: 10_000,
    probe: async () => ({ ready: false }),
    clock: (() => { let now = 0; return () => (now += 5_000); })(),
    wait: async () => {},
    stopAttemptProcessGroup: async () => {},
    attemptedProcessGroup: 8124,
    processAlive: async () => true,
  });
  assert.deepEqual(result, { ok: false, code: 'ATTEMPTED_PROCESS_SURVIVED_CLEANUP', timeoutMs: 10_000 });
});

test('GA-LIFE-005 stale/reused PID and locator-field mismatch/no signal', async () => {
  const { validateLocatorIdentity } = await control();
  const locator = validLocator();
  const observed = { ...locator };
  const fields = [
    'pid', 'processGroup', 'processStartFingerprint', 'commandHash', 'cwd', 'realRoot',
    'host', 'port', 'runId', 'fixtureDigest', 'implementationInput',
  ];
  for (const field of fields) {
    const changed = { ...observed, [field]: field === 'pid' || field === 'port' ? observed[field] + 1 : `${observed[field]}-wrong` };
    const result = validateLocatorIdentity(locator, changed, {
      implementationInput: INPUT_SHA,
      expectedRunId: locator.runId,
      expectedFixtureDigest: locator.fixtureDigest,
    });
    assert.equal(result.ok, false, field);
    assert.equal(result.code, 'LOCATOR_IDENTITY_MISMATCH', field);
    assert.ok(result.mismatches.includes(field), field);
    assert.equal(result.maySignal, false, field);
  }
});

test('GA-LIFE-006 exact route/path/symlink/traversal/query/method rejection', async () => {
  const { validateRequestTarget, validateResolvedAsset } = await host();
  for (const [method, target] of [
    ['POST', '/'], ['PUT', '/index.html'], ['GET', '/unknown'], ['GET', '/.env'],
    ['GET', '/../index.html'], ['GET', '/%2e%2e/index.html'], ['GET', '/%252e%252e/index.html'],
    ['GET', '/preview.css?theme=remote'], ['GET', '//private.example/path'], ['HEAD', '/preview.mjs'],
  ]) {
    assert.equal(validateRequestTarget(method, target).ok, false, `${method} ${target}`);
  }
  assert.equal(validateRequestTarget('GET', '/').ok, true);
  assert.equal(validateRequestTarget('GET', '/index.html').ok, true);
  assert.equal(validateRequestTarget('GET', '/preview.css').ok, true);
  assert.equal(validateRequestTarget('GET', '/preview.mjs').ok, true);
  assert.equal(validateRequestTarget('GET', '/__i5_02_ready').ok, true);
  assert.equal(validateResolvedAsset({ realRoot: '/safe/preview', resolvedPath: '/safe/preview-link/index.html', isSymlink: true }).ok, false);
  assert.equal(validateResolvedAsset({ realRoot: '/safe/preview', resolvedPath: '/safe/outside/index.html', isSymlink: false }).ok, false);
});

test('GA-LIFE-007 wrong lesson or fixture digest rejected', async () => {
  const { validateStartRequest, resetCheck } = await control();
  assert.equal(validateStartRequest({ lesson: 'other', fixtureDigest: 'sha256:fixture', implementationInput: INPUT_SHA }).code, 'LESSON_REJECTED');
  assert.equal(validateStartRequest({ lesson: 'promotion-trust', fixtureDigest: 'sha256:wrong', implementationInput: INPUT_SHA }).code, 'FIXTURE_DIGEST_MISMATCH');
  const result = await resetCheck({ lesson: 'other', implementationInput: INPUT_SHA });
  assert.deepEqual(result, { ok: false, code: 'LESSON_REJECTED' });
});

test('GA-LIFE-008 only new audited input and canonical fixture digest accepted', async () => {
  const { validateStartRequest } = await control();
  for (const ancestor of IMMUTABLE_ANCESTORS) {
    const ancestry = spawnSync('git', ['merge-base', '--is-ancestor', ancestor, INPUT_SHA], {
      cwd: repoRoot,
      encoding: 'utf8',
    });
    assert.equal(ancestry.status, 0, `missing immutable ancestor ${ancestor}`);
  }
  assert.equal(validateStartRequest({ lesson: 'promotion-trust', fixtureDigest: FIXTURE_DIGEST, implementationInput: INPUT_SHA }).ok, true);
  assert.equal(validateStartRequest({ lesson: 'promotion-trust', fixtureDigest: FIXTURE_DIGEST, implementationInput: 'a'.repeat(40) }).code, 'IMPLEMENTATION_INPUT_REJECTED');
  assert.equal(validateStartRequest({ lesson: 'promotion-trust', fixtureDigest: 'sha256:' + 'b'.repeat(64), implementationInput: INPUT_SHA }).code, 'FIXTURE_DIGEST_MISMATCH');
});

test('GA-LIFE-009 double reset/baseline/audit counter/history contract', async () => {
  const { resetCheck } = await control();
  const result = await resetCheck({ lesson: 'promotion-trust', implementationInput: INPUT_SHA });
  assert.equal(result.ok, true);
  assert.equal(result.firstResettableDigest, result.baselineDigest);
  assert.equal(result.secondResettableDigest, result.baselineDigest);
  assert.equal(result.firstResetAuditCount, result.initialResetAuditCount + 1);
  assert.equal(result.secondResetAuditCount, result.firstResetAuditCount + 1);
  assert.equal(result.historyMode, 'replace');
  assert.equal(result.notice, NOTICE);
});

test('GA-LIFE-010 down without locator is idempotent/no signal', async () => {
  const { downPreview } = await control();
  const signals = [];
  const result = await downPreview({
    port: 4174,
    implementationInput: INPUT_SHA,
    readLocator: async () => null,
    signalProcessGroup: async (...args) => signals.push(args),
  });
  assert.deepEqual(result, { ok: true, code: 'ALREADY_DOWN' });
  assert.deepEqual(signals, []);
});

test('GA-LIFE-011 foreign listener or locator mismatch/no signal', async () => {
  const { downPreview } = await control();
  const signals = [];
  const locator = validLocator();
  const result = await downPreview({
    port: locator.port,
    implementationInput: INPUT_SHA,
    readLocator: async () => locator,
    observeProcess: async () => ({ ...locator, runId: 'foreign-run' }),
    probeReadiness: async () => ({ ready: true, runId: 'foreign-run' }),
    signalProcessGroup: async (...args) => signals.push(args),
  });
  assert.equal(result.ok, false);
  assert.equal(result.code, 'LOCATOR_IDENTITY_MISMATCH');
  assert.deepEqual(signals, []);
});

test('GA-LIFE-012 observed authority binds fixed host/requested port', async () => {
  const { downPreview } = await control();
  const requestedPort = 4174;
  const locator = { ...validLocator(requestedPort), host: '127.0.0.2', port: requestedPort + 1 };
  const signals = [];
  let observedRequest;
  const result = await downPreview({
    port: requestedPort,
    implementationInput: INPUT_SHA,
    readLocator: async () => locator,
    observeProcess: async (candidate, expectations) => {
      observedRequest = expectations;
      return { ...candidate, host: '127.0.0.1', port: expectations.requestedPort };
    },
    probeReadiness: async () => ({ ready: true, runId: locator.runId }),
    signalProcessGroup: async (...args) => signals.push(args),
  });
  assert.deepEqual(observedRequest, { requestedPort });
  assert.equal(result.ok, false);
  assert.equal(result.code, 'LOCATOR_IDENTITY_MISMATCH');
  assert.ok(result.mismatches.includes('host'));
  assert.ok(result.mismatches.includes('port'));
  assert.deepEqual(signals, []);
});

test('GA-LIFE-013 surviving verified owned process is reported', async () => {
  const { downPreview } = await control();
  const locator = validLocator();
  const signals = [];
  const result = await downPreview({
    port: locator.port,
    implementationInput: INPUT_SHA,
    readLocator: async () => locator,
    observeProcess: async () => ({ ...locator }),
    probeReadiness: async () => ({ ready: true, runId: locator.runId }),
    signalProcessGroup: async (group, signal) => signals.push([group, signal]),
    processAlive: async () => true,
    wait: async () => {},
  });
  assert.equal(result.ok, false);
  assert.equal(result.code, 'OWNED_PROCESS_SURVIVED_SHUTDOWN');
  assert.ok(signals.length >= 1);
  assert.ok(signals.every(([group]) => group === locator.processGroup));

  const groupedLocator = { ...validLocator(), processGroup: 5151 };
  const checkedGroups = [];
  const stopped = await downPreview({
    port: groupedLocator.port,
    implementationInput: INPUT_SHA,
    readLocator: async () => groupedLocator,
    observeProcess: async () => ({ ...groupedLocator }),
    probeReadiness: async () => ({ ready: true, runId: groupedLocator.runId }),
    signalProcessGroup: async () => {},
    processAlive: async (processGroup) => { checkedGroups.push(processGroup); return false; },
    wait: async () => {},
  });
  assert.deepEqual(stopped, { ok: true, code: 'STOPPED' });
  assert.deepEqual(checkedGroups, [groupedLocator.processGroup]);
});

test('GA-LIFE-014 readiness binds lesson/digest/run/input', async () => {
  const fixture = JSON.parse(await readFile(new URL('../../common/fixtures/synthetic-promotion-trust-v1.json', import.meta.url), 'utf8'));
  const { createReadinessPayload, validateReadinessPayload } = await host();
  const { awaitReadiness } = await control();
  const expected = {
    lesson: 'promotion-trust',
    fixtureDigest: fixture.fixtureDigest,
    runId: 'gate-a-bind-test',
    implementationInput: INPUT_SHA,
  };
  const payload = createReadinessPayload(expected);
  assert.equal(validateReadinessPayload(payload, expected).ok, true);
  for (const field of ['lesson', 'fixtureDigest', 'runId', 'implementationInput']) {
    assert.equal(validateReadinessPayload({ ...payload, [field]: `${payload[field]}-wrong` }, expected).ok, false, field);
  }
  const stopped = [];
  let now = 0;
  const wrongIdentity = await awaitReadiness({
    runId: expected.runId,
    expectedReadiness: expected,
    deadlineMs: 10_000,
    probe: async () => ({ ...payload, lesson: 'other' }),
    clock: () => (now += 5_000),
    wait: async () => {},
    stopAttemptProcessGroup: async (processGroup) => stopped.push(processGroup),
    attemptedProcessGroup: 8126,
  });
  assert.deepEqual(wrongIdentity, { ok: false, code: 'READINESS_TIMEOUT', timeoutMs: 10_000 });
  assert.deepEqual(stopped, [8126]);
});

test('GA-LIFE-015 canonical fixture bytes/digest validation', async () => {
  const bytes = await readFile(new URL('../../common/fixtures/synthetic-promotion-trust-v1.json', import.meta.url));
  const { validateFixtureBytes } = await control();
  const valid = validateFixtureBytes(bytes);
  assert.deepEqual(valid, { ok: true, fixtureDigest: FIXTURE_DIGEST });
  const changed = Buffer.from(bytes.toString('utf8').replace('Tia Hè', 'Tia Thu'));
  assert.equal(validateFixtureBytes(changed).code, 'FIXTURE_DIGEST_MISMATCH');
  assert.equal(validateFixtureBytes(Buffer.from('{')).code, 'FIXTURE_UNAVAILABLE');
});

test('GA-LIFE-016 redirect rejection and fixed host authority', async () => {
  const controllerSource = await readFile(controlUrl, 'utf8');
  assert.match(controllerSource, /redirect\s*:\s*['"]error['"]/);
  const { validateHostAuthority } = await host();
  assert.equal(validateHostAuthority({ lesson: 'promotion-trust', fixtureDigest: FIXTURE_DIGEST, implementationInput: INPUT_SHA, runId: 'gate-a-safe' }).ok, true);
  assert.equal(validateHostAuthority({ lesson: 'promotion-trust', fixtureDigest: FIXTURE_DIGEST, implementationInput: 'a'.repeat(40), runId: 'gate-a-safe' }).code, 'IMPLEMENTATION_INPUT_REJECTED');
});

test('GA-LIFE-017 real asset rejects symlink/outside/non-regular before read', async () => {
  const { readVerifiedAsset } = await host();
  let reads = 0;
  const hooks = {
    lstatAsset: async () => ({ isSymbolicLink: () => false, isFile: () => true }),
    realpathAsset: async () => '/outside/preview.mjs',
    readAsset: async () => { reads += 1; return Buffer.from('unsafe'); },
  };
  const outside = await readVerifiedAsset('/preview.mjs', hooks);
  assert.equal(outside.code, 'PATH_REJECTED');
  assert.equal(reads, 0);
  const symlink = await readVerifiedAsset('/preview.mjs', {
    ...hooks,
    lstatAsset: async () => ({ isSymbolicLink: () => true, isFile: () => true }),
  });
  assert.equal(symlink.code, 'SYMLINK_REJECTED');
  assert.equal(reads, 0);
  const swapped = await readVerifiedAsset('/preview.mjs', {
    lstatAsset: async () => ({ isSymbolicLink: () => false, isFile: () => true }),
    realpathAsset: async () => new URL('../../preview/preview.mjs', import.meta.url).pathname,
    openAsset: async () => {
      const error = new Error('swapped to symlink');
      error.code = 'ELOOP';
      throw error;
    },
    readAsset: async () => { reads += 1; return Buffer.from('unsafe'); },
  });
  assert.equal(swapped.code, 'SYMLINK_REJECTED');
  assert.equal(reads, 0);
  const hostSource = await readFile(hostUrl, 'utf8');
  assert.match(hostSource, /O_NOFOLLOW/);
  assert.match(hostSource, /handle\.readFile\(\)/);
  assert.doesNotMatch(hostSource, /readAsset\(resolvedPath\)/);
});
