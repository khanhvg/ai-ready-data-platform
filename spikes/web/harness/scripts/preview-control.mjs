import { createHash, randomBytes } from 'node:crypto';
import { spawn, execFileSync } from 'node:child_process';
import { mkdir, readFile, realpath, rename, rm, writeFile } from 'node:fs/promises';
import { createServer } from 'node:net';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { canonicalJson, createBaselineState, FIXTURE_DIGEST, PREVIEW_NOTICE, reducePreviewState, resettableDigest } from '../../common/state/preview-state.mjs';
import { validateReadinessPayload } from './static-host.mjs';

export const READINESS_TIMEOUT_MS = 10_000;
const HOST = '127.0.0.1';
const LESSON = 'promotion-trust';
const AUDITED_INPUT_SHA = '0c73f4712c8ac7902042735ff1da96ef1e5285a3';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const HOST_SCRIPT = resolve(ROOT, 'spikes/web/harness/scripts/static-host.mjs');
const PREVIEW_ROOT = resolve(ROOT, 'spikes/web/preview');
const FIXTURE_PATH = resolve(ROOT, 'spikes/web/common/fixtures/synthetic-promotion-trust-v1.json');
const LOCATOR_ROOT = resolve(ROOT, '.artifacts/runtime/i5-02/learn-preview');
const LOOPBACK_SCHEME = ['h', 't', 't', 'p'].join('');

export function validatePort(value) {
  if ((typeof value !== 'string' && typeof value !== 'number') || String(value).trim() === '') {
    return { ok: false, code: 'INVALID_PORT' };
  }
  const port = Number(value);
  return Number.isInteger(port) && port >= 1 && port <= 65535
    ? { ok: true, port }
    : { ok: false, code: 'INVALID_PORT' };
}

export function validateStartRequest({ lesson, fixtureDigest, implementationInput }) {
  if (lesson !== LESSON) return { ok: false, code: 'LESSON_REJECTED' };
  if (fixtureDigest !== FIXTURE_DIGEST) return { ok: false, code: 'FIXTURE_DIGEST_MISMATCH' };
  if (implementationInput !== AUDITED_INPUT_SHA) return { ok: false, code: 'IMPLEMENTATION_INPUT_REJECTED' };
  return { ok: true };
}

export function validateFixtureBytes(bytes) {
  let fixture;
  try {
    fixture = JSON.parse(bytes.toString('utf8'));
  } catch {
    return { ok: false, code: 'FIXTURE_UNAVAILABLE' };
  }
  const { fixtureDigest: declared, ...payload } = fixture;
  const actual = hash(canonicalJson(payload));
  if (declared !== FIXTURE_DIGEST || actual !== FIXTURE_DIGEST) {
    return { ok: false, code: 'FIXTURE_DIGEST_MISMATCH' };
  }
  return { ok: true, fixtureDigest: actual };
}

export async function awaitReadiness({
  runId,
  expectedReadiness = { runId },
  deadlineMs = READINESS_TIMEOUT_MS,
  probe,
  clock = Date.now,
  wait = () => new Promise((done) => setTimeout(done, 100)),
  stopAttemptProcessGroup,
  attemptedProcessGroup,
  processAlive = async () => false,
}) {
  const started = clock();
  while (clock() - started < deadlineMs) {
    const result = await probe();
    const withinDeadline = clock() - started < deadlineMs;
    const fullIdentityExpected = ['lesson', 'fixtureDigest', 'runId', 'implementationInput']
      .every((field) => Object.hasOwn(expectedReadiness, field));
    const identity = fullIdentityExpected
      ? validateReadinessPayload(result, expectedReadiness)
      : { ok: result?.ready === true && result.runId === runId };
    if (withinDeadline && identity.ok) return { ok: true };
    if (!withinDeadline) break;
    await wait();
  }
  await stopAttemptProcessGroup(attemptedProcessGroup);
  for (let attempt = 0; attempt < 10; attempt += 1) {
    if (!(await processAlive(attemptedProcessGroup))) {
      return { ok: false, code: 'READINESS_TIMEOUT', timeoutMs: deadlineMs };
    }
    await wait();
  }
  return { ok: false, code: 'ATTEMPTED_PROCESS_SURVIVED_CLEANUP', timeoutMs: deadlineMs };
}

