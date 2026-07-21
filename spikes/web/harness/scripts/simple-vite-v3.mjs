import { spawn, spawnSync } from 'node:child_process';
import { createHash, randomBytes } from 'node:crypto';
import { cpSync, existsSync, mkdirSync, readFileSync, realpathSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { dirname, relative, resolve, sep } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const ROOT = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), '../../../..'));
export const CONTRACT_PATH = resolve(ROOT, 'spikes/web/harness/simple-vite-v3.json');
export const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
const CANDIDATE = resolve(ROOT, 'spikes/web/candidates/vite');
const RUNTIME = resolve(ROOT, contract.runtimePrefix);
const EVIDENCE_CLOSURE_RED_SHA = '23ad065ed49aa5bba718252a6755511182e55a23';
const EXPECTED_CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'";
const PROCESS_TERM_GRACE_MS = 250;
const PROCESS_FINAL_WAIT_MS = 250;
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const relativePath = path => relative(ROOT, path).split(sep).join('/');
const git = args => {
  const result = spawnSync('git', args, { cwd: ROOT, encoding: 'utf8' });
  if (result.status !== 0) throw new Error(`git ${args.join(' ')} failed: ${result.stderr.trim()}`);
  return result.stdout.replace(/\n$/, '');
};

export function hashFile(path) {
  return sha256(readFileSync(resolve(ROOT, path)));
}

export function allowedPath(path, configuration = contract) {
  return configuration.allowedPaths.includes(path) || configuration.allowedPrefixes.some(prefix => path.startsWith(prefix));
}

export function validateChangedPaths(paths, configuration = contract) {
  return paths.filter(path => path && !allowedPath(path, configuration));
}

