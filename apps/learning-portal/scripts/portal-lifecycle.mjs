import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import net from "node:net";
import { spawn } from "node:child_process";

process.umask(0o077);
const repo = path.resolve(import.meta.dirname, "../../..");
const artifacts = path.join(repo, ".artifacts");
const runtimeParent = path.join(artifacts, "runtime");
const runtime = path.join(runtimeParent, "i5-05-stage-a");
const statePath = path.join(runtime, "portal.json");
const inventoryPath = path.join(repo, "apps/learning-portal/dist/.portal-build-inventory.json");
const STATE_KEYS = ["buildInventorySha256", "challenge", "control", "controlRoot", "log", "maturity", "run", "runId", "schemaVersion", "url"];
const sha256 = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const sleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

async function privateDirectory(directory, create = false) {
  if (create) await fs.mkdir(directory, { recursive: false, mode: 0o700 }).catch((error) => { if (error.code !== "EEXIST") throw error; });
  const stat = await fs.lstat(directory).catch((error) => { if (error.code === "ENOENT") return null; throw error; });
  if (!stat) return null;
  if (!stat.isDirectory() || stat.isSymbolicLink()) throw new Error("LIFECYCLE_ROOT_ALIAS");
  if (stat.uid !== process.getuid()) throw new Error("LIFECYCLE_ROOT_OWNER");
  if ((stat.mode & 0o777) !== 0o700) throw new Error("LIFECYCLE_ROOT_MODE");
  return stat;
}

async function ensureRuntime() {
  for (const directory of [artifacts, runtimeParent, runtime]) await privateDirectory(directory, true);
}