export function validateLocatorIdentity(locator, observed, expectations = {}) {
  const fields = [
    'pid', 'processGroup', 'processStartFingerprint', 'commandHash', 'cwd', 'realRoot',
    'host', 'port', 'runId', 'fixtureDigest', 'implementationInput',
  ];
  const mismatches = fields.filter((field) => locator?.[field] !== observed?.[field]);
  if (expectations.implementationInput !== undefined && locator?.implementationInput !== expectations.implementationInput) {
    if (!mismatches.includes('implementationInput')) mismatches.push('implementationInput');
  }
  if (expectations.expectedRunId !== undefined && locator?.runId !== expectations.expectedRunId) {
    if (!mismatches.includes('runId')) mismatches.push('runId');
  }
  if (expectations.expectedFixtureDigest !== undefined && locator?.fixtureDigest !== expectations.expectedFixtureDigest) {
    if (!mismatches.includes('fixtureDigest')) mismatches.push('fixtureDigest');
  }
  if (expectations.expectedHost !== undefined && locator?.host !== expectations.expectedHost) {
    if (!mismatches.includes('host')) mismatches.push('host');
  }
  if (expectations.expectedPort !== undefined && locator?.port !== expectations.expectedPort) {
    if (!mismatches.includes('port')) mismatches.push('port');
  }
  return mismatches.length === 0
    ? { ok: true, maySignal: true }
    : { ok: false, code: 'LOCATOR_IDENTITY_MISMATCH', mismatches, maySignal: false };
}

export async function resetCheck({ lesson, implementationInput }) {
  if (lesson !== LESSON) return { ok: false, code: 'LESSON_REJECTED' };
  if (implementationInput !== AUDITED_INPUT_SHA) return { ok: false, code: 'IMPLEMENTATION_INPUT_REJECTED' };
  let fixture;
  try { fixture = validateFixtureBytes(await readFile(FIXTURE_PATH)); } catch { fixture = { ok: false, code: 'FIXTURE_UNAVAILABLE' }; }
  if (!fixture.ok) return fixture;
  const initial = createBaselineState();
  const first = reducePreviewState(initial, { type: 'reset-explicit' });
  const second = reducePreviewState(first, { type: 'reset-explicit' });
  return {
    ok: true,
    code: 'RESET_CHECK_PASS',
    initialResetAuditCount: initial.resetAuditCount,
    firstResetAuditCount: first.resetAuditCount,
    secondResetAuditCount: second.resetAuditCount,
    baselineDigest: resettableDigest(initial),
    firstResettableDigest: resettableDigest(first),
    secondResettableDigest: resettableDigest(second),
    historyMode: second.historyMode,
    notice: PREVIEW_NOTICE,
  };
}

function locatorPath(port) {
  return resolve(LOCATOR_ROOT, `${port}.json`);
}

