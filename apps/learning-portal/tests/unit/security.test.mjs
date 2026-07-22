import test from "node:test";
import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import fsp from "node:fs/promises";
import net from "node:net";
import os from "node:os";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { prepareEvidenceRoot, writeOwnedEvidence, finalizeEvidence } from "../../scripts/write-review-artifacts.mjs";

const appRoot = path.resolve(import.meta.dirname, "../..");
const repo = path.resolve(appRoot, "../..");
const lifecycle = path.join(appRoot, "scripts/portal-lifecycle.mjs");
const serverScript = path.join(appRoot, "scripts/serve-built-portal.mjs");
const verifier = path.join(appRoot, "scripts/verify-stage-a-release.mjs");
const runtime = path.join(repo, ".artifacts/runtime/i5-05-stage-a");
const statePath = path.join(runtime, "portal.json");
const securityHeaders = ["content-security-policy", "referrer-policy", "x-content-type-options", "cross-origin-opener-policy", "permissions-policy", "cache-control"];

const run = (command, args, options = {}) => spawnSync(command, args, { cwd: options.cwd ?? repo, encoding: "utf8", timeout: options.timeout ?? 30_000, env: options.env ?? process.env, input: options.input });
const sleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));
const processStart = (pid) => run("ps", ["-o", "lstart=", "-p", String(pid)]).stdout.trim();

async function startServer(options = {}) {
  const child = spawn(process.execPath, [serverScript], { cwd: appRoot, stdio: ["ignore", "pipe", "pipe"], env: options.env ?? process.env });
  const url = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("SERVER_READINESS_TIMEOUT")), 10_000);
    child.stdout.on("data", (chunk) => { const match = chunk.toString().match(/PORTAL_URL=(http:\/\/127\.0\.0\.1:\d+)/); if (match) { clearTimeout(timer); resolve(match[1]); } });
    child.once("exit", (code) => { clearTimeout(timer); reject(new Error(`SERVER_EXITED:${code}`)); });
  });
  return { child, url };
}

async function stopDirectChild(child) {
  if (child?.exitCode !== null) return;
  child.kill("SIGTERM");
  await Promise.race([new Promise((resolve) => child.once("exit", resolve)), sleep(5_000)]);
  if (child.exitCode === null) child.kill("SIGKILL");
}

async function rawRequest(url, request) {
  const { port } = new URL(url);
  return await new Promise((resolve, reject) => {
    const chunks = [];
    const socket = net.createConnection({ host: "127.0.0.1", port: Number(port) }, () => socket.write(request));
    socket.setTimeout(5_000, () => socket.destroy(new Error("RAW_REQUEST_TIMEOUT")));
    socket.on("data", (chunk) => chunks.push(chunk));
    socket.on("end", () => resolve(Buffer.concat(chunks).toString("latin1")));
    socket.on("error", reject);
  });
}

test.before(() => {
  const built = run("npm", ["run", "build"], { cwd: appRoot, timeout: 180_000 });
  assert.equal(built.status, 0, `SECURITY_BUILD_SETUP_FAILED\n${built.stdout}\n${built.stderr}`);
});