async function pinnedRegular(file, limit = 1024 * 1024) {
  const before = await fs.lstat(file);
  if (!before.isFile() || before.isSymbolicLink() || before.nlink !== 1 || before.uid !== process.getuid() || (before.mode & 0o777) !== 0o600 || before.size > limit) throw new Error("STATE_FILE_UNSAFE");
  const handle = await fs.open(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  try { const opened = await handle.stat(); if (opened.dev !== before.dev || opened.ino !== before.ino || opened.nlink !== 1) throw new Error("LIFECYCLE_STATE_INODE"); return { bytes: await handle.readFile(), stat: opened }; } finally { await handle.close(); }
}
async function pinnedAuthority(file) {
  const before = await fs.lstat(file);
  if (!before.isFile() || before.isSymbolicLink() || before.nlink !== 1 || before.uid !== process.getuid() || (before.mode & 0o777) !== 0o400 || before.size > 4096) throw new Error("CHILD_AUTHENTICATION_FAILED");
  const handle = await fs.open(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  try { const opened = await handle.stat(); if (opened.dev !== before.dev || opened.ino !== before.ino || opened.nlink !== 1) throw new Error("CHILD_AUTHENTICATION_FAILED"); return { bytes: await handle.readFile(), stat: opened }; } finally { await handle.close(); }
}

function validateIdentity(identity) {
  return identity && Number.isSafeInteger(identity.dev) && Number.isSafeInteger(identity.ino) && identity.dev >= 0 && identity.ino > 0;
}

async function readState() {
  const root = await privateDirectory(runtime, false);
  if (!root) return null;
  let pinned;
  try { pinned = await pinnedRegular(statePath); } catch (error) { if (error.code === "ENOENT") return null; throw error; }
  let value; try { value = JSON.parse(pinned.bytes.toString("utf8")); } catch { throw new Error("STATE_FILE_UNSAFE"); }
  if (!value || Object.keys(value).sort().join(",") !== STATE_KEYS.join(",") || value.schemaVersion !== "portal-lifecycle-state-v3" || value.maturity !== "static-portal-stage-a" || !/^[0-9a-f]{32}$/.test(value.runId) || !/^[0-9a-f]{64}$/.test(value.challenge) || !/^http:\/\/127\.0\.0\.1:\d+$/.test(value.url) || !/^[0-9a-f]{64}$/.test(value.buildInventorySha256) || !validateIdentity(value.control) || !validateIdentity(value.controlRoot) || !validateIdentity(value.log) || !validateIdentity(value.run)) throw new Error("STATE_FILE_UNSAFE");
  const runDirectory = path.join(runtime, `run-${value.runId}`);
  await privateDirectory(runDirectory, false).then((stat) => { if (!stat) throw new Error("LIFECYCLE_STATE_STALE"); if (stat.dev !== value.run.dev || stat.ino !== value.run.ino) throw new Error("LIFECYCLE_STATE_INODE"); });
  const controlDirectory = path.join("/private/tmp", `i5-05-portal-${value.runId}`);
  await privateDirectory(controlDirectory, false).then((stat) => { if (!stat || stat.dev !== value.controlRoot.dev || stat.ino !== value.controlRoot.ino) throw new Error("CONTROL_SOCKET_FOREIGN"); });
  const authorityPath = path.join(runDirectory, "child-authority.json"); const authority = await pinnedAuthority(authorityPath);
  return { value, stat: pinned.stat, runDirectory, controlDirectory, controlPath: path.join(controlDirectory, "control.sock"), authorityPath, authorityStat: authority.stat, logPath: path.join(runDirectory, "portal.log") };
}

async function validateSocket(record) {
  const stat = await fs.lstat(record.controlPath).catch((error) => { if (error.code === "ENOENT") throw new Error("LIFECYCLE_STATE_STALE"); throw error; });
  if (!stat.isSocket() || stat.isSymbolicLink() || stat.uid !== process.getuid() || stat.nlink !== 1 || (stat.mode & 0o777) !== 0o700 || stat.dev !== record.value.control.dev || stat.ino !== record.value.control.ino) throw new Error("CONTROL_SOCKET_FOREIGN");
}

async function control(record, action) {
  await validateSocket(record);
  const authority = await pinnedAuthority(record.authorityPath);
  if (authority.stat.dev !== record.authorityStat.dev || authority.stat.ino !== record.authorityStat.ino) throw new Error("CHILD_AUTHENTICATION_FAILED");
  let authorityValue; try { authorityValue = JSON.parse(authority.bytes.toString("utf8")); } catch { throw new Error("CHILD_AUTHENTICATION_FAILED"); }
  if (!authorityValue || authorityValue.schemaVersion !== "portal-child-authority-v1" || authorityValue.runId !== record.value.runId || typeof authorityValue.publicKey !== "string" || Object.keys(authorityValue).sort().join(",") !== "publicKey,runId,schemaVersion") throw new Error("CHILD_AUTHENTICATION_FAILED");
  let publicKey; try { publicKey = crypto.createPublicKey({ key: Buffer.from(authorityValue.publicKey, "base64"), format: "der", type: "spki" }); if (publicKey.asymmetricKeyType !== "ed25519") throw new Error(); } catch { throw new Error("CHILD_AUTHENTICATION_FAILED"); }
  const requestNonce = crypto.randomBytes(32).toString("hex");
  const request = JSON.stringify({ version: "portal-control-v2", action, runId: record.value.runId, challenge: record.value.challenge, requestNonce });
  const response = await new Promise((resolve, reject) => {
    let raw = ""; const socket = net.createConnection(record.controlPath);
    socket.setEncoding("utf8"); socket.setTimeout(3000, () => socket.destroy(new Error("CONTROL_TIMEOUT")));
    socket.on("connect", () => socket.end(request));
    socket.on("data", (chunk) => { raw += chunk; if (raw.length > 1024) socket.destroy(new Error("CONTROL_PROTOCOL_INVALID")); });
    socket.on("end", () => resolve(raw)); socket.on("error", reject);
  });
  let value; try { value = JSON.parse(response); } catch { throw new Error("CONTROL_PROTOCOL_INVALID"); }
  if (value.ok !== true) throw new Error(value.code === "CONTROL_CHALLENGE_STALE" ? "CONTROL_CHALLENGE_STALE" : "CONTROL_PROTOCOL_INVALID");
  const expectedKeys = action === "status" ? "action,ok,requestNonce,runId,signature,status,url" : "action,ok,requestNonce,runId,signature,status";
  if (Object.keys(value).sort().join(",") !== expectedKeys || value.action !== action || value.runId !== record.value.runId || value.requestNonce !== requestNonce || (action === "status" ? value.status !== "running" || value.url !== record.value.url : value.status !== "shutting-down")) throw new Error("CHILD_AUTHENTICATION_FAILED");
  const signed = { action: value.action, ok: value.ok, requestNonce: value.requestNonce, runId: value.runId, status: value.status, ...(action === "status" ? { url: value.url } : {}) };
  let signature; try { signature = Buffer.from(value.signature, "base64"); } catch { throw new Error("CHILD_AUTHENTICATION_FAILED"); }
  if (!crypto.verify(null, Buffer.from(JSON.stringify(signed)), publicKey, signature)) throw new Error("CHILD_AUTHENTICATION_FAILED");
  return value;
}

async function cleanupDirectChild(child) {
  if (!child || child.exitCode !== null || child.signalCode !== null) return;
  child.kill("SIGTERM");
  await Promise.race([new Promise((resolve) => child.once("exit", resolve)), sleep(2000)]);
  if (child.exitCode === null && child.signalCode === null) child.kill("SIGKILL");
}
async function removeEmptyParents() { for (const directory of [runtime, runtimeParent, artifacts]) await fs.rmdir(directory).catch((error) => { if (!["ENOENT", "ENOTEMPTY"].includes(error.code)) throw error; }); }

async function start() {
  const existing = await readState();
  if (existing) { await control(existing, "status"); console.log(`${existing.value.url}\nrunner=unavailable completion=disabled`); return; }
  await ensureRuntime();
  const runId = crypto.randomBytes(16).toString("hex"); const challenge = crypto.randomBytes(32).toString("hex");
  const runDirectory = path.join(runtime, `run-${runId}`); await fs.mkdir(runDirectory, { mode: 0o700 }); const runStat = await privateDirectory(runDirectory);
  const controlDirectory = path.join("/private/tmp", `i5-05-portal-${runId}`); await fs.mkdir(controlDirectory, { mode: 0o700 }); const controlRootStat = await privateDirectory(controlDirectory);
  const controlPath = path.join(controlDirectory, "control.sock"); const authorityPath = path.join(runDirectory, "child-authority.json"); const logPath = path.join(runDirectory, "portal.log");
  const logHandle = await fs.open(logPath, "wx", 0o600); const logStat = await logHandle.stat();
  const childEnvironment = Object.freeze({ PATH: process.env.PATH ?? "/usr/bin:/bin", LANG: "C.UTF-8", LC_ALL: "C.UTF-8", TZ: "UTC" });
  let child;
  try {
    child = spawn(process.execPath, [path.join(import.meta.dirname, "serve-built-portal.mjs"), "--control-socket", controlPath, "--authority-file", authorityPath, "--challenge", challenge, "--run-id", runId], { cwd: repo, detached: true, stdio: ["ignore", logHandle.fd, logHandle.fd], env: childEnvironment });
  } finally { await logHandle.close(); }
  try {
    let url;
    for (let index = 0; index < 60; index++) { if (child.exitCode !== null || child.signalCode !== null) break; await sleep(250); const log = await fs.readFile(logPath, "utf8"); url = log.match(/PORTAL_URL=(http:\/\/127\.0\.0\.1:\d+)/)?.[1]; if (url) { try { await fs.lstat(controlPath); break; } catch {} } }
    if (!url || child.exitCode !== null || child.signalCode !== null) throw new Error("PORTAL_READINESS_TIMEOUT");
    const socketStat = await fs.lstat(controlPath); if (!socketStat.isSocket() || socketStat.isSymbolicLink() || socketStat.uid !== process.getuid() || socketStat.nlink !== 1 || (socketStat.mode & 0o777) !== 0o700) throw new Error("CONTROL_SOCKET_FOREIGN");
    await pinnedAuthority(authorityPath);
    const inventory = await pinnedRegular(inventoryPath); const value = { schemaVersion: "portal-lifecycle-state-v3", runId, challenge, url, maturity: "static-portal-stage-a", buildInventorySha256: sha256(inventory.bytes), run: { dev: runStat.dev, ino: runStat.ino }, controlRoot: { dev: controlRootStat.dev, ino: controlRootStat.ino }, control: { dev: socketStat.dev, ino: socketStat.ino }, log: { dev: logStat.dev, ino: logStat.ino } };
    const stateHandle = await fs.open(statePath, "wx", 0o600); try { await stateHandle.writeFile(JSON.stringify(value)); } finally { await stateHandle.close(); }
    child.unref(); console.log(`${url}\nrunner=unavailable completion=disabled`);
  } catch (error) { await cleanupDirectChild(child); await fs.rm(controlPath, { force: true }); await fs.rm(authorityPath, { force: true }); await fs.rm(logPath, { force: true }); await fs.rmdir(controlDirectory).catch(() => {}); await fs.rmdir(runDirectory).catch(() => {}); await removeEmptyParents(); throw error; }
}

async function status() {
  const record = await readState();
  if (!record) { console.log("portal=stopped stage-b=blocked-on-issue9"); return; }
  await control(record, "status");
  console.log(`portal=running url=${record.value.url} runner=unavailable completion=disabled stage-b=blocked-on-issue9`);
}

async function down() {
  const record = await readState();
  if (!record) { await removeEmptyParents(); console.log("portal=stopped review-evidence=preserved"); return; }
  await control(record, "shutdown");
  for (let index = 0; index < 50; index++) { try { await fs.lstat(record.controlPath); await sleep(100); } catch (error) { if (error.code === "ENOENT") break; throw error; } }
  try { await fs.lstat(record.controlPath); throw new Error("CONTROL_SHUTDOWN_TIMEOUT"); } catch (error) { if (error.code !== "ENOENT") throw error; }
  const state = await fs.lstat(statePath); if (state.dev !== record.stat.dev || state.ino !== record.stat.ino || state.nlink !== 1) throw new Error("LIFECYCLE_STATE_INODE");
  const log = await fs.lstat(record.logPath); if (!log.isFile() || log.isSymbolicLink() || log.uid !== process.getuid() || log.nlink !== 1 || log.dev !== record.value.log.dev || log.ino !== record.value.log.ino) throw new Error("LOG_IDENTITY_MISMATCH");
  const authority = await pinnedAuthority(record.authorityPath); if (authority.stat.dev !== record.authorityStat.dev || authority.stat.ino !== record.authorityStat.ino) throw new Error("CHILD_AUTHENTICATION_FAILED");
  await fs.rm(record.logPath); await fs.rm(record.authorityPath); await fs.rm(statePath); await fs.rmdir(record.controlDirectory); await fs.rmdir(record.runDirectory); await removeEmptyParents();
  console.log("portal=stopped review-evidence=preserved");
}

const action = process.argv[2];
if (action === "start") await start(); else if (action === "status") await status(); else if (action === "down") await down(); else throw new Error("LIFECYCLE_ACTION_FORBIDDEN");