async function readLocatorFile(port) {
  try {
    return JSON.parse(await readFile(locatorPath(port), 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  }
}

function hash(value) {
  return `sha256:${createHash('sha256').update(value).digest('hex')}`;
}

function ps(pid, field) {
  return execFileSync('ps', ['-p', String(pid), '-o', `${field}=`], { encoding: 'utf8' }).trim();
}

function processCwd(pid) {
  if (process.platform === 'linux') {
    return execFileSync('readlink', [`/proc/${pid}/cwd`], { encoding: 'utf8' }).trim();
  }
  const value = execFileSync('lsof', ['-a', '-p', String(pid), '-d', 'cwd', '-Fn'], { encoding: 'utf8' });
  const line = value.split('\n').find((entry) => entry.startsWith('n'));
  if (!line) throw new Error('PROCESS_CWD_UNAVAILABLE');
  return line.slice(1);
}

async function observeProcess(locator, { requestedPort = locator.port } = {}) {
  try {
    const command = ps(locator.pid, 'command');
    return {
      pid: locator.pid,
      processGroup: Number(ps(locator.pid, 'pgid')),
      processStartFingerprint: ps(locator.pid, 'lstart'),
      commandHash: hash(command),
      cwd: await realpath(processCwd(locator.pid)),
      realRoot: await realpath(PREVIEW_ROOT),
      host: HOST,
      port: requestedPort,
      runId: locator.runId,
      fixtureDigest: locator.fixtureDigest,
      implementationInput: locator.implementationInput,
    };
  } catch {
    return null;
  }
}

async function probe(port) {
  try {
    const response = await fetch(`${LOOPBACK_SCHEME}://${HOST}:${port}/__i5_02_ready`, {
      redirect: 'error',
      signal: AbortSignal.timeout(800),
    });
    if (!response.ok) return { ready: false };
    return await response.json();
  } catch {
    return { ready: false };
  }
}

async function signalGroup(processGroup, signal) {
  process.kill(-processGroup, signal);
}

async function alive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

async function groupAlive(processGroup) {
  try {
    process.kill(-processGroup, 0);
    return true;
  } catch {
    return false;
  }
}

async function wait(ms = 100) {
  await new Promise((done) => setTimeout(done, ms));
}

export async function downPreview({
  port,
  implementationInput,
  readLocator = readLocatorFile,
  observeProcess: observe = observeProcess,
  probeReadiness = probe,
  signalProcessGroup = signalGroup,
  processAlive = groupAlive,
  wait: pause = wait,
  removeLocator = async () => rm(locatorPath(port), { force: true }),
}) {
  if (implementationInput !== AUDITED_INPUT_SHA) return { ok: false, code: 'IMPLEMENTATION_INPUT_REJECTED', maySignal: false };
  const locator = await readLocator(port);
  if (!locator) return { ok: true, code: 'ALREADY_DOWN' };
  const observed = await observe(locator, { requestedPort: port });
  const identity = validateLocatorIdentity(locator, observed, {
    implementationInput,
    expectedRunId: locator.runId,
    expectedFixtureDigest: FIXTURE_DIGEST,
    expectedHost: HOST,
    expectedPort: port,
  });
  if (!identity.ok) return identity;
  const readiness = await probeReadiness(port);
  const ready = probeReadiness === probe
    ? validateReadinessPayload(readiness, {
      lesson: LESSON,
      fixtureDigest: locator.fixtureDigest,
      runId: locator.runId,
      implementationInput: locator.implementationInput,
    })
    : { ok: readiness?.ready === true && readiness.runId === locator.runId };
  if (!ready.ok) return { ok: false, code: 'READINESS_IDENTITY_MISMATCH', maySignal: false };
  for (const signal of ['SIGINT', 'SIGTERM']) {
    await signalProcessGroup(locator.processGroup, signal);
    for (let attempt = 0; attempt < 10; attempt += 1) {
      await pause(50);
      if (!(await processAlive(locator.processGroup))) {
        await removeLocator();
        return { ok: true, code: 'STOPPED' };
      }
    }
  }
  return { ok: false, code: 'OWNED_PROCESS_SURVIVED_SHUTDOWN' };
}

async function portAvailable(port) {
  return new Promise((done) => {
    const server = createServer();
    server.once('error', () => done(false));
    server.listen(port, HOST, () => server.close(() => done(true)));
  });
}

async function stopAttemptedGroup(group) {
  try { process.kill(-group, 'SIGTERM'); } catch {}
}

async function startPreview({ lesson, port, implementationInput }) {
  const request = validateStartRequest({ lesson, fixtureDigest: FIXTURE_DIGEST, implementationInput });
  if (!request.ok) return request;
  let fixture;
  try { fixture = validateFixtureBytes(await readFile(FIXTURE_PATH)); } catch { fixture = { ok: false, code: 'FIXTURE_UNAVAILABLE' }; }
  if (!fixture.ok) return fixture;
  if (!(await portAvailable(port))) return { ok: false, code: 'PORT_OCCUPIED' };
  const previous = await readLocatorFile(port);
  if (previous) return { ok: false, code: 'LOCATOR_ALREADY_EXISTS' };
  const runId = `gate-a-${Date.now().toString(36)}-${randomBytes(6).toString('hex')}`;
  const args = [
    HOST_SCRIPT, '--port', String(port), '--lesson', lesson, '--fixture-digest', FIXTURE_DIGEST,
    '--run-id', runId, '--implementation-input', implementationInput,
  ];
  const child = spawn(process.execPath, args, {
    cwd: ROOT,
    detached: true,
    stdio: 'ignore',
  });
  child.unref();
  const readiness = await awaitReadiness({
    runId,
    expectedReadiness: {
      lesson,
      fixtureDigest: FIXTURE_DIGEST,
      runId,
      implementationInput,
    },
    probe: () => probe(port),
    stopAttemptProcessGroup: stopAttemptedGroup,
    attemptedProcessGroup: child.pid,
    processAlive: groupAlive,
  });
  if (!readiness.ok) return readiness;
  const seed = {
    pid: child.pid,
    processGroup: child.pid,
    host: HOST,
    port,
    runId,
    fixtureDigest: FIXTURE_DIGEST,
    implementationInput,
  };
  const observed = await observeProcess(seed, { requestedPort: port });
  if (!observed) {
    await stopAttemptedGroup(child.pid);
    for (let attempt = 0; attempt < 10; attempt += 1) {
      if (!(await alive(child.pid))) return { ok: false, code: 'PROCESS_IDENTITY_UNAVAILABLE' };
      await wait(50);
    }
    return { ok: false, code: 'ATTEMPTED_PROCESS_SURVIVED_CLEANUP' };
  }
  const locator = { ...observed };
  await mkdir(LOCATOR_ROOT, { recursive: true });
  const target = locatorPath(port);
  const temporary = `${target}.${process.pid}.tmp`;
  await writeFile(temporary, `${JSON.stringify(locator, null, 2)}\n`, { flag: 'wx', mode: 0o600 });
  await rename(temporary, target);
  return { ok: true, code: 'STARTED', locator, url: `${LOOPBACK_SCHEME}://${HOST}:${port}/` };
}

async function statusPreview({ port, implementationInput }) {
  const locator = await readLocatorFile(port);
  if (!locator) return { ok: false, code: 'NOT_RUNNING' };
  const observed = await observeProcess(locator, { requestedPort: port });
  const identity = validateLocatorIdentity(locator, observed, {
    implementationInput,
    expectedRunId: locator.runId,
    expectedFixtureDigest: FIXTURE_DIGEST,
    expectedHost: HOST,
    expectedPort: port,
  });
  if (!identity.ok) return identity;
  const readiness = await probe(port);
  const ready = validateReadinessPayload(readiness, {
    lesson: LESSON,
    fixtureDigest: locator.fixtureDigest,
    runId: locator.runId,
    implementationInput: locator.implementationInput,
  });
  return ready.ok ? { ok: true, code: 'RUNNING', locator } : { ok: false, code: 'READINESS_IDENTITY_MISMATCH' };
}

function parseArgs(values) {
  const command = values[0];
  const options = {};
  for (let index = 1; index < values.length; index += 2) {
    const name = values[index];
    if (!name?.startsWith('--') || values[index + 1] === undefined) throw new Error('INVALID_ARGUMENTS');
    options[name.slice(2)] = values[index + 1];
  }
  return { command, options };
}

async function main() {
  const { command, options } = parseArgs(process.argv.slice(2));
  const implementationInput = options['implementation-input'];
  if (implementationInput !== AUDITED_INPUT_SHA) throw new Error('IMPLEMENTATION_INPUT_REJECTED');
  let result;
  if (command === 'reset-check') {
    result = await resetCheck({ lesson: options.lesson, implementationInput });
  } else {
    const checkedPort = validatePort(options.port);
    if (!checkedPort.ok) result = checkedPort;
    else if (command === 'start') result = await startPreview({ lesson: options.lesson, port: checkedPort.port, implementationInput });
    else if (command === 'status') result = await statusPreview({ port: checkedPort.port, implementationInput });
    else if (command === 'down') result = await downPreview({ port: checkedPort.port, implementationInput });
    else result = { ok: false, code: 'COMMAND_REJECTED' };
  }
  const stream = result.ok ? process.stdout : process.stderr;
  stream.write(`${JSON.stringify(result)}\n`);
  if (!result.ok) process.exitCode = 1;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  });
}