test("PTP-S3 source exposes no runner, storage, cloud, or mutable-state signal path", () => {
  const sourceFiles = fs.readdirSync(path.join(appRoot, "src"), { recursive: true }).filter((name) => /\.(mjs|jsx|css)$/.test(name));
  const authored = sourceFiles.map((name) => fs.readFileSync(path.join(appRoot, "src", name), "utf8")).join("\n");
  assert.doesNotMatch(authored, /dangerouslySetInnerHTML|localStorage|sessionStorage|indexedDB|serviceWorker|child_process|exec\(|spawn\(|Issue\s*#?9/i);
  assert.doesNotMatch(authored, /https?:\/\//);
  const lifecycleSource = fs.readFileSync(lifecycle, "utf8");
  assert.doesNotMatch(lifecycleSource, /process\.kill|spawnSync\(["'](?:kill|pkill)["']|\bpkill\b/, "mutable lifecycle state can still reach an OS signal primitive");
});

test("PTP-S3 lifecycle state replacement never terminates a foreign process", async () => {
  assert.equal(fs.existsSync(runtime), false, "lifecycle test requires an empty exact runtime root");
  const started = run(process.execPath, [lifecycle, "start"], { timeout: 30_000 });
  assert.equal(started.status, 0, `lifecycle start failed: ${started.stderr}`);
  const original = await fsp.readFile(statePath, "utf8");
  const originalValue = JSON.parse(original);
  const sentinel = spawn(process.execPath, ["-e", "setInterval(() => {}, 1000)"], { stdio: "ignore" });
  try {
    const forged = { ...originalValue, pid: sentinel.pid, processStart: processStart(sentinel.pid), challenge: "00".repeat(32), log: { ...(originalValue.log ?? {}), ino: -1 } };
    await fsp.writeFile(statePath, JSON.stringify(forged));
    const stopped = run(process.execPath, [lifecycle, "down"], { timeout: 10_000 });
    await sleep(100);
    assert.notEqual(stopped.status, 0, "replaced lifecycle state was accepted");
    assert.equal(sentinel.exitCode, null, "foreign sentinel exited from mutable lifecycle state");
    assert.equal(sentinel.signalCode, null, "foreign sentinel was terminated from mutable lifecycle state");
  } finally {
    await fsp.writeFile(statePath, original);
    const cleaned = run(process.execPath, [lifecycle, "down"], { timeout: 10_000 });
    assert.equal(cleaned.status, 0, `owned lifecycle cleanup failed: ${cleaned.stderr}`);
    await stopDirectChild(sentinel);
  }
});

test("PTP-S3 lifecycle rejects stale challenge, alias, type, mode, and foreign socket state", async () => {
  const source = fs.readFileSync(lifecycle, "utf8");
  for (const behavior of ["CONTROL_CHALLENGE_STALE", "CONTROL_SOCKET_FOREIGN", "LIFECYCLE_ROOT_ALIAS", "LIFECYCLE_ROOT_MODE", "LIFECYCLE_STATE_INODE"]) {
    assert.match(source, new RegExp(behavior), `missing named fail-closed lifecycle behavior ${behavior}`);
  }
});

test("PTP-S3 stale challenge and socket mode fail closed while the authenticated child stays live", async () => {
  assert.equal(fs.existsSync(runtime), false);
  assert.equal(run(process.execPath, [lifecycle, "start"], { timeout: 30_000 }).status, 0);
  const original = await fsp.readFile(statePath, "utf8"); const state = JSON.parse(original); const controlPath = path.join("/private/tmp", `i5-05-portal-${state.runId}`, "control.sock");
  try {
    await fsp.writeFile(statePath, JSON.stringify({ ...state, challenge: "00".repeat(32) }));
    const stale = run(process.execPath, [lifecycle, "down"], { timeout: 10_000 });
    assert.notEqual(stale.status, 0); assert.match(stale.stderr, /CONTROL_CHALLENGE_STALE/);
    assert.equal((await fetch(state.url)).status, 200, "stale challenge stopped the authenticated child");
    await fsp.writeFile(statePath, original); await fsp.chmod(controlPath, 0o777);
    const mode = run(process.execPath, [lifecycle, "status"], { timeout: 10_000 });
    assert.notEqual(mode.status, 0); assert.match(mode.stderr, /CONTROL_SOCKET_FOREIGN/);
  } finally {
    await fsp.chmod(controlPath, 0o700); await fsp.writeFile(statePath, original);
    assert.equal(run(process.execPath, [lifecycle, "down"], { timeout: 10_000 }).status, 0);
  }
});

test("PTP-S3 foreign socket, state alias, and runtime mode never gain lifecycle authority", async () => {
  assert.equal(fs.existsSync(runtime), false);
  assert.equal(run(process.execPath, [lifecycle, "start"], { timeout: 30_000 }).status, 0);
  const original = await fsp.readFile(statePath, "utf8"); const state = JSON.parse(original); const controlDirectory = path.join("/private/tmp", `i5-05-portal-${state.runId}`); const controlPath = path.join(controlDirectory, "control.sock"); const ownedPath = path.join(controlDirectory, "owned.sock");
  let foreign;
  try {
    await fsp.rename(controlPath, ownedPath);
    foreign = net.createServer((socket) => { socket.on("error", () => {}); socket.resume(); });
    await new Promise((resolve, reject) => { foreign.once("error", reject); foreign.listen(controlPath, resolve); }); await fsp.chmod(controlPath, 0o700);
    const foreignStat = await fsp.lstat(controlPath); await fsp.writeFile(statePath, JSON.stringify({ ...state, control: { dev: foreignStat.dev, ino: foreignStat.ino } }));
    const rejected = run(process.execPath, [lifecycle, "down"], { timeout: 10_000 }); assert.notEqual(rejected.status, 0); assert.match(rejected.stderr, /CONTROL_PROTOCOL_INVALID|CONTROL_TIMEOUT/);
    assert.equal((await fetch(state.url)).status, 200, "foreign control socket stopped the authenticated child");
    await new Promise((resolve) => foreign.close(resolve)); foreign = null; await fsp.rm(controlPath, { force: true }); await fsp.rename(ownedPath, controlPath); await fsp.writeFile(statePath, original);
    await fsp.chmod(runtime, 0o755); const mode = run(process.execPath, [lifecycle, "status"]); assert.notEqual(mode.status, 0); assert.match(mode.stderr, /LIFECYCLE_ROOT_MODE/); await fsp.chmod(runtime, 0o700);
    const saved = `${statePath}.owned`; await fsp.rename(statePath, saved); await fsp.symlink(path.basename(saved), statePath); const alias = run(process.execPath, [lifecycle, "status"]); assert.notEqual(alias.status, 0); assert.match(alias.stderr, /STATE_FILE_UNSAFE/); await fsp.rm(statePath); await fsp.rename(saved, statePath);
  } finally {
    if (foreign) await new Promise((resolve) => foreign.close(resolve));
    await fsp.chmod(runtime, 0o700).catch(() => {}); if (fs.existsSync(ownedPath)) { await fsp.rm(controlPath, { force: true }); await fsp.rename(ownedPath, controlPath); } await fsp.writeFile(statePath, original);
    assert.equal(run(process.execPath, [lifecycle, "down"], { timeout: 10_000 }).status, 0);
  }
});

test("PTP-S3 protocol-aware socket replacement cannot impersonate the spawned child", async () => {
  assert.equal(fs.existsSync(runtime), false);
  assert.equal(run(process.execPath, [lifecycle, "start"], { timeout: 30_000 }).status, 0);
  const original = await fsp.readFile(statePath, "utf8"); const state = JSON.parse(original); const controlDirectory = path.join("/private/tmp", `i5-05-portal-${state.runId}`); const controlPath = path.join(controlDirectory, "control.sock"); const ownedPath = path.join(controlDirectory, "owned.sock");
  let impostor;
  try {
    await fsp.rename(controlPath, ownedPath);
    impostor = net.createServer((socket) => { let raw = ""; socket.setEncoding("utf8"); socket.on("data", (chunk) => { raw += chunk; }); socket.on("end", () => { const request = JSON.parse(raw); socket.end(JSON.stringify({ ok: true, status: "running", url: state.url, requestNonce: request.requestNonce }) + "\n"); }); });
    await new Promise((resolve, reject) => { impostor.once("error", reject); impostor.listen(controlPath, resolve); }); await fsp.chmod(controlPath, 0o700);
    const foreignStat = await fsp.lstat(controlPath); await fsp.writeFile(statePath, JSON.stringify({ ...state, control: { dev: foreignStat.dev, ino: foreignStat.ino } }));
    const rejected = run(process.execPath, [lifecycle, "status"], { timeout: 10_000 });
    assert.notEqual(rejected.status, 0, "protocol-aware impostor authenticated through mutable portal.json");
    assert.match(rejected.stderr, /CHILD_AUTHENTICATION_FAILED/);
    assert.equal((await fetch(state.url)).status, 200, "protocol-aware impostor stopped the real child");
  } finally {
    if (impostor) await new Promise((resolve) => impostor.close(resolve));
    await fsp.rm(controlPath, { force: true }); await fsp.rename(ownedPath, controlPath); await fsp.writeFile(statePath, original);
    assert.equal(run(process.execPath, [lifecycle, "down"], { timeout: 10_000 }).status, 0);
  }
});

test("PTP-S3 authenticated shutdown is self-directed and removes only owned control state", async () => {
  assert.equal(run(process.execPath, [lifecycle, "start"], { timeout: 30_000 }).status, 0);
  const state = JSON.parse(await fsp.readFile(statePath, "utf8")); const controlDirectory = path.join("/private/tmp", `i5-05-portal-${state.runId}`);
  const stopped = run(process.execPath, [lifecycle, "down"], { timeout: 10_000 });
  assert.equal(stopped.status, 0, stopped.stderr); assert.match(stopped.stdout, /portal=stopped review-evidence=preserved/); assert.equal(fs.existsSync(runtime), false); assert.equal(fs.existsSync(controlDirectory), false);
});

test("PTP-S3 server admits a closed manifest and rejects post-admission files and aliases", async () => {
  const inventoryPath = path.join(appRoot, "dist/.portal-build-inventory.json");
  assert.equal(fs.existsSync(inventoryPath), true, "closed build inventory was not emitted");
  const { child, url } = await startServer();
  const added = path.join(appRoot, "dist/added-after-admission.txt");
  const alias = path.join(appRoot, "dist/alias-after-admission.txt");
  try {
    await fsp.writeFile(added, "foreign");
    await fsp.symlink("index.html", alias);
    for (const locator of ["/added-after-admission.txt", "/alias-after-admission.txt", "/.vite/manifest.json"]) {
      const response = await fetch(`${url}${locator}`);
      assert.equal(response.status, 404, `unindexed build locator was served: ${locator}`);
    }
  } finally {
    await fsp.rm(added, { force: true });
    await fsp.rm(alias, { force: true });
    await stopDirectChild(child);
  }
});

test("PTP-S3 server rejects transfer encoding, bodies, ambiguous paths, and unsupported methods before file access", async () => {
  const { child, url } = await startServer();
  const host = new URL(url).host;
  try {
    const cases = [
      ["transfer-encoding", `GET / HTTP/1.1\r\nHost: ${host}\r\nTransfer-Encoding: chunked\r\nConnection: close\r\n\r\n1\r\nx\r\n0\r\n\r\n`],
      ["nonzero-content-length", `GET / HTTP/1.1\r\nHost: ${host}\r\nContent-Length: 1\r\nConnection: close\r\n\r\nx`],
      ["unsupported-method", `POST / HTTP/1.1\r\nHost: ${host}\r\nContent-Length: 0\r\nConnection: close\r\n\r\n`],
      ["encoded-path", `GET /%2e%2e/secret HTTP/1.1\r\nHost: ${host}\r\nConnection: close\r\n\r\n`],
    ];
    for (const [name, raw] of cases) {
      const response = await rawRequest(url, raw);
      assert.doesNotMatch(response, /^HTTP\/1\.1 200/m, `${name} reached an admitted file`);
      for (const header of securityHeaders) assert.match(response.toLowerCase(), new RegExp(`^${header}:`, "m"), `${name} rejection lacks ${header}`);
    }
    const unknown = await fetch(`${url}/unknown-unindexed`);
    assert.equal(unknown.status, 404, "unknown route did not fail closed");
  } finally { await stopDirectChild(child); }
});

test("PTP-S3 admitted GET and HEAD responses are exact and deterministic", async () => {
  const { child, url } = await startServer();
  try {
    const get = await fetch(url);
    const head = await fetch(url, { method: "HEAD" });
    assert.equal(get.status, 200);
    assert.equal(head.status, 200);
    assert.equal(await head.text(), "");
    assert.equal(get.headers.get("content-length"), head.headers.get("content-length"));
    for (const header of securityHeaders) assert.equal(get.headers.get(header), head.headers.get(header), `GET/HEAD header drift: ${header}`);
  } finally { await stopDirectChild(child); }
});

test("PTP-S3 admitted bytes survive pathname inode replacement and a fresh server rejects drift", async () => {
  const indexPath = path.join(appRoot, "dist/index.html"); const original = await fsp.readFile(indexPath); const { child, url } = await startServer();
  try {
    await fsp.writeFile(indexPath, "BUILD_REOPEN_CANARY");
    const response = await fetch(url); assert.equal(response.status, 200); assert.doesNotMatch(await response.text(), /BUILD_REOPEN_CANARY/, "server reopened a replaced admitted pathname");
  } finally { await fsp.writeFile(indexPath, original); await stopDirectChild(child); }
  await fsp.writeFile(indexPath, "BUILD_HASH_DRIFT");
  try { await assert.rejects(startServer(), /SERVER_EXITED:1|SERVER_READINESS_TIMEOUT/, "fresh server admitted build hash drift"); } finally { await fsp.writeFile(indexPath, original); }
});

test("PTP-S3 public verifier rejects lock drift and cloud/proxy/runtime injection", async () => {
  const lockPath = path.join(appRoot, "package-lock.json");
  const original = await fsp.readFile(lockPath);
  try {
    await fsp.writeFile(lockPath, Buffer.concat([original, Buffer.from("\n")]));
    const drift = run(process.execPath, [verifier, "--local-only"]);
    assert.notEqual(drift.status, 0, "package-lock byte drift passed the public verifier");
  } finally { await fsp.writeFile(lockPath, original); }
  for (const [name, value] of [["AWS_ACCESS_KEY_ID", "sentinel"], ["HTTPS_PROXY", "http://127.0.0.1:9"], ["NODE_OPTIONS", "--trace-warnings"]]) {
    const injected = run(process.execPath, [verifier, "--local-only"], { env: { ...process.env, [name]: value } });
    assert.notEqual(injected.status, 0, `${name} injection passed the public verifier`);
  }
  const installedPackage = path.join(appRoot, "node_modules/react/package.json"); const installed = await fsp.readFile(installedPackage);
  try { const value = JSON.parse(installed); value.version = "0.0.0-drift"; await fsp.writeFile(installedPackage, JSON.stringify(value)); const graph = run(process.execPath, [verifier, "--local-only"]); assert.notEqual(graph.status, 0, "installed package graph drift passed the public verifier"); } finally { await fsp.writeFile(installedPackage, installed); }
  const packageValue = JSON.parse(await fsp.readFile(path.join(appRoot, "package.json"), "utf8"));
  assert.equal(packageValue.packageManager, "npm@10.9.8", "npm runtime is not frozen");
  assert.deepEqual(packageValue.engines, { node: "22.22.3", npm: "10.9.8" }, "Node/npm runtime admission is not exact");
});

test("PTP-S3 Stage B negatives emit released-schema-valid fitness-result-v2 on stderr", () => {
  const schema = JSON.parse(fs.readFileSync(path.join(repo, "learning/contracts/fitness-result-v2.schema.json"), "utf8"));
  for (const args of [["lesson-e2e", "LESSON=promotion-trust"], ["local-journey-e2e"]]) {
    const result = run("make", args);
    assert.equal(result.status, 2, `${args[0]} must remain blocked with exit 2`);
    assert.equal(result.stdout, "", `${args[0]} wrote blocked evidence to stdout`);
    const value = JSON.parse(result.stderr.trim().split("\n")[0]);
    assert.deepEqual(Object.keys(value).sort(), [...schema.required].sort(), `${args[0]} omitted or invented fitness fields`);
    assert.equal(value.status, "fail");
    assert.equal(value.failureCode, "STAGE_B_DEPENDENCY_UNAVAILABLE");
    const checked = run("python3.12", ["-c", "import json,pathlib,sys; from jsonschema import Draft202012Validator,FormatChecker; schema=json.loads(pathlib.Path('learning/contracts/fitness-result-v2.schema.json').read_text()); Draft202012Validator(schema, format_checker=FormatChecker()).validate(json.loads(sys.stdin.read()))"], { env: process.env, timeout: 30_000, cwd: repo, input: JSON.stringify(value) });
    assert.equal(checked.status, 0, `${args[0]} failed the released fitness validator: ${checked.stderr}`);
    assert.doesNotMatch(JSON.stringify(value), /runnerAction|completion|implemented/);
  }
});

test("PTP-S3 activation marks Stage A implemented and unavailable Stage B honestly", () => {
  const activation = JSON.parse(fs.readFileSync(path.join(appRoot, "command-owner-activation.stage-a.json"), "utf8"));
  const unavailable = activation.commands.filter((row) => ["lesson-e2e", "local-journey-e2e"].includes(row.commandId));
  assert.deepEqual(unavailable.map((row) => row.availability), ["unavailable", "unavailable"]);
  assert.equal(activation.commands.filter((row) => row.availability === "implemented").length, 7);
  const direct = run("make", ["-f", "mk/issue-5/i5-05.mk"]);
  assert.equal(direct.status, 2);
  assert.match(direct.stderr, /I5-05_FRAGMENT_DIRECT_INVOCATION_DENIED/);
});

test("PTP-S3 evidence writer refuses foreign outputs and enforces a closed bounded privacy-scanned inventory", async () => {
  const evidenceRoot = await fsp.mkdtemp(path.join(os.tmpdir(), "portal-evidence-red-"));
  const foreign = path.join(evidenceRoot, "uat-checklist.md");
  await fsp.writeFile(foreign, "foreign");
  try {
    const result = run(process.execPath, [path.join(appRoot, "scripts/write-review-artifacts.mjs")], { env: { ...process.env, PORTAL_EVIDENCE_ROOT: evidenceRoot } });
    assert.notEqual(result.status, 0, "foreign retained output was adopted or overwritten");
    assert.equal(await fsp.readFile(foreign, "utf8"), "foreign");
  } finally {
    await fsp.rm(evidenceRoot, { recursive: true, force: true });
    const legacy = path.join(repo, ".artifacts/evidence/local-journey");
    await fsp.rm(legacy, { recursive: true, force: true });
    for (const directory of [path.join(repo, ".artifacts/evidence"), path.join(repo, ".artifacts")]) { try { await fsp.rmdir(directory); } catch {} }
  }
  const writerSource = fs.readFileSync(path.join(appRoot, "scripts/write-review-artifacts.mjs"), "utf8");
  for (const behavior of ["EVIDENCE_OWNER_MISMATCH", "EVIDENCE_INVENTORY_UNEXPECTED", "EVIDENCE_FILE_LIMIT", "EVIDENCE_AGGREGATE_LIMIT", "EVIDENCE_PRIVACY_REJECTED", "EVIDENCE_ALIAS_FORBIDDEN"]) assert.match(writerSource, new RegExp(behavior));
  assert.doesNotMatch(writerSource, /\.zip/);
});

test("PTP-S3 artifact root, alias, type, residue, size, and privacy bounds are executable", async () => {
  const approvedParent = path.join(repo, ".hermes/issue-10-stage-a-v2/evidence"); await fsp.mkdir(approvedParent, { recursive: true, mode: 0o700 });
  const parent = await fsp.mkdtemp(path.join(approvedParent, "portal-evidence-bounds-")); const root = path.join(parent, "evidence"); await fsp.mkdir(root, { mode: 0o700 });
  try {
    const outside = await fsp.mkdtemp(path.join("/private/tmp", "portal-evidence-outside-"));
    try { await assert.rejects(prepareEvidenceRoot(outside), /EVIDENCE_ROOT_OUTSIDE_APPROVED_NAMESPACE/); } finally { await fsp.rm(outside, { recursive: true, force: true }); }
    await fsp.chmod(root, 0o755); await assert.rejects(prepareEvidenceRoot(root), /EVIDENCE_OWNER_MISMATCH/); await fsp.chmod(root, 0o700);
    const work = await prepareEvidenceRoot(root);
    await assert.rejects(writeOwnedEvidence("unexpected.json", "{}", work), /EVIDENCE_INVENTORY_UNEXPECTED/);
    await assert.rejects(writeOwnedEvidence("axe.json", `{"raw_record":"${"x".repeat(16)}"}`, work), /EVIDENCE_PRIVACY_REJECTED/);
    await assert.rejects(writeOwnedEvidence("axe.json", "x".repeat(2 * 1024 * 1024 + 1), work), /EVIDENCE_FILE_LIMIT/);
    const outsideFile = path.join(parent, "outside"); await fsp.writeFile(outsideFile, "foreign"); await fsp.link(outsideFile, path.join(work, "axe.json"));
    await assert.rejects(writeOwnedEvidence("axe.json", "{}", work)); await fsp.rm(path.join(work, "axe.json"));
    for (const name of ["axe.json", "console-csp.json", "dom-inventory.json", "no-js-inventory.json"]) await writeOwnedEvidence(name, "[]", work);
    for (const name of ["desktop-catalog.png", "desktop-decision.png", "desktop-grains.png", "desktop-unavailable.png", "narrow-catalog.png", "narrow-decision.png", "narrow-grains.png", "narrow-unavailable.png"]) await writeOwnedEvidence(name, Buffer.from([0x89, 0x50, 0x4e, 0x47]), work);
    await finalizeEvidence(work);
    const verified = run(process.execPath, [path.join(appRoot, "scripts/write-review-artifacts.mjs")], { env: { ...process.env, PORTAL_EVIDENCE_ROOT: root } }); assert.equal(verified.status, 0, verified.stderr);
    const retained = await fsp.readFile(path.join(root, "hash-manifest.sha256"));
    const interrupted = await prepareEvidenceRoot(root, { reset: true });
    await writeOwnedEvidence("axe.json", "[]", interrupted);
    await assert.rejects(finalizeEvidence(interrupted), /EVIDENCE_INVENTORY_UNEXPECTED/);
    assert.deepEqual(await fsp.readFile(path.join(root, "hash-manifest.sha256")), retained, "failed replacement destroyed the prior verified evidence bundle");
  } finally { await fsp.rm(parent, { recursive: true, force: true }); }
});

test("PTP-RED-A-016 styles prove visible focus and 360px reflow", () => {
  const css = fs.readFileSync(path.join(appRoot, "src/styles.css"), "utf8");
  assert.match(css, /:focus-visible/);
  assert.match(css, /max-width:\s*100%|overflow-wrap/);
  assert.match(css, /prefers-reduced-motion/);
});