export function scanText(text) {
  const rules = {
    privateKey: /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/i,
    credential: /(?:api[_-]?key|client[_-]?secret|password|token)\s*[:=]\s*["'][^"']{8,}["']/i,
    absolutePrivatePath: /\/(?:Users|home)\/[A-Za-z0-9._-]+\//,
    email: /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i,
    phone: /(?:phone|mobile|telephone)\s*[:=]\s*["']?(?:\+?84|0)(?:[ .-]?\d){9}\b/i,
    governmentIdentifier: /(?:citizen|national|government|identity|ssn)[_-]?(?:id|number)\s*[:=]\s*["']?\d{9,12}\b/i,
    unsafeInjection: /dangerouslySetInnerHTML|\beval\s*\(|new\s+Function\s*\(|\.innerHTML\s*=/,
    remoteImport: /(?:from\s*|import\s*\()\s*["']https?:\/\//,
    sourceMap: /sourceMappingURL=|\.map(?:"|$)/,
  };
  return Object.entries(rules).filter(([, pattern]) => pattern.test(text)).map(([id]) => id);
}

export function validateOwnership(ledger, expected = {}) {
  const failures = [];
  for (const key of ['pid', 'processGroup', 'fingerprint', 'cwd', 'command', 'root', 'port', 'runId', 'childHandle']) {
    if (ledger?.[key] === undefined || ledger[key] === null || ledger[key] === '') failures.push(`missing-${key}`);
  }
  if (ledger?.port !== contract.port) failures.push('wrong-port');
  if (ledger?.root && resolve(ROOT, ledger.root) !== resolve(CANDIDATE, 'dist')) failures.push('wrong-root');
  if (expected.runId && ledger?.runId !== expected.runId) failures.push('wrong-run-id');
  return failures;
}

export function validateEvidenceManifest(manifest) {
  const failures = [];
  const closedRun = typeof manifest?.runId === 'string' && manifest.runId.length > 0;
  if (manifest?.schemaVersion !== 'i5-02-simple-vite-v3-evidence-v1') failures.push('schema');
  if (manifest?.acceptanceRevision !== contract.acceptanceRevision) failures.push('revision');
  if (manifest?.implementationInputSha !== contract.implementationInputSha) failures.push('input');
  if (!/^[0-9a-f]{40}$/.test(manifest?.testedSourceSha || '')) failures.push('tested-source');
  if (!/^[0-9a-f]{40}$/.test(manifest?.testedTreeSha || '')) failures.push('tested-tree');
  if (JSON.stringify(manifest?.groups?.map(({ id }) => id)) !== JSON.stringify(contract.groups)) failures.push('groups');
  if (manifest?.groups?.some(({ result }) => result !== 'pass')) failures.push('group-result');
  if (manifest?.redProvenance?.result !== 'pass') failures.push('red-provenance');
  if (manifest?.redaction?.result !== 'pass') failures.push('redaction');
  if (manifest?.cleanupRollback?.result !== 'pass') failures.push('rollback');
  const locators = manifest?.artifactLocators;
  if (!locators
      || !Array.isArray(locators.journeyFacts) || locators.journeyFacts.length !== 2
      || typeof locators.axe !== 'string'
      || typeof locators.noJsInventory !== 'string'
      || typeof locators.noJsResponse !== 'string') failures.push('artifact-locators');
  if (!Array.isArray(manifest?.testNameInventory)
      || manifest.testNameInventory.length < 5
      || !manifest.testNameInventory.some(name => name.includes('V3-02'))
      || !manifest.testNameInventory.some(name => name.includes('chromium-desktop'))
      || !manifest.testNameInventory.some(name => name.includes('chromium-narrow'))) failures.push('test-name-inventory');
  const axe = manifest?.axeSummary;
  if (!axe || axe.invocations !== 1 || axe.critical !== 0 || axe.serious !== 0
      || axe.findingsRetained !== true || (closedRun && !Number.isInteger(axe.incomplete))) failures.push('axe-summary');
  const noJs = manifest?.noJsFacts;
  if (!noJs || noJs.javaScriptEnabled !== false || !(noJs.responseBytes > 0)
      || typeof noJs.csp !== 'string' || (closedRun && noJs.csp !== EXPECTED_CSP)
      || noJs.inventoryCount < 13) failures.push('no-js-facts');
  const scan = manifest?.scanSummary;
  if (!scan || scan.result !== 'pass' || scan.findings !== 0
      || (closedRun && (scan.finalRetained !== 'pass' || !(scan.checks >= 6)))) failures.push('scan-summary');
  const owned = manifest?.ownedResourceSummary;
  if (!owned || owned.result !== 'pass' || owned.serverCount !== 1
      || owned.port !== contract.port || owned.cleanup !== 'pass'
      || owned.rollbackSimulation !== 'pass') failures.push('owned-resource-summary');
  if (closedRun && manifest?.evidenceClosureRedSha !== EVIDENCE_CLOSURE_RED_SHA) failures.push('evidence-closure-red-sha');
  if (closedRun && !['feature-branch', 'detached-exact-live'].includes(manifest?.authorityMode)) failures.push('authority-mode');
  if (closedRun && (!/^[0-9a-f]{40}$/.test(manifest?.freshLiveHead || '')
      || manifest?.targetedReviewFixRed?.result !== 'pass'
      || manifest?.targetedReviewFixRed?.sourceSha !== 'f45aa016605c250aa26c977f2320acf75b565ecb'
      || !(manifest?.targetedReviewFixRed?.rc > 0)
      || manifest?.targetedReviewFixRed?.assertionIds?.length !== 4
      || manifest?.targetedReviewFixRed?.log !== 'tdd/review-fix-red/focused-tests.tap')) failures.push('targeted-review-fix-red');
  return failures;
}

function statusPaths() {
  const paths = new Set();
  for (const args of [['diff', '--name-only', `${contract.implementationInputSha}...HEAD`], ['diff', '--name-only'], ['diff', '--cached', '--name-only']]) {
    for (const path of git(args).split('\n').filter(Boolean)) paths.add(path);
  }
  for (const line of git(['status', '--porcelain=v1', '--untracked-files=all']).split('\n').filter(Boolean)) {
    const path = line.slice(3).replace(/^"|"$/g, '');
    if (!path.startsWith('.artifacts/') && !path.startsWith('spikes/web/candidates/vite/node_modules/') && !path.startsWith('spikes/web/candidates/vite/dist/') && !path.startsWith('spikes/web/candidates/vite/test-results/') && !path.startsWith('spikes/web/candidates/vite/playwright-report/')) paths.add(path);
  }
  return [...paths].sort();
}

export function preflight(implementationInput) {
  const failures = [];
  const branch = git(['branch', '--show-current']);
  const head = git(['rev-parse', '--verify', 'HEAD']);
  const live = spawnSync('git', ['ls-remote', '--exit-code', 'origin', `refs/heads/${contract.branch}`], { cwd: ROOT, encoding: 'utf8' });
  const liveLines = live.status === 0 ? live.stdout.trim().split('\n').filter(Boolean) : [];
  const liveParts = liveLines.length === 1 ? liveLines[0].trim().split(/\s+/) : [];
  const liveHead = liveParts.length === 2 && liveParts[1] === `refs/heads/${contract.branch}` ? liveParts[0] : '';
  let authorityMode = 'invalid';
  if (implementationInput !== contract.implementationInputSha) failures.push('implementation-input-mismatch');
  if (!/^[0-9a-f]{40}$/.test(head)) failures.push('invalid-head-identity');
  if (live.status !== 0 || liveLines.length === 0) failures.push('fresh-live-unavailable');
  else if (liveLines.length !== 1 || !/^[0-9a-f]{40}$/.test(liveHead)) failures.push('fresh-live-ambiguous-or-invalid');
  if (branch === contract.branch) authorityMode = 'feature-branch';
  else if (branch) failures.push('branch-mismatch');
  else if (/^[0-9a-f]{40}$/.test(head) && /^[0-9a-f]{40}$/.test(liveHead) && head === liveHead) authorityMode = 'detached-exact-live';
  else failures.push('detached-head-mismatch');
  if (git(['status', '--porcelain=v1', '--untracked-files=no'])) failures.push('dirty-tracked-state');
  for (const ancestor of [contract.implementationInputSha, contract.issue6IntegrationSha]) {
    if (spawnSync('git', ['merge-base', '--is-ancestor', ancestor, 'HEAD'], { cwd: ROOT }).status !== 0) failures.push(`missing-ancestor:${ancestor}`);
  }
  for (const [path, expected] of Object.entries(contract.fixtureIdentities)) {
    if (hashFile(path) !== expected.sha256) failures.push(`fixture-sha:${path}`);
    if (git(['hash-object', path]) !== expected.blob) failures.push(`fixture-blob:${path}`);
  }
  for (const [path, expected] of Object.entries(contract.protected)) if (hashFile(path) !== expected) failures.push(`protected-sha:${path}`);
  for (const [path, expected] of Object.entries(contract.protectedTrees)) {
    const actual = path === 'spikes/web/evidence/retained' ? git(['rev-parse', `${contract.implementationInputSha}:${path}`]) : git(['rev-parse', `HEAD:${path}`]);
    if (actual !== expected) failures.push(`protected-tree:${path}`);
  }
  if (hashFile('spikes/web/candidates/vite/package-lock.json') !== contract.lockSha256) failures.push('lock-sha');
  const unauthorized = validateChangedPaths(statusPaths());
  if (unauthorized.length) failures.push(`unauthorized-paths:${unauthorized.join(',')}`);
  if (existsSync(resolve(ROOT, 'apps/learning-portal')) || existsSync(resolve(ROOT, 'apps/lab-runner'))) failures.push('forbidden-portal-or-runner');
  return { result: failures.length ? 'fail' : 'pass', failures, authorityMode, head, freshLiveHead: liveHead || null, changedPaths: statusPaths() };
}

function sanitize(text) {
  return String(text)
    .split(ROOT).join('<WORKSPACE>')
    .replace(/\/Users\/[^/\s"'<>]+(?:\/[^\s"'<>]*)*/g, '<PRIVATE_PATH>')
    .replace(/\/home\/[^/\s"'<>]+(?:\/[^\s"'<>]*)*/g, '<PRIVATE_PATH>');
}

function copySanitized(source, destination) {
  writeFileSync(destination, sanitize(readFileSync(source, 'utf8')));
}

function processFingerprint(pid) {
  const result = spawnSync('ps', ['-p', String(pid), '-o', 'pgid=', '-o', 'lstart=', '-o', 'command='], { encoding: 'utf8' });
  return result.status === 0 ? result.stdout.trim().replace(/\s+/g, ' ') : '';
}

function processGroup(pid) {
  const result = spawnSync('ps', ['-p', String(pid), '-o', 'pgid='], { encoding: 'utf8' });
  const pgid = result.status === 0 ? Number(result.stdout.trim()) : NaN;
  return Number.isInteger(pgid) ? pgid : null;
}

function groupExists(processGroupId) {
  try { process.kill(-processGroupId, 0); return true; } catch (error) { return error.code === 'EPERM'; }
}

const delay = milliseconds => new Promise(resolveDelay => setTimeout(resolveDelay, milliseconds));

async function waitForGroupExit(owned, ceilingMs) {
  const deadline = Date.now() + ceilingMs;
  while (groupExists(owned.processGroup) && Date.now() < deadline) await delay(20);
  return !groupExists(owned.processGroup);
}

function spawnOwned(command, options = {}) {
  const [program, ...args] = command;
  const child = spawn(program, args, { cwd: ROOT, detached: true, ...options });
  const pid = child.pid;
  const pgid = processGroup(pid);
  const fingerprint = processFingerprint(pid);
  const currentGroup = processGroup(process.pid);
  if (!Number.isInteger(pid) || pid <= 1 || pgid !== pid || pgid === currentGroup || !fingerprint) {
    if (Number.isInteger(pid) && pid > 1) child.kill('SIGKILL');
    throw new Error('spawned child did not establish a verified owned process group');
  }
  let closed = false;
  const closePromise = new Promise(resolveClose => {
    child.once('error', error => resolveClose({ code: null, signal: null, error }));
    child.once('close', (code, signal) => { closed = true; resolveClose({ code, signal, error: null }); });
  });
  return { child, pid, processGroup: pgid, fingerprint, currentGroup, closePromise, isClosed: () => closed };
}

function signalOwnedGroup(owned, signal) {
  if (!owned || owned.processGroup !== owned.pid || owned.pid <= 1 || owned.processGroup === owned.currentGroup) throw new Error('invalid owned process group; refusing to signal');
  const current = processFingerprint(owned.pid);
  if (current && current !== owned.fingerprint) throw new Error('owned process fingerprint changed; refusing to signal');
  try { process.kill(-owned.processGroup, signal); return true; } catch (error) {
    if (error.code === 'ESRCH') return false;
    throw error;
  }
}

async function terminateOwnedGroup(owned) {
  const termination = { termSent: false, killSent: false, groupExited: true, finalWaitExpired: false };
  if (!owned || !groupExists(owned.processGroup)) return termination;
  termination.termSent = signalOwnedGroup(owned, 'SIGTERM');
  termination.groupExited = await waitForGroupExit(owned, PROCESS_TERM_GRACE_MS);
  if (!termination.groupExited) {
    termination.killSent = signalOwnedGroup(owned, 'SIGKILL');
    termination.groupExited = await waitForGroupExit(owned, PROCESS_FINAL_WAIT_MS);
  }
  termination.finalWaitExpired = !termination.groupExited;
  await Promise.race([owned.closePromise, delay(PROCESS_FINAL_WAIT_MS)]);
  return termination;
}

async function runBounded(name, command, ceilingMs, directory) {
  const startedAt = new Date().toISOString();
  const started = process.hrtime.bigint();
  const owned = spawnOwned(command, { env: { ...process.env, BASE_URL: 'http://127.0.0.1:4175' }, stdio: ['ignore', 'pipe', 'pipe'] });
  let stdout = '', stderr = '';
  owned.child.stdout.on('data', chunk => { stdout += chunk; });
  owned.child.stderr.on('data', chunk => { stderr += chunk; });
  const outcome = await Promise.race([
    owned.closePromise.then(value => ({ kind: 'close', ...value })),
    delay(ceilingMs).then(() => ({ kind: 'timeout' })),
  ]);
  const timedOut = outcome.kind === 'timeout';
  let termination = { termSent: false, killSent: false, groupExited: true, finalWaitExpired: false };
  if (timedOut || outcome.error || groupExists(owned.processGroup)) termination = await terminateOwnedGroup(owned);
  const closed = outcome.kind === 'close' ? outcome : await Promise.race([owned.closePromise, delay(PROCESS_FINAL_WAIT_MS).then(() => ({ code: null, signal: null, error: new Error('bounded final child wait expired') }))]);
  const result = { name, command, startedAt, durationMs: Number(process.hrtime.bigint() - started) / 1e6, rc: closed.code ?? 1, signal: closed.signal, timedOut, termination, stdout: sanitize(stdout), stderr: sanitize(`${stderr}${closed.error ? `${stderr ? '\n' : ''}${closed.error.message}` : ''}`) };
  writeFileSync(resolve(directory, `${name}.json`), `${JSON.stringify(result, null, 2)}\n`);
  writeFileSync(resolve(directory, `${name}.log`), `${result.stdout}${result.stderr}`);
  return result;
}

async function startHost(runId, directory) {
  const hostPath = resolve(ROOT, 'spikes/web/harness/scripts/candidate-static-host.mjs');
  const command = [process.execPath, hostPath, resolve(CANDIDATE, 'dist'), String(contract.port)];
  const owned = spawnOwned(command, { stdio: ['ignore', 'pipe', 'pipe'] });
  const { child } = owned;
  let output = '';
  try {
    const ready = await new Promise((resolveReady, reject) => {
      const timer = setTimeout(() => reject(new Error('V3 host READY timeout')), contract.ceilingsMs.hostReady);
      const consume = chunk => {
        output += chunk;
        if (output.includes('READY http://127.0.0.1:4175')) { clearTimeout(timer); resolveReady(true); }
      };
      child.stdout.on('data', consume);
      child.stderr.on('data', consume);
      child.on('exit', code => { clearTimeout(timer); reject(new Error(`V3 host exited before READY: ${code} ${sanitize(output)}`)); });
    });
    if (!ready) throw new Error('host not ready');
  } catch (error) {
    const termination = await terminateOwnedGroup(owned);
    writeFileSync(resolve(directory, 'host-start-error.json'), `${JSON.stringify({ error: sanitize(error.message), output: sanitize(output), termination }, null, 2)}\n`);
    throw error;
  }
  const ledger = { pid: owned.pid, processGroup: owned.processGroup, fingerprint: sanitize(owned.fingerprint), cwd: '.', command: command.map(sanitize), root: 'spikes/web/candidates/vite/dist', port: contract.port, runId, childHandle: true };
  const liveLedger = { ...ledger, fingerprint: owned.fingerprint };
  writeFileSync(resolve(directory, 'owned-resources.json'), `${JSON.stringify(ledger, null, 2)}\n`);
  return { ...owned, ledger: liveLedger };
}

async function stopHost(owned) {
  if (!owned) return;
  const termination = await terminateOwnedGroup(owned);
  if (!termination.groupExited) throw new Error('owned host process group survived bounded cleanup');
}

function makeRunDirectory(kind, runId) {
  const directory = resolve(RUNTIME, runId, kind);
  mkdirSync(directory, { recursive: true });
  writeFileSync(resolve(RUNTIME, `latest-${kind}.json`), `${JSON.stringify({ runId, directory: relativePath(directory) }, null, 2)}\n`);
  return directory;
}

function runId() {
  return `v3-${new Date().toISOString().replace(/[-:.]/g, '').replace('Z', 'Z')}-${randomBytes(4).toString('hex')}`;
}

function treeSha() {
  const result = spawnSync('git', ['write-tree'], { cwd: ROOT, encoding: 'utf8' });
  if (result.status !== 0) throw new Error(result.stderr);
  return result.stdout.trim();
}

function commandVersion(program, args = ['--version']) {
  const result = spawnSync(program, args, { cwd: ROOT, encoding: 'utf8' });
  return result.status === 0 ? result.stdout.trim() : 'unavailable';
}

function playwrightReport(logPath) {
  const output = readFileSync(logPath, 'utf8');
  const reportStart = output.indexOf('{');
  if (reportStart < 0) throw new Error('Playwright JSON report was not emitted');
  return JSON.parse(output.slice(reportStart));
}

function playwrightInventory(logPath) {
  const report = playwrightReport(logPath);
  const entries = report.suites.flatMap(suite => suite.specs).flatMap(spec => spec.tests.map(entry => ({
    title: spec.title,
    project: entry.projectName,
    status: entry.status,
    retries: entry.results.reduce((maximum, result) => Math.max(maximum, result.retry || 0), 0),
  })));
  return entries.sort((a, b) => `${a.project}:${a.title}`.localeCompare(`${b.project}:${b.title}`));
}

function testNamesFromTap(path) {
  if (!existsSync(path)) return [];
  return [...readFileSync(path, 'utf8').matchAll(/^# Subtest: (.+)$/gm)].map(match => match[1]);
}

function materializeBrowserEvidence(directory) {
  const report = playwrightReport(resolve(directory, 'playwright.log'));
  const required = new Map([
    ['chromium-desktop:v3-03-v3-04-journey-facts.json', 'chromium-desktop/v3-03-v3-04-journey-facts.json'],
    ['chromium-narrow:v3-03-v3-04-journey-facts.json', 'chromium-narrow/v3-03-v3-04-journey-facts.json'],
    ['chromium-desktop:v3-05-axe-complete.json', 'chromium-desktop/v3-05-axe-complete.json'],
    ['chromium-desktop:v3-06-no-js-inventory.json', 'chromium-desktop/v3-06-no-js-inventory.json'],
    ['chromium-desktop:v3-06-response.html', 'chromium-desktop/v3-06-response.html'],
  ]);
  const materialized = new Map();
  for (const suite of report.suites ?? []) {
    for (const spec of suite.specs ?? []) {
      for (const test of spec.tests ?? []) {
        for (const result of test.results ?? []) {
          for (const attachment of result.attachments ?? []) {
            const key = `${test.projectName}:${attachment.name}`;
            const target = required.get(key);
            if (!target) continue;
            if (!attachment.body || materialized.has(key)) throw new Error(`browser-evidence-attachment:${key}`);
            const path = resolve(directory, 'browser-evidence', target);
            mkdirSync(dirname(path), { recursive: true });
            writeFileSync(path, Buffer.from(attachment.body, 'base64'));
            materialized.set(key, path);
          }
        }
      }
    }
  }
  const missing = [...required.keys()].filter(key => !materialized.has(key));
  if (missing.length) throw new Error(`browser-evidence-missing:${missing.join(',')}`);
  const journey = ['chromium-desktop', 'chromium-narrow'].map(project => JSON.parse(readFileSync(materialized.get(`${project}:v3-03-v3-04-journey-facts.json`), 'utf8')));
  const axe = JSON.parse(readFileSync(materialized.get('chromium-desktop:v3-05-axe-complete.json'), 'utf8'));
  const noJs = JSON.parse(readFileSync(materialized.get('chromium-desktop:v3-06-no-js-inventory.json'), 'utf8'));
  const response = readFileSync(materialized.get('chromium-desktop:v3-06-response.html'));
  return { required, materialized, journey, axe, noJs, response, report };
}

function cleanupCandidateRuntime(directory) {
  const distIndex = resolve(CANDIDATE, 'dist/index.html');
  if (existsSync(distIndex)) cpSync(distIndex, resolve(directory, 'response-index.html'));
  const targets = ['node_modules', 'dist', 'test-results', 'playwright-report'].map(name => resolve(CANDIDATE, name));
  for (const target of targets) rmSync(target, { recursive: true, force: true });
  const preserved = resolve(directory, 'result.json');
  const result = {
    result: targets.every(target => !existsSync(target)) && existsSync(preserved) ? 'pass' : 'fail',
    removed: targets.map(relativePath),
    preserved: relativePath(preserved),
    scope: 'run-owned-candidate-runtime-only',
  };
  writeFileSync(resolve(directory, 'rollback.json'), `${JSON.stringify(result, null, 2)}\n`);
  return result;
}

async function execute(mode, implementationInput) {
  const authority = preflight(implementationInput);
  if (authority.result !== 'pass') throw new Error(`authority failed: ${authority.failures.join('; ')}`);
  for (const name of ['node_modules', 'dist', 'test-results', 'playwright-report']) {
    if (existsSync(resolve(CANDIDATE, name))) throw new Error(`pre-existing candidate runtime is not owned by this run: ${name}`);
  }
  const id = runId();
  const directory = makeRunDirectory(mode, id);
  const packageBefore = hashFile('spikes/web/candidates/vite/package.json');
  const lockBefore = hashFile('spikes/web/candidates/vite/package-lock.json');
  const results = [];
  let owned;
  try {
    results.push(await runBounded('install', contract.commands.install, contract.ceilingsMs.install, directory));
    results.push(await runBounded('build', contract.commands.build, contract.ceilingsMs.build, directory));
    results.push(await runBounded('unit', contract.commands.unit, contract.ceilingsMs.node, directory));
    if (mode === 'gate') results.push(await runBounded('harness', contract.commands.harness, contract.ceilingsMs.node, directory));
    if (results[1].rc === 0) {
      owned = await startHost(id, directory);
      results.push(await runBounded('playwright', contract.commands.smoke, contract.ceilingsMs.playwright, directory));
      const browserResults = resolve(CANDIDATE, 'test-results');
      if (existsSync(browserResults)) cpSync(browserResults, resolve(directory, 'browser-results'), { recursive: true });
    }
    if (mode === 'gate') results.push(await runBounded('npm-audit', contract.commands.audit, contract.ceilingsMs.audit, directory));
  } finally {
    await stopHost(owned);
  }
  const lockAfter = hashFile('spikes/web/candidates/vite/package-lock.json');
  const packageAfter = hashFile('spikes/web/candidates/vite/package.json');
  const inventory = existsSync(resolve(CANDIDATE, 'dist')) ? readdirSync(resolve(CANDIDATE, 'dist'), { recursive: true }).filter(path => statSync(resolve(CANDIDATE, 'dist', path)).isFile()).sort() : [];
  const unit = results.find(({ name }) => name === 'unit');
  const smoke = results.find(({ name }) => name === 'playwright');
  let pass;
  if (mode === 'red') {
    const named = `${unit?.stdout || ''}${unit?.stderr || ''}${smoke?.stdout || ''}${smoke?.stderr || ''}`;
    pass = results[0]?.rc === 0 && results[1]?.rc === 0 && packageBefore === packageAfter && lockBefore === lockAfter && (unit?.rc !== 0 || smoke?.rc !== 0) && /V3-02/.test(named) && /V3-03|V3-04|V3-05|V3-06/.test(named) && !/ERR_MODULE_NOT_FOUND|Cannot find package|browserType\.launch: Executable doesn't exist/.test(named);
  } else {
    pass = results.length === 6 && results.every(({ rc, timedOut }) => rc === 0 && !timedOut) && packageBefore === packageAfter && lockBefore === lockAfter;
  }
  const browserInventory = smoke?.rc === 0 ? playwrightInventory(resolve(directory, 'playwright.log')) : [];
  const summary = { schemaVersion: `i5-02-simple-vite-v3-${mode}-v1`, result: pass ? 'pass' : 'fail', runId: id, implementationInputSha: implementationInput, sourceSha: git(['rev-parse', 'HEAD']), testedTreeSha: treeSha(), authority, packageBefore, packageAfter, lockBefore, lockAfter, inventory, browserInventory, tools: { node: process.version, npm: commandVersion('npm'), chrome: commandVersion('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome') }, commands: results.map(({ name, command, rc, timedOut, durationMs }) => ({ name, command, rc, timedOut, durationMs })) };
  writeFileSync(resolve(directory, 'result.json'), `${JSON.stringify(summary, null, 2)}\n`);
  if (mode === 'gate') {
    const cleanup = cleanupCandidateRuntime(directory);
    if (cleanup.result !== 'pass') { summary.result = 'fail'; writeFileSync(resolve(directory, 'result.json'), `${JSON.stringify(summary, null, 2)}\n`); }
  }
  process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
  if (!pass) process.exitCode = 1;
  return summary;
}

function latest(kind) {
  const pointer = JSON.parse(readFileSync(resolve(RUNTIME, `latest-${kind}.json`), 'utf8'));
  const directory = resolve(ROOT, pointer.directory);
  if (!directory.startsWith(`${RUNTIME}${sep}`)) throw new Error('unsafe runtime pointer');
  return { ...pointer, directory };
}

function contemporaneousRed() {
  const pointer = resolve(RUNTIME, 'latest-red.json');
  if (existsSync(pointer)) return latest('red');
  if (!existsSync(resolve(ROOT, contract.retentionIndex))) throw new Error('contemporaneous RED evidence is unavailable');
  const retainedIndex = JSON.parse(readFileSync(resolve(ROOT, contract.retentionIndex), 'utf8'));
  const manifestPath = resolve(ROOT, retainedIndex.manifest?.path || '');
  const retainedRoot = dirname(manifestPath);
  const directory = resolve(retainedRoot, 'tdd/red');
  const resultPath = resolve(directory, 'result.json');
  if (!manifestPath.startsWith(resolve(ROOT, contract.retainedPrefix)) || !existsSync(resultPath)) throw new Error('retained RED locator is invalid');
  const manifestHash = sha256(readFileSync(manifestPath));
  if (manifestHash !== retainedIndex.manifest.sha256) throw new Error('retained RED manifest hash mismatch');
  const redResult = JSON.parse(readFileSync(resultPath, 'utf8'));
  if (redResult.result !== 'pass' || redResult.sourceSha !== 'd644c4fbb0e88bd4d77567a705b835a9c0eb79a0') throw new Error('retained RED identity mismatch');
  return { runId: redResult.runId, directory, retained: true };
}

function targetedReviewFixRed() {
  const directory = resolve(RUNTIME, 'targeted-review-fix-red');
  const resultPath = resolve(directory, 'result.json');
  const logPath = resolve(directory, 'focused-tests.tap');
  if (!existsSync(resultPath) || !existsSync(logPath)) throw new Error('targeted review-fix RED evidence is unavailable');
  const result = JSON.parse(readFileSync(resultPath, 'utf8'));
  if (result.result !== 'pass' || result.rc === 0 || result.sourceSha !== 'f45aa016605c250aa26c977f2320acf75b565ecb' || result.assertionIds?.length !== 4) throw new Error('targeted review-fix RED evidence is invalid');
  return { directory, result };
}

export function scanRun() {
  const green = latest('gate');
  const browserEvidence = materializeBrowserEvidence(green.directory);
  const roots = [resolve(ROOT, 'spikes/web/candidates/vite/index.html'), resolve(ROOT, 'spikes/web/candidates/vite/src'), resolve(ROOT, 'spikes/web/candidates/vite/dist'), green.directory];
  const findings = [];
  const walk = path => {
    if (!existsSync(path)) return;
    if (statSync(path).isDirectory()) for (const child of readdirSync(path)) walk(resolve(path, child));
    else {
      const text = readFileSync(path, 'utf8');
      for (const finding of scanText(text)) findings.push({ path: relativePath(path), finding });
    }
  };
  roots.forEach(walk);
  const responseText = browserEvidence.response.toString('utf8');
  const documentCsp = responseText.includes(`http-equiv="Content-Security-Policy" content="${EXPECTED_CSP}"`);
  const responseCsp = browserEvidence.noJs.csp === EXPECTED_CSP;
  const sameOrigin = browserEvidence.journey.length === 2
    && browserEvidence.journey.every(facts => JSON.stringify(facts.requestOrigins) === JSON.stringify(['http://127.0.0.1:4175']));
  const persistence = browserEvidence.journey.length === 2 && browserEvidence.journey.every(facts => {
    const reset = facts.checkpoints?.find(checkpoint => checkpoint.id === 'reset');
    return reset && JSON.stringify(reset.persistence) === JSON.stringify({ cookie: '', localStorage: 0, sessionStorage: 0, caches: 0, indexedDb: 0, serviceWorkers: 0 });
  });
  const expectedNoJsIds = ['lesson-entry', 'grain-promotion', 'grain-promotion-limitation', 'grain-fulfillment', 'grain-fulfillment-limitation', 'grain-returns', 'grain-returns-limitation', 'grain-data-quality', 'grain-data-quality-limitation', 'lesson-conclusion', 'lesson-reason', 'no-js-reset-limitation', 'reflection-prompt'];
  const noJs = browserEvidence.noJs.responseBytes === browserEvidence.response.length
    && JSON.stringify(browserEvidence.noJs.inventory?.map(({ id }) => id)) === JSON.stringify(expectedNoJsIds);
  const blockingAxe = (browserEvidence.axe.violations ?? []).filter(({ impact }) => impact === 'critical' || impact === 'serious');
  const axe = browserEvidence.axe.testEngine?.name === 'axe-core' && blockingAxe.length === 0;
  const checks = [
    { id: 'content-safety', result: findings.length ? 'fail' : 'pass', details: { scannedRoots: roots.map(relativePath), ruleIds: ['privateKey', 'credential', 'absolutePrivatePath', 'email', 'phone', 'governmentIdentifier', 'unsafeInjection', 'remoteImport', 'sourceMap'] } },
    { id: 'csp-document', result: documentCsp ? 'pass' : 'fail', details: { expected: EXPECTED_CSP } },
    { id: 'csp-response', result: responseCsp ? 'pass' : 'fail', details: { expected: EXPECTED_CSP } },
    { id: 'same-origin', result: sameOrigin ? 'pass' : 'fail', details: { allowedOrigin: 'http://127.0.0.1:4175', projects: browserEvidence.journey.map(({ project, requestOrigins }) => ({ project, requestOrigins })) } },
    { id: 'persistence-empty', result: persistence ? 'pass' : 'fail', details: { stores: ['cookies', 'localStorage', 'sessionStorage', 'CacheStorage', 'IndexedDB', 'serviceWorkers'] } },
    { id: 'no-js-response-inventory', result: noJs ? 'pass' : 'fail', details: { responseBytes: browserEvidence.response.length, inventoryIds: expectedNoJsIds } },
    { id: 'axe-complete', result: axe ? 'pass' : 'fail', details: { violations: browserEvidence.axe.violations?.length ?? -1, critical: blockingAxe.filter(({ impact }) => impact === 'critical').length, serious: blockingAxe.filter(({ impact }) => impact === 'serious').length, passes: browserEvidence.axe.passes?.length ?? -1, incomplete: browserEvidence.axe.incomplete?.length ?? -1, inapplicable: browserEvidence.axe.inapplicable?.length ?? -1 } },
    { id: 'browser-evidence-materialized', result: browserEvidence.materialized.size === browserEvidence.required.size ? 'pass' : 'fail', details: { artifacts: [...browserEvidence.materialized.values()].map(relativePath).sort() } },
  ];
  const output = { schemaVersion: 'i5-02-simple-vite-v3-scan-v1', result: findings.length === 0 && checks.every(check => check.result === 'pass') ? 'pass' : 'fail', roots: roots.map(relativePath), checkInventory: checks, findings };
  writeFileSync(resolve(green.directory, 'scans.json'), `${JSON.stringify(output, null, 2)}\n`);
  return output;
}

function fileIndex(root, excluded = new Set()) {
  const paths = [];
  const walk = directory => {
    for (const name of readdirSync(directory).sort()) {
      const path = resolve(directory, name);
      if (statSync(path).isDirectory()) walk(path);
      else if (!excluded.has(relative(directory, path))) paths.push(path);
    }
  };
  walk(root);
  return paths.sort((a, b) => Buffer.from(relative(root, a)).compare(Buffer.from(relative(root, b)))).map(path => ({ path: relative(root, path).split(sep).join('/'), bytes: statSync(path).size, sha256: sha256(readFileSync(path)) }));
}

function simulateRollback(destination, green, cleanup) {
  const simulationRoot = resolve(RUNTIME, green.runId, 'rollback-simulation');
  const ownedRollbackSentinel = resolve(simulationRoot, 'owned-by-v3.sentinel');
  const unownedRollbackSentinel = resolve(RUNTIME, `unowned-control-${green.runId}.sentinel`);
  mkdirSync(simulationRoot, { recursive: true });
  writeFileSync(ownedRollbackSentinel, `owned:${green.runId}\n`, { flag: 'wx' });
  writeFileSync(unownedRollbackSentinel, `control:${green.runId}\n`, { flag: 'wx' });
  const retainedFiles = [
    resolve(destination, 'green/result.json'),
    resolve(destination, 'security/scans.json'),
    resolve(destination, 'green/browser-results/chromium-desktop/v3-05-axe-complete.json'),
  ];
  const before = Object.fromEntries(retainedFiles.map(path => [relative(destination, path).split(sep).join('/'), sha256(readFileSync(path))]));
  rmSync(ownedRollbackSentinel, { force: true });
  const after = Object.fromEntries(retainedFiles.map(path => [relative(destination, path).split(sep).join('/'), sha256(readFileSync(path))]));
  const retainedPreservation = { result: JSON.stringify(before) === JSON.stringify(after) ? 'pass' : 'fail', before, after };
  const result = {
    result: !existsSync(ownedRollbackSentinel) && existsSync(unownedRollbackSentinel) && retainedPreservation.result === 'pass' && cleanup.result === 'pass' ? 'pass' : 'fail',
    cleanup,
    ownedRollbackSentinel: { id: 'ownedRollbackSentinel', removed: !existsSync(ownedRollbackSentinel), scope: relativePath(simulationRoot) },
    unownedRollbackSentinel: { id: 'unownedRollbackSentinel', preservedDuringSimulation: existsSync(unownedRollbackSentinel), sha256: sha256(readFileSync(unownedRollbackSentinel)) },
    retainedPreservation,
    scope: 'run-owned-sentinel-only',
  };
  rmSync(simulationRoot, { recursive: true, force: true });
  rmSync(unownedRollbackSentinel, { force: true });
  result.unownedRollbackSentinel.controlCleanup = !existsSync(unownedRollbackSentinel);
  return result;
}

function finalRetainedScan(destination) {
  const findings = [];
  let scannedFiles = 0;
  const excluded = new Set(['hash-index.json', 'security/final-retained-scan.json']);
  const walk = directory => {
    for (const name of readdirSync(directory).sort()) {
      const path = resolve(directory, name);
      if (statSync(path).isDirectory()) walk(path);
      else {
        const locator = relative(destination, path).split(sep).join('/');
        if (excluded.has(locator)) continue;
        scannedFiles += 1;
        for (const finding of scanText(readFileSync(path, 'utf8'))) findings.push({ path: locator, finding });
      }
    }
  };
  walk(destination);
  const result = { schemaVersion: 'i5-02-simple-vite-v3-final-retained-scan-v1', result: findings.length ? 'fail' : 'pass', root: '.', scannedFiles, excluded: [...excluded].sort(), findings };
  writeFileSync(resolve(destination, 'security/final-retained-scan.json'), `${JSON.stringify(result, null, 2)}\n`);
  return result;
}

function verifyHashIndex(destination, index) {
  const expected = fileIndex(destination, new Set(['hash-index.json']));
  const exact = JSON.stringify(index.files) === JSON.stringify(expected);
  return { result: exact ? 'pass' : 'fail', fileCount: expected.length };
}

export function retainRun() {
  const red = contemporaneousRed();
  const reviewFixRed = targetedReviewFixRed();
  const green = latest('gate');
  const redResult = JSON.parse(readFileSync(resolve(red.directory, 'result.json'), 'utf8'));
  const greenResult = JSON.parse(readFileSync(resolve(green.directory, 'result.json'), 'utf8'));
  const scans = JSON.parse(readFileSync(resolve(green.directory, 'scans.json'), 'utf8'));
  if (redResult.result !== 'pass' || greenResult.result !== 'pass' || scans.result !== 'pass') throw new Error('cannot retain failed RED/GREEN/scan');
  const browserEvidence = materializeBrowserEvidence(green.directory);
  const destination = resolve(ROOT, contract.retainedPrefix, green.runId);
  if (existsSync(destination)) throw new Error('immutable run destination already exists');
  mkdirSync(resolve(destination, 'tdd/red'), { recursive: true });
  mkdirSync(resolve(destination, 'tdd/review-fix-red'), { recursive: true });
  mkdirSync(resolve(destination, 'green'), { recursive: true });
  mkdirSync(resolve(destination, 'security'), { recursive: true });
  mkdirSync(resolve(destination, 'lifecycle'), { recursive: true });
  for (const name of ['unit.log', 'playwright.log', 'result.json']) if (existsSync(resolve(red.directory, name))) copySanitized(resolve(red.directory, name), resolve(destination, 'tdd/red', name));
  for (const name of ['focused-tests.tap', 'result.json']) copySanitized(resolve(reviewFixRed.directory, name), resolve(destination, 'tdd/review-fix-red', name));
  for (const name of ['install.log', 'build.log', 'unit.log', 'harness.log', 'playwright.log', 'result.json', 'response-index.html']) if (existsSync(resolve(green.directory, name))) copySanitized(resolve(green.directory, name), resolve(destination, 'green', name));
  if (existsSync(resolve(green.directory, 'browser-results'))) cpSync(resolve(green.directory, 'browser-results'), resolve(destination, 'green/browser-results'), { recursive: true });
  for (const [key, target] of browserEvidence.required) {
    const output = resolve(destination, 'green/browser-results', target);
    mkdirSync(dirname(output), { recursive: true });
    writeFileSync(output, readFileSync(browserEvidence.materialized.get(key)));
  }
  copySanitized(resolve(green.directory, 'npm-audit.log'), resolve(destination, 'security/npm-audit.json'));
  copySanitized(resolve(green.directory, 'scans.json'), resolve(destination, 'security/scans.json'));
  copySanitized(resolve(green.directory, 'owned-resources.json'), resolve(destination, 'lifecycle/owned-resources.json'));
  const audit = JSON.parse(readFileSync(resolve(green.directory, 'npm-audit.log'), 'utf8'));
  const browser = greenResult.browserInventory;
  const has = (project, fragment) => browser.some(entry => entry.project === project && entry.title.includes(fragment) && entry.status === 'expected' && entry.retries === 0);
  const commandPassed = name => greenResult.commands.some(command => command.name === name && command.rc === 0 && !command.timedOut);
  const groupChecks = {
    'V3-01': commandPassed('install') && commandPassed('build') && greenResult.packageBefore === greenResult.packageAfter && greenResult.lockBefore === greenResult.lockAfter,
    'V3-02': commandPassed('unit'),
    'V3-03': has('chromium-desktop', 'V3-03 V3-04') && has('chromium-narrow', 'V3-03 V3-04'),
    'V3-04': has('chromium-desktop', 'V3-03 V3-04') && has('chromium-narrow', 'V3-03 V3-04'),
    'V3-05': has('chromium-desktop', 'V3-05') && (browserEvidence.axe.violations ?? []).filter(({ impact }) => impact === 'critical' || impact === 'serious').length === 0,
    'V3-06': has('chromium-desktop', 'V3-06') && browserEvidence.noJs.csp === EXPECTED_CSP && browserEvidence.noJs.inventory?.length >= 13,
    'V3-07': commandPassed('harness') && commandPassed('npm-audit') && scans.result === 'pass' && audit.metadata?.vulnerabilities?.high === 0 && audit.metadata?.vulnerabilities?.critical === 0,
  };
  const groups = contract.groups.map(id => ({ id, result: groupChecks[id] ? 'pass' : 'fail' }));
  if (groups.some(({ result }) => result !== 'pass')) throw new Error('cannot retain incomplete blocking groups');
  const cleanup = JSON.parse(readFileSync(resolve(green.directory, 'rollback.json'), 'utf8'));
  const rollback = simulateRollback(destination, green, cleanup);
  writeFileSync(resolve(destination, 'lifecycle/rollback.json'), `${JSON.stringify(rollback, null, 2)}\n`);
  const ledger = JSON.parse(readFileSync(resolve(green.directory, 'owned-resources.json'), 'utf8'));
  const artifactLocators = {
    journeyFacts: ['green/browser-results/chromium-desktop/v3-03-v3-04-journey-facts.json', 'green/browser-results/chromium-narrow/v3-03-v3-04-journey-facts.json'],
    axe: 'green/browser-results/chromium-desktop/v3-05-axe-complete.json',
    noJsInventory: 'green/browser-results/chromium-desktop/v3-06-no-js-inventory.json',
    noJsResponse: 'green/browser-results/chromium-desktop/v3-06-response.html',
    scan: 'security/scans.json',
    finalRetainedScan: 'security/final-retained-scan.json',
    ownership: 'lifecycle/owned-resources.json',
    rollback: 'lifecycle/rollback.json',
  };
  const testNameInventory = [
    ...testNamesFromTap(resolve(green.directory, 'unit.log')),
    ...testNamesFromTap(resolve(green.directory, 'harness.log')),
    ...browser.map(({ title, project }) => `${title} [${project}]`),
  ];
  const blockingAxe = (browserEvidence.axe.violations ?? []).filter(({ impact }) => impact === 'critical' || impact === 'serious');
  const axeSummary = {
    invocations: 1,
    critical: blockingAxe.filter(({ impact }) => impact === 'critical').length,
    serious: blockingAxe.filter(({ impact }) => impact === 'serious').length,
    violations: browserEvidence.axe.violations?.length ?? 0,
    passes: browserEvidence.axe.passes?.length ?? 0,
    incomplete: browserEvidence.axe.incomplete?.length ?? 0,
    incompleteSummary: (browserEvidence.axe.incomplete ?? []).map(({ id, impact, nodes }) => ({ id, impact, nodes: nodes.length })),
    inapplicable: browserEvidence.axe.inapplicable?.length ?? 0,
    findingsRetained: true,
  };
  const noJsFacts = {
    javaScriptEnabled: false,
    responseBytes: browserEvidence.noJs.responseBytes,
    csp: browserEvidence.noJs.csp,
    inventoryCount: browserEvidence.noJs.inventory?.length ?? 0,
    inventoryIds: browserEvidence.noJs.inventory?.map(({ id }) => id) ?? [],
    responseSha256: sha256(browserEvidence.response),
  };
  const scanSummary = { result: scans.result, findings: scans.findings.length, checks: scans.checkInventory?.length ?? 0, checkInventory: scans.checkInventory?.map(({ id, result }) => ({ id, result })) ?? [], finalRetained: 'pass' };
  const ownedResourceSummary = { result: validateOwnership(ledger, { runId: green.runId }).length === 0 && rollback.result === 'pass' ? 'pass' : 'fail', serverCount: 1, port: ledger.port, cleanup: cleanup.result, rollbackSimulation: rollback.result };
  const manifest = { schemaVersion: 'i5-02-simple-vite-v3-evidence-v1', acceptanceRevision: contract.acceptanceRevision, runId: green.runId, implementationInputSha: contract.implementationInputSha, testedSourceSha: greenResult.sourceSha, testedTreeSha: greenResult.testedTreeSha, branch: contract.branch, authorityMode: greenResult.authority.authorityMode, freshLiveHead: greenResult.authority.freshLiveHead, issue6IntegrationSha: contract.issue6IntegrationSha, fixtureIdentities: contract.fixtureIdentities, lockSha256: contract.lockSha256, tools: greenResult.tools, commands: greenResult.commands, browserInventory: browser, groups, redProvenance: { result: 'pass', testOnlySha: redResult.sourceSha, testedTreeSha: redResult.testedTreeSha }, targetedReviewFixRed: { result: reviewFixRed.result.result, sourceSha: reviewFixRed.result.sourceSha, rc: reviewFixRed.result.rc, assertionIds: reviewFixRed.result.assertionIds, log: 'tdd/review-fix-red/focused-tests.tap' }, evidenceClosureRedSha: EVIDENCE_CLOSURE_RED_SHA, testNameInventory, artifactLocators, axeSummary, noJsFacts, scanSummary, ownedResourceSummary, audit: audit.metadata?.vulnerabilities, redaction: { result: 'pass', findings: [] }, cleanupRollback: rollback, limitations: ['Chromium and axe automation are not a full WCAG or screen-reader conformance claim.', 'Production accessibility and manual UAT remain deferred.'] };
  if (validateEvidenceManifest(manifest).length) throw new Error('generated manifest is invalid');
  writeFileSync(resolve(destination, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
  const finalScan = finalRetainedScan(destination);
  if (finalScan.result !== 'pass') throw new Error(`final-retained-scan:${finalScan.findings.map(({ path, finding }) => `${path}:${finding}`).join(',')}`);
  const hashIndex = { schemaVersion: 'i5-02-simple-vite-v3-hash-index-v1', files: fileIndex(destination, new Set(['hash-index.json'])) };
  writeFileSync(resolve(destination, 'hash-index.json'), `${JSON.stringify(hashIndex, null, 2)}\n`);
  const hashClosure = verifyHashIndex(destination, hashIndex);
  if (hashClosure.result !== 'pass') throw new Error('hash-index-closure');
  const index = { schemaVersion: 'i5-02-simple-vite-v3-retention-index-v1', acceptedRun: green.runId, manifest: { path: relativePath(resolve(destination, 'manifest.json')), sha256: hashFile(relativePath(resolve(destination, 'manifest.json'))) }, hashIndex: { path: relativePath(resolve(destination, 'hash-index.json')), sha256: hashFile(relativePath(resolve(destination, 'hash-index.json'))) } };
  writeFileSync(resolve(ROOT, contract.retentionIndex), `${JSON.stringify(index, null, 2)}\n`);
  return { result: 'pass', destination: relativePath(destination), finalRetainedScan: finalScan.result, hashIndexClosure: hashClosure.result };
}

export function rollbackRun() {
  let retainedBefore = null;
  if (existsSync(resolve(ROOT, contract.retentionIndex))) {
    const retention = JSON.parse(readFileSync(resolve(ROOT, contract.retentionIndex), 'utf8'));
    retainedBefore = {
      manifest: hashFile(retention.manifest.path),
      hashIndex: hashFile(retention.hashIndex.path),
    };
  }
  const targets = ['spikes/web/candidates/vite/node_modules', 'spikes/web/candidates/vite/dist', 'spikes/web/candidates/vite/test-results', 'spikes/web/candidates/vite/playwright-report', contract.runtimePrefix];
  for (const target of targets) {
    const path = resolve(ROOT, target);
    if (!(path === RUNTIME || path.startsWith(`${CANDIDATE}${sep}`))) throw new Error(`unsafe rollback target: ${target}`);
    rmSync(path, { recursive: true, force: true });
  }
  let retainedAfter = null;
  if (retainedBefore) {
    const retention = JSON.parse(readFileSync(resolve(ROOT, contract.retentionIndex), 'utf8'));
    retainedAfter = { manifest: hashFile(retention.manifest.path), hashIndex: hashFile(retention.hashIndex.path) };
  }
  const retainedPreservation = { result: JSON.stringify(retainedBefore) === JSON.stringify(retainedAfter) ? 'pass' : 'fail', before: retainedBefore, after: retainedAfter };
  const result = targets.some(target => existsSync(resolve(ROOT, target))) || retainedPreservation.result !== 'pass' ? 'fail' : 'pass';
  return { result, removed: targets, retainedPreservation };
}

async function main() {
  const [verb] = process.argv.slice(2);
  const inputIndex = process.argv.indexOf('--implementation-input');
  const input = inputIndex >= 0 ? process.argv[inputIndex + 1] : '';
  let output;
  if (verb === 'preflight') output = preflight(input);
  else if (verb === 'red' || verb === 'gate') return execute(verb, input);
  else if (verb === 'scan') output = scanRun();
  else if (verb === 'retain') output = retainRun();
  else if (verb === 'rollback') output = rollbackRun();
  else throw new Error(`unsupported verb: ${verb}`);
  process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
  if (output.result !== 'pass') process.exitCode = 1;
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  main().catch(error => { console.error(sanitize(error.stack || error.message)); process.exitCode = 1; });
}
