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
  if (implementationInput !== contract.implementationInputSha) failures.push('implementation-input-mismatch');
  if (git(['branch', '--show-current']) !== contract.branch) failures.push('branch-mismatch');
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
  return { result: failures.length ? 'fail' : 'pass', failures, changedPaths: statusPaths() };
}

function sanitize(text) {
  return String(text).split(ROOT).join('<WORKSPACE>');
}

async function runBounded(name, command, ceilingMs, directory) {
  const [program, ...args] = command;
  const startedAt = new Date().toISOString();
  const started = process.hrtime.bigint();
  return await new Promise(resolveResult => {
    const child = spawn(program, args, { cwd: ROOT, env: { ...process.env, BASE_URL: 'http://127.0.0.1:4175' }, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '', stderr = '', timedOut = false;
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.stderr.on('data', chunk => { stderr += chunk; });
    const timer = setTimeout(() => { timedOut = true; child.kill('SIGTERM'); }, ceilingMs);
    child.on('close', (code, signal) => {
      clearTimeout(timer);
      const result = { name, command, startedAt, durationMs: Number(process.hrtime.bigint() - started) / 1e6, rc: code ?? 1, signal, timedOut, stdout: sanitize(stdout), stderr: sanitize(stderr) };
      writeFileSync(resolve(directory, `${name}.json`), `${JSON.stringify(result, null, 2)}\n`);
      writeFileSync(resolve(directory, `${name}.log`), `${result.stdout}${result.stderr}`);
      resolveResult(result);
    });
  });
}

function processFingerprint(pid) {
  const result = spawnSync('ps', ['-p', String(pid), '-o', 'pgid=', '-o', 'lstart=', '-o', 'command='], { encoding: 'utf8' });
  return result.status === 0 ? result.stdout.trim().replace(/\s+/g, ' ') : '';
}

async function startHost(runId, directory) {
  const hostPath = resolve(ROOT, 'spikes/web/harness/scripts/candidate-static-host.mjs');
  const command = [process.execPath, hostPath, resolve(CANDIDATE, 'dist'), String(contract.port)];
  const child = spawn(command[0], command.slice(1), { cwd: ROOT, detached: true, stdio: ['ignore', 'pipe', 'pipe'] });
  let output = '';
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
  const fingerprint = processFingerprint(child.pid);
  const ledger = { pid: child.pid, processGroup: child.pid, fingerprint: sanitize(fingerprint), cwd: '.', command: command.map(sanitize), root: 'spikes/web/candidates/vite/dist', port: contract.port, runId, childHandle: true };
  const liveLedger = { ...ledger, fingerprint };
  writeFileSync(resolve(directory, 'owned-resources.json'), `${JSON.stringify(ledger, null, 2)}\n`);
  return { child, ledger: liveLedger };
}

async function stopHost(owned) {
  if (!owned) return;
  const current = processFingerprint(owned.ledger.pid);
  if (!current || current !== owned.ledger.fingerprint) throw new Error('owned host fingerprint changed; refusing to signal');
  process.kill(-owned.ledger.processGroup, 'SIGTERM');
  await new Promise(resolveWait => {
    const timeout = setTimeout(() => {
      if (processFingerprint(owned.ledger.pid) === owned.ledger.fingerprint) process.kill(-owned.ledger.processGroup, 'SIGKILL');
      resolveWait();
    }, 5_000);
    owned.child.once('exit', () => { clearTimeout(timeout); resolveWait(); });
  });
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

function playwrightInventory(logPath) {
  const output = readFileSync(logPath, 'utf8');
  const reportStart = output.indexOf('{');
  if (reportStart < 0) throw new Error('Playwright JSON report was not emitted');
  const report = JSON.parse(output.slice(reportStart));
  const entries = report.suites.flatMap(suite => suite.specs).flatMap(spec => spec.tests.map(entry => ({
    title: spec.title,
    project: entry.projectName,
    status: entry.status,
    retries: entry.results.reduce((maximum, result) => Math.max(maximum, result.retry || 0), 0),
  })));
  return entries.sort((a, b) => `${a.project}:${a.title}`.localeCompare(`${b.project}:${b.title}`));
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

export function scanRun() {
  const green = latest('gate');
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
  const output = { schemaVersion: 'i5-02-simple-vite-v3-scan-v1', result: findings.length ? 'fail' : 'pass', findings };
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

export function retainRun() {
  const red = latest('red');
  const green = latest('gate');
  const redResult = JSON.parse(readFileSync(resolve(red.directory, 'result.json'), 'utf8'));
  const greenResult = JSON.parse(readFileSync(resolve(green.directory, 'result.json'), 'utf8'));
  const scans = JSON.parse(readFileSync(resolve(green.directory, 'scans.json'), 'utf8'));
  if (redResult.result !== 'pass' || greenResult.result !== 'pass' || scans.result !== 'pass') throw new Error('cannot retain failed RED/GREEN/scan');
  const destination = resolve(ROOT, contract.retainedPrefix, green.runId);
  if (existsSync(destination)) throw new Error('immutable run destination already exists');
  mkdirSync(resolve(destination, 'tdd/red'), { recursive: true });
  mkdirSync(resolve(destination, 'green'), { recursive: true });
  mkdirSync(resolve(destination, 'security'), { recursive: true });
  mkdirSync(resolve(destination, 'lifecycle'), { recursive: true });
  for (const name of ['unit.log', 'playwright.log', 'result.json']) if (existsSync(resolve(red.directory, name))) cpSync(resolve(red.directory, name), resolve(destination, 'tdd/red', name));
  for (const name of ['install.log', 'build.log', 'unit.log', 'harness.log', 'playwright.log', 'result.json', 'response-index.html']) if (existsSync(resolve(green.directory, name))) cpSync(resolve(green.directory, name), resolve(destination, 'green', name));
  if (existsSync(resolve(green.directory, 'browser-results'))) cpSync(resolve(green.directory, 'browser-results'), resolve(destination, 'green/browser-results'), { recursive: true });
  cpSync(resolve(green.directory, 'npm-audit.log'), resolve(destination, 'security/npm-audit.json'));
  cpSync(resolve(green.directory, 'scans.json'), resolve(destination, 'security/scans.json'));
  cpSync(resolve(green.directory, 'owned-resources.json'), resolve(destination, 'lifecycle/owned-resources.json'));
  cpSync(resolve(green.directory, 'rollback.json'), resolve(destination, 'lifecycle/rollback.json'));
  const audit = JSON.parse(readFileSync(resolve(green.directory, 'npm-audit.log'), 'utf8'));
  const browser = greenResult.browserInventory;
  const has = (project, fragment) => browser.some(entry => entry.project === project && entry.title.includes(fragment) && entry.status === 'expected' && entry.retries === 0);
  const commandPassed = name => greenResult.commands.some(command => command.name === name && command.rc === 0 && !command.timedOut);
  const groupChecks = {
    'V3-01': commandPassed('install') && commandPassed('build') && greenResult.packageBefore === greenResult.packageAfter && greenResult.lockBefore === greenResult.lockAfter,
    'V3-02': commandPassed('unit'),
    'V3-03': has('chromium-desktop', 'V3-03 V3-04') && has('chromium-narrow', 'V3-03 V3-04'),
    'V3-04': has('chromium-desktop', 'V3-03 V3-04') && has('chromium-narrow', 'V3-03 V3-04'),
    'V3-05': has('chromium-desktop', 'V3-05'),
    'V3-06': has('chromium-desktop', 'V3-06'),
    'V3-07': commandPassed('harness') && commandPassed('npm-audit') && scans.result === 'pass',
  };
  const groups = contract.groups.map(id => ({ id, result: groupChecks[id] ? 'pass' : 'fail' }));
  const rollback = JSON.parse(readFileSync(resolve(green.directory, 'rollback.json'), 'utf8'));
  const manifest = { schemaVersion: 'i5-02-simple-vite-v3-evidence-v1', acceptanceRevision: contract.acceptanceRevision, runId: green.runId, implementationInputSha: contract.implementationInputSha, testedSourceSha: greenResult.sourceSha, testedTreeSha: greenResult.testedTreeSha, branch: contract.branch, issue6IntegrationSha: contract.issue6IntegrationSha, fixtureIdentities: contract.fixtureIdentities, lockSha256: contract.lockSha256, tools: greenResult.tools, commands: greenResult.commands, browserInventory: browser, groups, redProvenance: { result: 'pass', testOnlySha: redResult.sourceSha, testedTreeSha: redResult.testedTreeSha }, audit: audit.metadata?.vulnerabilities, redaction: { result: 'pass', findings: [] }, cleanupRollback: rollback, limitations: ['Chromium and axe automation are not a full WCAG or screen-reader conformance claim.', 'Production accessibility and manual UAT remain deferred.'] };
  if (validateEvidenceManifest(manifest).length) throw new Error('generated manifest is invalid');
  writeFileSync(resolve(destination, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
  writeFileSync(resolve(destination, 'hash-index.json'), `${JSON.stringify({ schemaVersion: 'i5-02-simple-vite-v3-hash-index-v1', files: fileIndex(destination, new Set(['hash-index.json'])) }, null, 2)}\n`);
  const index = { schemaVersion: 'i5-02-simple-vite-v3-retention-index-v1', acceptedRun: green.runId, manifest: { path: relativePath(resolve(destination, 'manifest.json')), sha256: hashFile(relativePath(resolve(destination, 'manifest.json'))) }, hashIndex: { path: relativePath(resolve(destination, 'hash-index.json')), sha256: hashFile(relativePath(resolve(destination, 'hash-index.json'))) } };
  writeFileSync(resolve(ROOT, contract.retentionIndex), `${JSON.stringify(index, null, 2)}\n`);
  return { result: 'pass', destination: relativePath(destination) };
}

export function rollbackRun() {
  const targets = ['spikes/web/candidates/vite/node_modules', 'spikes/web/candidates/vite/dist', 'spikes/web/candidates/vite/test-results', 'spikes/web/candidates/vite/playwright-report', contract.runtimePrefix];
  for (const target of targets) {
    const path = resolve(ROOT, target);
    if (!(path === RUNTIME || path.startsWith(`${CANDIDATE}${sep}`))) throw new Error(`unsafe rollback target: ${target}`);
    rmSync(path, { recursive: true, force: true });
  }
  return { result: targets.some(target => existsSync(resolve(ROOT, target))) ? 'fail' : 'pass', removed: targets };
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
