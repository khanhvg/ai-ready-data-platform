import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { chmodSync, existsSync, linkSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync, symlinkSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:net';
import { tmpdir } from 'node:os';
import { dirname, resolve } from 'node:path';
import test from 'node:test';
import { ROOT, contract, scanText, validateChangedPaths, validateEvidenceManifest, validateOwnership } from '../scripts/simple-vite-v3.mjs';

const wait = milliseconds => new Promise(resolveWait => setTimeout(resolveWait, milliseconds));
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');

function inspectBuiltOutput(root) {
  if (typeof globalThis.__viteV3ScanBuiltOutput === 'function') return globalThis.__viteV3ScanBuiltOutput(root);
  return { result: 'pass', requiredIndex: false, inventory: [], findings: [], failures: [] };
}

async function withBuiltOutputScanner(callback) {
  const runner = await import(`../scripts/simple-vite-v3.mjs?built-output=${Date.now()}-${Math.random()}`);
  globalThis.__viteV3ScanBuiltOutput = runner.scanBuiltOutput;
  try {
    return callback();
  } finally {
    delete globalThis.__viteV3ScanBuiltOutput;
  }
}

function processExists(pid) {
  if (!Number.isInteger(pid) || pid <= 1) return false;
  try { process.kill(pid, 0); return true; } catch (error) { return error.code === 'EPERM'; }
}

function killPid(pid) {
  if (!processExists(pid)) return;
  try { process.kill(pid, 'SIGKILL'); } catch (error) { if (error.code !== 'ESRCH') throw error; }
}

function processGroup(pid) {
  const result = spawnSync('ps', ['-p', String(pid), '-o', 'pgid='], { encoding: 'utf8' });
  const pgid = result.status === 0 ? Number(result.stdout.trim()) : NaN;
  return Number.isInteger(pgid) ? pgid : null;
}

async function loadInstrumentedRunner(transform = source => source) {
  const sourcePath = resolve(ROOT, 'spikes/web/harness/scripts/simple-vite-v3.mjs');
  const temporaryPath = resolve(dirname(sourcePath), `.simple-vite-v3-test-${process.pid}-${Date.now()}.mjs`);
  const source = `${transform(readFileSync(sourcePath, 'utf8'))}\nexport { cleanupCandidateRuntime, runBounded, sanitize, startHost };\n`;
  writeFileSync(temporaryPath, source);
  try {
    return { module: await import(`${new URL(`file://${temporaryPath}`).href}?test=${Date.now()}`), temporaryPath };
  } catch (error) {
    rmSync(temporaryPath, { force: true });
    throw error;
  }
}

test('V3-07 harness contract closes authority, seven groups, commands, and write paths', () => {
  assert.equal(contract.implementationInputSha, '4cfd01f891655670b5a43a362b1567bcaaf4a824');
  assert.deepEqual(contract.groups, ['V3-01', 'V3-02', 'V3-03', 'V3-04', 'V3-05', 'V3-06', 'V3-07']);
  assert.equal(contract.port, 4175);
  assert.deepEqual(contract.commands.install, ['npm', '--prefix', 'spikes/web/candidates/vite', 'ci', '--ignore-scripts', '--no-audit', '--no-fund']);
  assert.equal(contract.allowedPrefixes.length, 1);
  assert.equal(contract.allowedPrefixes[0], 'spikes/web/evidence/retained/simple-vite-v3/');
  assert.equal(contract.authorityLookupMs, 60000);
  for (const unsupported of ['authority', 'verb', 'red', 'gate']) assert.equal(contract.ceilingsMs[unsupported], undefined, `${unsupported} outer ceiling must not be declared without enforcement`);
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

test('V3-07 retained scanner catches local temporary workspace paths without flagging neutral locators', () => {
  for (const sample of [
    '/private/tmp/vite-red/work/focused-tests.tap',
    '/private/var/folders/ab/cd/T/vite-red/result.json',
    '/var/folders/ab/cd/T/vite-red/result.json',
    '/tmp/vite-red/result.json',
    'file:///private/tmp/vite-red/work/focused-tests.tap:19:1',
    'file:///var/folders/ab/cd/T/vite-red/result.json',
    'file:///tmp/vite-red/result.json',
  ]) assert.ok(scanText(sample).includes('absolutePrivatePath'), sample);
  for (const neutral of [
    '/tmp/',
    '/var/folders/',
    '/private/',
    'file://<WORKSPACE>/spikes/web/harness/tests/simple-vite-v3.test.mjs:1:1',
    'https://example.com/tmp/report.json',
    'spikes/web/evidence/retained/simple-vite-v3/manifest.json',
    'Document the /tmp/ and /var/folders/ workspace classes.',
  ]) assert.equal(scanText(neutral).includes('absolutePrivatePath'), false, neutral);
});

test('V3-07 retained sanitizer normalizes local temporary workspace paths before writing evidence', async () => {
  const loaded = await loadInstrumentedRunner();
  try {
    const input = [
      '/private/tmp/vite-red/work/focused-tests.tap',
      'file:///private/tmp/vite-red/work/focused-tests.tap:19:1',
      '/private/var/folders/ab/cd/T/vite-red/result.json',
      '/var/folders/ab/cd/T/vite-red/result.json',
      '/tmp/vite-red/result.json',
      'https://example.com/tmp/report.json',
      'spikes/web/evidence/retained/simple-vite-v3/manifest.json',
    ].join('\n');
    assert.equal(loaded.module.sanitize(input), [
      '<WORKSPACE>/work/focused-tests.tap',
      'file://<WORKSPACE>/work/focused-tests.tap:19:1',
      '<WORKSPACE>/result.json',
      '<WORKSPACE>/result.json',
      '<WORKSPACE>/result.json',
      'https://example.com/tmp/report.json',
      'spikes/web/evidence/retained/simple-vite-v3/manifest.json',
    ].join('\n'));
  } finally {
    rmSync(loaded.temporaryPath, { force: true });
  }
});

test('V3-07 authorized retained correction replaces exactly 12 paths and binds its attestation', () => {
  const run = 'spikes/web/evidence/retained/simple-vite-v3/v3-20260721T202415031Z-52a03869';
  const tapLocator = `${run}/tdd/fifth-targeted-review-fix-red/focused-tests.tap`;
  const original = spawnSync('git', ['show', `aaddb3af4dade6751d1209bf9f5b25f28b5a06ec:${tapLocator}`], { cwd: ROOT, encoding: 'utf8' });
  assert.equal(original.status, 0, original.stderr);
  const rawPrefix = /\/private\/tmp\/vite-fifth-red-adf79ae/g;
  assert.equal(original.stdout.match(rawPrefix)?.length, 12);
  const corrected = readFileSync(resolve(ROOT, tapLocator), 'utf8');
  assert.equal(corrected.match(rawPrefix)?.length ?? 0, 0);
  assert.equal(corrected, original.stdout.replace(rawPrefix, '<WORKSPACE>'), 'only the 12 authorized path prefixes may change');

  const correctionLocator = `${run}/correction.json`;
  assert.equal(existsSync(resolve(ROOT, correctionLocator)), true, 'authorized correction attestation must exist');
  const correction = JSON.parse(readFileSync(resolve(ROOT, correctionLocator), 'utf8'));
  assert.equal(correction.ownerCommentUrl, 'https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5038913224');
  assert.deepEqual(correction.replacement, { class: 'local-absolute-path', count: 12, from: 'raw-local-workspace-prefix', to: '<WORKSPACE>' });
  assert.equal(correction.reason, 'local-absolute-path-redaction');
  assert.equal(correction.contentMeaningChanged, false);
  assert.deepEqual(correction.priorHashes, {
    tapSha256: 'b90cde68a7a925676df0c920044b1df00deaac9be293c4a1ee986c54fb3823a1',
    manifestSha256: 'f0f03ba4aeabd39aeccb99f2dfef9a6544f276fb164a95c37f9eeeca5920bc1b',
    hashIndexSha256: 'bf670df7d3ce20a79ed24b2c4f63c6afd83cea981a7216ce87c739acc9f71a7f',
  });
  assert.equal(correction.correctedHashes.tapSha256, sha256(corrected));
  assert.match(correction.correctedHashes.manifestSha256, /^[0-9a-f]{64}$/);
  assert.match(correction.correctedHashes.hashIndexSha256, /^[0-9a-f]{64}$/);
  assert.equal(correction.correctedHashes.scope, 'canonical-json-with-correction-digest-fields-omitted');
  assert.equal(correction.correctionSourceHead, 'aaddb3af4dade6751d1209bf9f5b25f28b5a06ec');
  assert.match(correction.correctionOutputHead, /^[0-9a-f]{40}$/);

  const manifest = JSON.parse(readFileSync(resolve(ROOT, run, 'manifest.json'), 'utf8'));
  assert.equal(manifest.correctionAttestation.path, 'correction.json');
  assert.equal(manifest.correctionAttestation.sha256, sha256(readFileSync(resolve(ROOT, correctionLocator))));
  const hashIndex = JSON.parse(readFileSync(resolve(ROOT, run, 'hash-index.json'), 'utf8'));
  assert.ok(hashIndex.files.some(entry => entry.path === 'correction.json' && entry.sha256 === manifest.correctionAttestation.sha256));

  const canonicalManifest = structuredClone(manifest);
  delete canonicalManifest.correctionAttestation.sha256;
  assert.equal(correction.correctedHashes.manifestSha256, sha256(`${JSON.stringify(canonicalManifest, null, 2)}\n`));
  const canonicalHashIndex = structuredClone(hashIndex);
  for (const path of ['correction.json', 'manifest.json']) delete canonicalHashIndex.files.find(entry => entry.path === path).sha256;
  assert.equal(correction.correctedHashes.hashIndexSha256, sha256(`${JSON.stringify(canonicalHashIndex, null, 2)}\n`));

  const indexed = new Map(hashIndex.files.map(entry => [entry.path, entry]));
  const actual = [];
  const walk = directory => {
    for (const name of readdirSync(directory).sort()) {
      const path = resolve(directory, name);
      if (statSync(path).isDirectory()) walk(path);
      else if (!path.endsWith('/hash-index.json')) actual.push(path);
    }
  };
  walk(resolve(ROOT, run));
  assert.deepEqual([...indexed.keys()], actual.map(path => path.slice(resolve(ROOT, run).length + 1)));
  for (const path of actual) {
    const locator = path.slice(resolve(ROOT, run).length + 1);
    const bytes = readFileSync(path);
    assert.equal(indexed.get(locator).bytes, bytes.length, locator);
    assert.equal(indexed.get(locator).sha256, sha256(bytes), locator);
    if (locator !== 'security/final-retained-scan.json') assert.deepEqual(scanText(bytes.toString('utf8')), [], locator);
  }
  const finalScan = JSON.parse(readFileSync(resolve(ROOT, run, 'security/final-retained-scan.json'), 'utf8'));
  assert.equal(finalScan.result, 'pass');
  assert.equal(finalScan.scannedFiles, hashIndex.files.length - 1, 'every indexed text file except the scan record itself must be covered');
  assert.deepEqual(finalScan.findings, []);
});

test('V3-07 scanner context keeps authored injection detection while built output excludes only that rule', async () => {
  const dist = mkdtempSync(resolve(tmpdir(), 'vite-v3-built-context-'));
  const runtime = resolve(dist, 'runtime.js');
  try {
    writeFileSync(resolve(dist, 'index.html'), '<!doctype html>\n');
    assert.deepEqual(scanText('element.innerHTML=value'), ['unsafeInjection']);
    writeFileSync(runtime, 'function reactRuntime(node,value){node.innerHTML=value}\n');
    await withBuiltOutputScanner(() => {
      const clean = inspectBuiltOutput(dist);
      assert.equal(clean.result, 'pass', 'React-runtime-shaped built output must not trip the authored-source heuristic');
      assert.deepEqual(clean.ruleIds, ['privateKey', 'credential', 'absolutePrivatePath', 'email', 'phone', 'governmentIdentifier', 'remoteImport', 'sourceMap']);

      writeFileSync(runtime, 'function reactRuntime(node,value){node.innerHTML=value};const token="abcdefghijk";/* /Users/private/work/repo learner@example.com */import("https://example.com/a.js");//# sourceMappingURL=runtime.js.map\n');
      const unsafe = inspectBuiltOutput(dist);
      assert.equal(unsafe.result, 'fail', 'built output must retain every non-injection content rule');
      assert.deepEqual(unsafe.findings.map(({ finding }) => finding), ['absolutePrivatePath', 'credential', 'email', 'remoteImport', 'sourceMap']);
    });
  } finally {
    rmSync(dist, { recursive: true, force: true });
  }
});

test('V3-07 built-output scan fails closed when the required root is missing', async () => {
  const temporaryRoot = mkdtempSync(resolve(tmpdir(), 'vite-v3-built-missing-'));
  const missing = resolve(temporaryRoot, 'dist');
  try {
    await withBuiltOutputScanner(() => {
      const scan = inspectBuiltOutput(missing);
      assert.equal(scan.result, 'fail', 'missing required built-output root must fail closed');
      assert.ok(scan.failures.includes('built-output-missing'));
      assert.equal(scan.inventory.length, 0);
    });
  } finally {
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
});

test('V3-07 built-output scan detects forbidden markers in generated JS, CSS, and source maps', async () => {
  const dist = mkdtempSync(resolve(tmpdir(), 'vite-v3-built-unsafe-'));
  try {
    mkdirSync(resolve(dist, 'assets'));
    writeFileSync(resolve(dist, 'index.html'), '<!doctype html><script src="/assets/app.js"></script>\n');
    writeFileSync(resolve(dist, 'assets/app.js'), 'const token="abcdefghijk";\n');
    writeFileSync(resolve(dist, 'assets/app.css'), '/* /Users/private/work/repo */\n');
    writeFileSync(resolve(dist, 'assets/app.js.map'), '{"version":3,"sources":["learner@example.com"]}\n');
    writeFileSync(resolve(dist, 'assets/leak.txt'), 'client_secret="generated-secret"\n');
    await withBuiltOutputScanner(() => {
      const scan = inspectBuiltOutput(dist);
      assert.equal(scan.result, 'fail', 'unsafe generated assets must fail content safety');
      assert.deepEqual(scan.findings.map(({ path }) => path).sort(), ['assets/app.css', 'assets/app.js', 'assets/app.js.map', 'assets/leak.txt']);
      assert.ok(scan.findings.some(({ path, finding }) => path === 'assets/app.js' && finding === 'credential'));
      assert.ok(scan.findings.some(({ path, finding }) => path === 'assets/app.css' && finding === 'absolutePrivatePath'));
      assert.ok(scan.findings.some(({ path, finding }) => path === 'assets/app.js.map' && finding === 'email'));
      assert.ok(scan.findings.some(({ path, finding }) => path === 'assets/leak.txt' && finding === 'credential'));
    });
  } finally {
    rmSync(dist, { recursive: true, force: true });
  }
});

test('V3-07 clean complete built-output scan emits normalized path and SHA-256 inventory', async () => {
  const dist = mkdtempSync(resolve(tmpdir(), 'vite-v3-built-clean-'));
  const assets = new Map([
    ['index.html', Buffer.from('<!doctype html><link rel="stylesheet" href="/assets/app.css"><script src="/assets/app.js"></script>\n')],
    ['assets/app.css', Buffer.from('body { color: #123456; }\n')],
    ['assets/app.js', Buffer.from('document.documentElement.dataset.ready = "true";\n')],
    ['assets/app.js.map', Buffer.from('{"version":3,"sources":[],"names":[],"mappings":""}\n')],
    ['assets/manifest.json', Buffer.from('{"entry":"assets/app.js"}\n')],
  ]);
  try {
    mkdirSync(resolve(dist, 'assets'));
    for (const [path, bytes] of assets) writeFileSync(resolve(dist, path), bytes);
    await withBuiltOutputScanner(() => {
      const scan = inspectBuiltOutput(dist);
      assert.equal(scan.result, 'pass');
      assert.equal(scan.requiredIndex, true);
      assert.deepEqual(scan.findings, []);
      assert.deepEqual(scan.inventory, [...assets].map(([path, bytes]) => ({ path, bytes: bytes.length, sha256: sha256(bytes) })).sort((a, b) => Buffer.from(a.path).compare(Buffer.from(b.path))));
    });
  } finally {
    rmSync(dist, { recursive: true, force: true });
  }
});

test('V3-07 built-output scan rejects symlinks, hardlinks, special files, and their escape targets', async () => {
  const temporaryRoot = mkdtempSync(resolve(tmpdir(), 'vite-v3-built-structure-'));
  const dist = resolve(temporaryRoot, 'dist');
  const outside = resolve(temporaryRoot, 'outside.js');
  const socket = resolve(dist, 'runtime.sock');
  const server = createServer();
  try {
    mkdirSync(dist);
    writeFileSync(resolve(dist, 'index.html'), '<!doctype html>\n');
    writeFileSync(outside, 'const safe = true;\n');
    linkSync(outside, resolve(dist, 'hardlink.js'));
    symlinkSync(outside, resolve(dist, 'escape.js'));
    await new Promise((resolveListening, reject) => server.once('error', reject).listen(socket, resolveListening));
    await withBuiltOutputScanner(() => {
      const scan = inspectBuiltOutput(dist);
      assert.equal(scan.result, 'fail');
      assert.ok(scan.failures.includes('built-output-symlink:escape.js'));
      assert.ok(scan.failures.includes('built-output-hardlink:hardlink.js'));
      assert.ok(scan.failures.includes('built-output-special-file:runtime.sock'));
      assert.deepEqual(scan.inventory.map(({ path }) => path), ['index.html']);
    });
  } finally {
    await new Promise(resolveClose => server.close(resolveClose));
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
});

test('V3-07 structural built-output scan failure records evidence before run-owned cleanup', async () => {
  const temporaryRoot = mkdtempSync(resolve(tmpdir(), 'vite-v3-built-cleanup-'));
  const candidate = resolve(temporaryRoot, 'candidate');
  const dist = resolve(candidate, 'dist');
  const run = resolve(temporaryRoot, 'run');
  let temporaryPath;
  try {
    mkdirSync(dist, { recursive: true });
    mkdirSync(resolve(candidate, 'node_modules'));
    mkdirSync(run);
    writeFileSync(resolve(dist, 'index.html'), '<!doctype html>\n');
    symlinkSync(resolve(temporaryRoot, 'missing.js'), resolve(dist, 'dangling.js'));
    writeFileSync(resolve(run, 'result.json'), '{"result":"fail"}\n');
    const loaded = await loadInstrumentedRunner(source => source.replace("const CANDIDATE = resolve(ROOT, 'spikes/web/candidates/vite');", `const CANDIDATE = ${JSON.stringify(candidate)};`));
    temporaryPath = loaded.temporaryPath;
    const scan = loaded.module.scanBuiltOutput(dist);
    writeFileSync(resolve(run, 'built-output-scan.json'), `${JSON.stringify(scan, null, 2)}\n`);
    const cleanup = loaded.module.cleanupCandidateRuntime(run);
    assert.equal(scan.result, 'fail');
    assert.ok(scan.failures.includes('built-output-symlink:dangling.js'));
    assert.equal(cleanup.result, 'pass');
    assert.equal(existsSync(dist), false);
    assert.equal(existsSync(resolve(candidate, 'node_modules')), false);
    assert.equal(existsSync(resolve(run, 'built-output-scan.json')), true);
  } finally {
    if (temporaryPath) rmSync(temporaryPath, { force: true });
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
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
  assert.ok(source.indexOf('builtOutputScan = scanBuiltOutput') < source.indexOf('const cleanup = cleanupCandidateRuntime(directory)'), 'built output must be scanned and recorded before run-owned dist cleanup');
  assert.match(source, /security\/built-output-scan\.json/, 'retained evidence must include the complete built-output inventory');
  assert.doesNotMatch(source, /score-anchors|Firefox|webkit|VoiceOver|CuaDriver|terraform|historicalTimer/i);
});

test('V3-07 fast bounded command exits promptly without referenced harness timers', () => {
  const directory = resolve(ROOT, '.artifacts/runtime/i5-02/focused-fast-exit');
  const sourcePath = resolve(ROOT, 'spikes/web/harness/scripts/simple-vite-v3.mjs');
  const temporaryPath = resolve(dirname(sourcePath), `.simple-vite-v3-exit-test-${process.pid}-${Date.now()}.mjs`);
  rmSync(directory, { recursive: true, force: true });
  mkdirSync(directory, { recursive: true });
  writeFileSync(temporaryPath, `${readFileSync(sourcePath, 'utf8')}\nexport { runBounded };\n`);
  try {
    const program = [
      `import { runBounded } from ${JSON.stringify(new URL(`file://${temporaryPath}`).href)};`,
      `const result = await runBounded('fast-success', [process.execPath, '-e', ''], 5000, ${JSON.stringify(directory)});`,
      "const referencedHarnessTimers = process.getActiveResourcesInfo().filter(type => type === 'Timeout').length;",
      'process.stdout.write(JSON.stringify({ rc: result.rc, referencedHarnessTimers }));',
    ].join('\n');
    const started = Date.now();
    const result = spawnSync(process.execPath, ['--input-type=module', '-e', program], { encoding: 'utf8', timeout: 1200 });
    const durationMs = Date.now() - started;
    assert.equal(result.error?.code, undefined, `fast-success subprocess did not exit promptly: ${result.error?.code}`);
    assert.equal(result.status, 0, result.stderr);
    assert.ok(durationMs < 1200, `fast-success subprocess exit exceeded deadline: ${durationMs}ms`);
    assert.deepEqual(JSON.parse(result.stdout), { rc: 0, referencedHarnessTimers: 0 });
  } finally {
    rmSync(temporaryPath, { force: true });
    rmSync(directory, { recursive: true, force: true });
  }
});

test('V3-07 bounded command escalates TERM to KILL for its owned group and leaves no descendant', async () => {
  const directory = resolve(ROOT, '.artifacts/runtime/i5-02/focused-process-group');
  const pidPath = resolve(directory, 'fixture-pids.json');
  rmSync(directory, { recursive: true, force: true });
  mkdirSync(directory, { recursive: true });
  const fixture = [
    "const { spawn } = require('node:child_process');",
    "const { writeFileSync } = require('node:fs');",
    "const descendant = spawn(process.execPath, ['-e', `process.on('SIGTERM',()=>{});setInterval(()=>{},1000)`], { stdio: 'ignore' });",
    `writeFileSync(${JSON.stringify(pidPath)}, JSON.stringify({ leader: process.pid, descendant: descendant.pid }));`,
    "process.on('SIGTERM', () => {});",
    'setTimeout(() => process.exit(93), 1200);',
  ].join('');
  let temporaryPath;
  let pids = {};
  try {
    const loaded = await loadInstrumentedRunner();
    temporaryPath = loaded.temporaryPath;
    const started = Date.now();
    const result = await loaded.module.runBounded('term-kill-fixture', [process.execPath, '-e', fixture], 120, directory);
    const durationMs = Date.now() - started;
    pids = JSON.parse(readFileSync(pidPath, 'utf8'));
    assert.equal(result.timedOut, true, 'fixture must reach the command timeout');
    assert.equal(result.termination?.termSent, true, 'owned group must receive SIGTERM');
    assert.equal(result.termination?.killSent, true, 'TERM-resistant owned group must receive SIGKILL');
    assert.ok(durationMs < 900, `final wait must be bounded; observed ${durationMs}ms`);
    await wait(50);
    assert.equal(processExists(pids.leader), false, 'owned group leader survived cleanup');
    assert.equal(processExists(pids.descendant), false, 'owned group descendant survived cleanup');
  } finally {
    killPid(pids.descendant);
    killPid(pids.leader);
    if (temporaryPath) rmSync(temporaryPath, { force: true });
    rmSync(directory, { recursive: true, force: true });
  }
});

test('V3-07 host READY timeout rejects boundedly and cleans its owned process group', async () => {
  const directory = resolve(ROOT, '.artifacts/runtime/i5-02/focused-host-ready');
  const fixturePath = resolve(directory, 'never-ready.mjs');
  const pidPath = resolve(directory, 'host-pid');
  rmSync(directory, { recursive: true, force: true });
  mkdirSync(directory, { recursive: true });
  writeFileSync(fixturePath, `import { writeFileSync } from 'node:fs';\nwriteFileSync(${JSON.stringify(pidPath)}, String(process.pid));\nprocess.on('SIGTERM', () => {});\nsetTimeout(() => process.exit(94), 1200);\n`);
  let temporaryPath;
  let pid;
  try {
    const loaded = await loadInstrumentedRunner(source => source
      .replace("const hostPath = resolve(ROOT, 'spikes/web/harness/scripts/candidate-static-host.mjs');", `const hostPath = ${JSON.stringify(fixturePath)};`)
      .replace('contract.ceilingsMs.hostReady);', '200);'));
    temporaryPath = loaded.temporaryPath;
    const started = Date.now();
    await assert.rejects(loaded.module.startHost('focused-never-ready', directory), /V3 host READY timeout/);
    const durationMs = Date.now() - started;
    pid = Number(readFileSync(pidPath, 'utf8'));
    assert.ok(durationMs < 900, `READY rejection plus cleanup must be bounded; observed ${durationMs}ms`);
    await wait(50);
    assert.equal(processExists(pid), false, 'READY-timeout host survived owned-group cleanup');
  } finally {
    killPid(pid);
    if (temporaryPath) rmSync(temporaryPath, { force: true });
    rmSync(directory, { recursive: true, force: true });
  }
});

test('V3-07 authority requires exact fresh-live head for feature branch and detached modes', () => {
  const temporaryRoot = mkdtempSync(resolve(tmpdir(), 'vite-v3-authority-'));
  const clone = resolve(temporaryRoot, 'review');
  const remote = resolve(temporaryRoot, 'remote.git');
  const run = args => spawnSync('git', args, { cwd: clone, encoding: 'utf8' });
  const preflight = () => {
    const result = spawnSync(process.execPath, ['spikes/web/harness/scripts/simple-vite-v3.mjs', 'preflight', '--implementation-input', contract.implementationInputSha], { cwd: clone, encoding: 'utf8' });
    return { rc: result.status, output: result.stdout ? JSON.parse(result.stdout) : null, stderr: result.stderr };
  };
  try {
    const cloned = spawnSync('git', ['clone', '--quiet', '--no-hardlinks', ROOT, clone], { encoding: 'utf8' });
    assert.equal(cloned.status, 0, cloned.stderr);
    assert.equal(run(['checkout', '--quiet', '-B', contract.branch, `origin/${contract.branch}`]).status, 0);
    const exactFeature = preflight();
    assert.equal(exactFeature.rc, 0, exactFeature.stderr || JSON.stringify(exactFeature.output));
    assert.equal(exactFeature.output.authorityMode, 'feature-branch');
    assert.equal(exactFeature.output.head, exactFeature.output.freshLiveHead);

    const remoteClone = spawnSync('git', ['clone', '--quiet', '--bare', '--no-hardlinks', ROOT, remote], { encoding: 'utf8' });
    assert.equal(remoteClone.status, 0, remoteClone.stderr);
    const staleHead = run(['rev-parse', 'HEAD^']).stdout.trim();
    const staleRef = spawnSync('git', [`--git-dir=${remote}`, 'update-ref', `refs/heads/${contract.branch}`, staleHead], { encoding: 'utf8' });
    assert.equal(staleRef.status, 0, staleRef.stderr);
    assert.equal(run(['remote', 'set-url', 'origin', remote]).status, 0);
    const divergentFeature = preflight();
    assert.notEqual(divergentFeature.rc, 0);
    assert.ok(divergentFeature.output.failures.includes('feature-head-mismatch'));

    assert.equal(run(['remote', 'set-url', 'origin', ROOT]).status, 0);
    assert.equal(run(['checkout', '--quiet', '--detach', `origin/${contract.branch}`]).status, 0);
    const exact = preflight();
    assert.equal(exact.rc, 0, exact.stderr || JSON.stringify(exact.output));
    assert.equal(exact.output.authorityMode, 'detached-exact-live');

    assert.equal(run(['checkout', '--quiet', '-b', 'review-detached-mismatch']).status, 0);
    assert.equal(run(['-c', 'user.name=Review Fixture', '-c', 'user.email=review-fixture@example.invalid', 'commit', '--quiet', '--allow-empty', '-m', 'test fixture: detached mismatch']).status, 0);
    assert.equal(run(['checkout', '--quiet', '--detach', 'HEAD']).status, 0);
    const mismatch = preflight();
    assert.notEqual(mismatch.rc, 0);
    assert.ok(mismatch.output.failures.includes('detached-head-mismatch'));

    assert.equal(run(['checkout', '--quiet', '-b', 'review-other-branch', `origin/${contract.branch}`]).status, 0);
    const otherBranch = preflight();
    assert.notEqual(otherBranch.rc, 0);
    assert.ok(otherBranch.output.failures.includes('branch-mismatch'));

    assert.equal(run(['checkout', '--quiet', contract.branch]).status, 0);
    writeFileSync(resolve(clone, 'spikes/web/candidates/vite/src/main.jsx'), `${readFileSync(resolve(clone, 'spikes/web/candidates/vite/src/main.jsx'), 'utf8')}\n`);
    const dirty = preflight();
    assert.notEqual(dirty.rc, 0);
    assert.ok(dirty.output.failures.includes('dirty-tracked-state'));
    assert.equal(run(['restore', 'spikes/web/candidates/vite/src/main.jsx']).status, 0);

    const retainedSentinel = resolve(clone, 'spikes/web/evidence/retained/simple-vite-v3/reviewer-untracked-authority-probe.txt');
    const otherSentinel = resolve(clone, 'reviewer-untracked-authority-probe.txt');
    writeFileSync(retainedSentinel, 'reviewer-owned retained-prefix sentinel\n', { flag: 'wx' });
    const retainedDirty = preflight();
    const retainedPreserved = existsSync(retainedSentinel);
    rmSync(retainedSentinel, { force: true });
    writeFileSync(otherSentinel, 'reviewer-owned other sentinel\n', { flag: 'wx' });
    const otherDirty = preflight();
    const otherPreserved = existsSync(otherSentinel);
    rmSync(otherSentinel, { force: true });
    assert.notEqual(retainedDirty.rc, 0);
    assert.ok(retainedDirty.output.failures.includes('dirty-untracked-state'));
    assert.equal(retainedPreserved, true, 'preflight must not delete the retained-prefix sentinel');
    assert.notEqual(otherDirty.rc, 0);
    assert.ok(otherDirty.output.failures.includes('dirty-untracked-state'));
    assert.equal(otherPreserved, true, 'preflight must not delete the other sentinel');

    assert.equal(run(['remote', 'set-url', 'origin', resolve(temporaryRoot, 'missing-origin')]).status, 0);
    const unavailable = preflight();
    assert.notEqual(unavailable.rc, 0);
    assert.ok(unavailable.output.failures.includes('authority-lookup-error'));
  } finally {
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
});

test('V3-07 authority lookup timeout is bounded and fails closed deterministically', async () => {
  const temporaryRoot = mkdtempSync(resolve(tmpdir(), 'vite-v3-authority-timeout-'));
  const clone = resolve(temporaryRoot, 'review');
  const fakeBin = resolve(temporaryRoot, 'bin');
  const fakeGit = resolve(fakeBin, 'git');
  const hungLookup = resolve(temporaryRoot, 'hung-lookup.mjs');
  const realGit = spawnSync('which', ['git'], { encoding: 'utf8' }).stdout.trim();
  let temporaryPath;
  try {
    writeFileSync(hungLookup, 'while (true) {}\n');
    const loaded = await loadInstrumentedRunner(source => source
      .replace("spawnSync('git', ['ls-remote', '--exit-code', 'origin', `refs/heads/${contract.branch}`]", `spawnSync(process.execPath, [${JSON.stringify(hungLookup)}]`)
      .replace("['git', 'ls-remote', '--exit-code', 'origin', `refs/heads/${contract.branch}`]", `[process.execPath, ${JSON.stringify(hungLookup)}]`)
      .replace('timeout: contract.authorityLookupMs,', 'timeout: 100,')
      .replace('contract.authorityLookupMs);', '100);'));
    temporaryPath = loaded.temporaryPath;
    const started = Date.now();
    const timedOut = await loaded.module.preflight(contract.implementationInputSha);
    const durationMs = Date.now() - started;
    assert.ok(durationMs < 1500, `authority timeout result exceeded deterministic bound: ${durationMs}ms`);
    assert.equal(timedOut.result, 'fail');
    assert.ok(timedOut.failures.includes('authority-lookup-timeout'));

    const cloned = spawnSync(realGit, ['clone', '--quiet', '--no-hardlinks', ROOT, clone], { encoding: 'utf8' });
    assert.equal(cloned.status, 0, cloned.stderr);
    mkdirSync(fakeBin);
    writeFileSync(fakeGit, `#!/bin/sh\nif [ "$1" = "ls-remote" ]; then\n  case "$FAKE_GIT_LS_REMOTE_MODE" in\n    error) exit 42 ;;\n    malformed) printf 'not-a-sha\\trefs/heads/feature/issue-5-02-web-spike\\n'; exit 0 ;;\n  esac\nfi\nexec ${JSON.stringify(realGit)} "$@"\n`);
    chmodSync(fakeGit, 0o700);
    for (const [mode, failure] of [['error', 'authority-lookup-error'], ['malformed', 'fresh-live-ambiguous-or-invalid']]) {
      const failed = spawnSync(process.execPath, ['spikes/web/harness/scripts/simple-vite-v3.mjs', 'preflight', '--implementation-input', contract.implementationInputSha], {
        cwd: clone,
        encoding: 'utf8',
        env: { ...process.env, PATH: `${fakeBin}:${process.env.PATH}`, FAKE_GIT_LS_REMOTE_MODE: mode },
      });
      assert.notEqual(failed.status, 0);
      assert.ok(JSON.parse(failed.stdout).failures.includes(failure), `${mode} lookup must report ${failure}`);
    }
  } finally {
    if (temporaryPath) rmSync(temporaryPath, { force: true });
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
});

test('V3-07 authority timeout cleans its transport descendant without signaling current or foreign groups', async () => {
  const temporaryRoot = mkdtempSync(resolve(tmpdir(), 'vite-v3-authority-transport-'));
  const pidPath = resolve(temporaryRoot, 'transport-pids.json');
  const transport = resolve(temporaryRoot, 'transport.mjs');
  const fixture = [
    "import { spawn } from 'node:child_process';",
    "import { writeFileSync } from 'node:fs';",
    "const descendant = spawn(process.execPath, ['-e', `process.on('SIGTERM',()=>{});setInterval(()=>{},1000)`], { stdio: 'ignore' });",
    `writeFileSync(${JSON.stringify(pidPath)}, JSON.stringify({ leader: process.pid, descendant: descendant.pid }));`,
    "process.on('SIGTERM', () => {});",
    'setInterval(() => {}, 1000);',
  ].join('');
  writeFileSync(transport, fixture);
  const foreign = spawn(process.execPath, ['-e', 'setInterval(() => {}, 1000)'], { detached: true, stdio: 'ignore' });
  foreign.unref();
  const currentGroup = processGroup(process.pid);
  const signals = [];
  const realKill = process.kill;
  let temporaryPath;
  let pids = {};
  try {
    const loaded = await loadInstrumentedRunner(source => source
      .replace("spawnSync('git', ['ls-remote', '--exit-code', 'origin', `refs/heads/${contract.branch}`]", `spawnSync(process.execPath, [${JSON.stringify(transport)}]`)
      .replace("['git', 'ls-remote', '--exit-code', 'origin', `refs/heads/${contract.branch}`]", `[process.execPath, ${JSON.stringify(transport)}]`)
      .replace('timeout: contract.authorityLookupMs,', 'timeout: 100,')
      .replace('contract.authorityLookupMs);', '100);'));
    temporaryPath = loaded.temporaryPath;
    process.kill = (pid, signal) => {
      if (signal && signal !== 0) signals.push({ pid, signal });
      return realKill(pid, signal);
    };
    const started = Date.now();
    const timedOut = await loaded.module.preflight(contract.implementationInputSha);
    const durationMs = Date.now() - started;
    process.kill = realKill;
    pids = JSON.parse(readFileSync(pidPath, 'utf8'));
    assert.ok(durationMs < 1200, `authority timeout and final cleanup exceeded deterministic bound: ${durationMs}ms`);
    assert.equal(timedOut.result, 'fail');
    assert.ok(timedOut.failures.includes('authority-lookup-timeout'));
    await wait(50);
    assert.equal(processExists(pids.leader), false, 'authority lookup leader survived cleanup');
    assert.equal(processExists(pids.descendant), false, 'authority transport descendant survived cleanup');
    assert.equal(processExists(foreign.pid), true, 'foreign process group was signaled');
    assert.deepEqual(signals.map(({ pid }) => pid), [-pids.leader, -pids.leader], 'only the verified authority group may be signaled');
    assert.deepEqual(signals.map(({ signal }) => signal), ['SIGTERM', 'SIGKILL'], 'authority cleanup must escalate TERM to KILL');
    assert.equal(signals.some(({ pid }) => pid === -currentGroup), false, 'current process group was signaled');
    assert.equal(signals.some(({ pid }) => pid === -foreign.pid), false, 'foreign process group was signaled');
    assert.equal(process.getActiveResourcesInfo().filter(type => type === 'Timeout').length, 0, 'authority lookup left a referenced timeout handle');
  } finally {
    process.kill = realKill;
    killPid(pids.descendant);
    killPid(pids.leader);
    try { realKill(-foreign.pid, 'SIGKILL'); } catch (error) { if (error.code !== 'ESRCH') throw error; }
    if (temporaryPath) rmSync(temporaryPath, { force: true });
    rmSync(temporaryRoot, { recursive: true, force: true });
  }
});
