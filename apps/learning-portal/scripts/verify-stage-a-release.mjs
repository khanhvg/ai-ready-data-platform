import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";
import { loadReleasedLearning } from "../src/contracts/released-learning-adapter.mjs";

process.umask(0o077);
const repo = path.resolve(import.meta.dirname, "../../..");
const appRoot = path.resolve(import.meta.dirname, "..");
const EXPECTED_LOCK_SHA256 = "8ebb04ffd5504a17f0b144d421f478d8f1332e35075a46d9c5e95036d2ba2629";
const forbiddenEnvironment = /^(?:AWS_|AZURE_|GOOGLE_|GCP_|CLOUD_|HTTP_PROXY$|HTTPS_PROXY$|ALL_PROXY$|NO_PROXY$|NODE_OPTIONS$|NODE_PATH$|VITE_|NPM_CONFIG_(?:PROXY|HTTPS_PROXY)$|DOCKER_|ORB_|TF_|TERRAFORM_)/i;
const sha256 = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const safeEnvironment = () => Object.fromEntries(Object.entries({ PATH: `${path.dirname(process.execPath)}:/usr/local/bin:/usr/bin:/bin`, HOME: process.env.HOME, LANG: "C.UTF-8", LC_ALL: "C.UTF-8", TZ: "UTC", SSL_CERT_FILE: process.env.SSL_CERT_FILE }).filter(([, value]) => value !== undefined));

async function regularBytes(file, limit = 128 * 1024 * 1024) {
  const before = await fs.lstat(file); if (!before.isFile() || before.isSymbolicLink() || before.nlink !== 1 || before.uid !== process.getuid() || before.size > limit) throw new Error(`ADMISSION_FILE_UNSAFE:${file}`);
  const handle = await fs.open(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  try { const opened = await handle.stat(); if (opened.dev !== before.dev || opened.ino !== before.ino || opened.nlink !== 1) throw new Error(`ADMISSION_FILE_INODE:${file}`); return await handle.readFile(); } finally { await handle.close(); }
}
function execute(command, args, options = {}) {
  const result = spawnSync(command, args, { cwd: options.cwd ?? repo, encoding: "utf8", stdio: options.inherit ? "inherit" : "pipe", timeout: options.timeout ?? 300000, env: options.env ?? safeEnvironment(), input: options.input });
  if (result.status !== 0) throw new Error(`COMMAND_FAILED:${path.basename(command)}:${result.status}:${result.stderr ?? ""}`);
  return result;
}

async function verifyPortalAdmission() {
  for (const name of Object.keys(process.env)) if (forbiddenEnvironment.test(name)) throw new Error(`ENVIRONMENT_UNSAFE:${name}`);
  const packageBytes = await regularBytes(path.join(appRoot, "package.json"), 1024 * 1024);
  const lockBytes = await regularBytes(path.join(appRoot, "package-lock.json"), 4 * 1024 * 1024);
  const packageValue = JSON.parse(packageBytes.toString("utf8"));
  if (packageValue.packageManager !== "npm@10.9.8" || packageValue.engines?.node !== "22.22.3" || packageValue.engines?.npm !== "10.9.8" || process.versions.node !== "22.22.3") throw new Error("PORTAL_RUNTIME_VERSION_MISMATCH");
  if (sha256(lockBytes) !== EXPECTED_LOCK_SHA256) throw new Error("PORTAL_LOCK_HASH_MISMATCH");
  const lock = JSON.parse(lockBytes.toString("utf8"));
  if (lock.lockfileVersion !== 3 || lock.packages?.[""]?.engines?.node !== "22.22.3" || lock.packages?.[""]?.engines?.npm !== "10.9.8") throw new Error("PORTAL_LOCK_GRAPH_MISMATCH");
  const npmCli = path.resolve(path.dirname(process.execPath), "../lib/node_modules/npm/bin/npm-cli.js");
  const npmBytes = await regularBytes(npmCli, 1024 * 1024); const nodeBytes = await regularBytes(process.execPath);
  const npmVersion = execute(process.execPath, [npmCli, "--version"]); if (npmVersion.stdout.trim() !== "10.9.8") throw new Error("PORTAL_NPM_VERSION_MISMATCH");
  execute(process.execPath, [npmCli, "ls", "--all", "--json"], { cwd: appRoot, timeout: 120000 });
  const activation = JSON.parse((await regularBytes(path.join(appRoot, "command-owner-activation.stage-a.json"), 1024 * 1024)).toString("utf8"));
  const fragmentHash = sha256(await regularBytes(path.join(repo, "mk/issue-5/i5-05.mk"), 1024 * 1024));
  const expectedCommands = ["learn", "learn-status", "learn-down", "portal-test", "portal-a11y", "portal-e2e", "lesson-e2e", "local-journey-e2e", "portal-visual-review"];
  if (activation.schemaVersion !== "command-owner-activation-v1" || activation.owner !== "I5-05" || activation.baseRegistrySha256 !== "a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80" || activation.fragment?.path !== "mk/issue-5/i5-05.mk" || activation.fragment.sha256 !== fragmentHash || JSON.stringify(activation.commands.map((row) => row.commandId)) !== JSON.stringify(expectedCommands) || activation.commands.some((row) => row.evidenceVersion !== "fitness-result-v2" || row.availability !== (["lesson-e2e", "local-journey-e2e"].includes(row.commandId) ? "unavailable" : "implemented"))) throw new Error("PORTAL_ACTIVATION_MISMATCH");
  return { node: process.versions.node, npm: npmVersion.stdout.trim(), nodeBinarySha256: sha256(nodeBytes), npmCliSha256: sha256(npmBytes), packageJsonSha256: sha256(packageBytes), lockSha256: sha256(lockBytes) };
}

async function verifyReleasedInputs() {
  const amendment = await fs.readFile(path.join(repo, "plans/260721-010-promotion-trust-portal/stage-a-release-amendment.md"), "utf8");
  const section = amendment.split("## Released Read-Only Dependency Binding")[1].split("## Exact Stage A Tracked Write Allowlist")[0];
  const rows = [...section.matchAll(/^\| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \| `([0-9a-f]{64})` \|$/gm)].map((match) => ({ path: match[1], blob: match[2], bytes: Number(match[3]), sha: match[4] }));
  if (rows.length !== 85) throw new Error(`RELEASE_CATALOGUE_COUNT:${rows.length}`);
  for (const row of rows) { const bytes = await regularBytes(path.join(repo, row.path)); if (bytes.length !== row.bytes || sha256(bytes) !== row.sha) throw new Error(`RELEASE_BYTES_DRIFT:${row.path}`); }
  const git = (args) => spawnSync("git", args, { cwd: repo, encoding: "utf8", env: safeEnvironment() });
  const release = "5644f01b4c0443a81f3af0bcce80f44c847cd986";
  if (git(["merge-base", "HEAD", release]).stdout.trim() !== release) throw new Error("RELEASE_ANCESTRY_MISMATCH");
  if (git(["rev-parse", `${release}^{tree}`]).stdout.trim() !== "a38594d420fe7df2b30265a8a72bb5fad1698012") throw new Error("RELEASE_TREE_MISMATCH");
  const model = await loadReleasedLearning({ root: repo });
  return { rows, model };
}

const canonical = (value) => {
  if (value === null || typeof value === "boolean" || typeof value === "string") return JSON.stringify(value);
  if (typeof value === "number" && Number.isFinite(value)) return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  throw new Error("CANONICAL_VALUE_INVALID");
};

async function stageBBlocked(commandId, admission) {
  if (!["lesson-e2e", "local-journey-e2e"].includes(commandId)) throw new Error("STAGE_B_COMMAND_INVALID");
  const activationPath = path.join(appRoot, "command-owner-activation.stage-a.json");
  const activationBytes = await regularBytes(activationPath, 1024 * 1024);
  const schemaBytes = await regularBytes(path.join(repo, "learning/contracts/fitness-result-v2.schema.json"), 1024 * 1024);
  const bindingBytes = await regularBytes(path.join(repo, "learning/bindings/vite/promotion-trust-v1.json"), 1024 * 1024);
  const now = new Date().toISOString();
  const publicArgv = commandId === "lesson-e2e" ? ["make", "lesson-e2e", "LESSON=promotion-trust"] : ["make", "local-journey-e2e"];
  const childArgv = [process.execPath, "apps/learning-portal/scripts/verify-stage-a-release.mjs", "--stage-b-block", commandId];
  const gitTree = execute("git", ["rev-parse", "HEAD^{tree}"]).stdout.trim();
  const value = {
    schemaVersion: "fitness-result-v2", commandId, owner: "I5-05",
    requested: { subjectType: commandId === "lesson-e2e" ? "lesson" : "contract-set", subjectId: commandId === "lesson-e2e" ? "promotion-trust" : "stage-b-issue-9", parameters: [] },
    status: "fail", failureCode: "STAGE_B_DEPENDENCY_UNAVAILABLE", remediation: "Keep Stage B blocked until Issue 9 has an independently approved exact-head release.",
    inputSha: "7cd01679c40bb014d6ea0f6f0403d50c97e82572", testedTreeSha: gitTree,
    dependencyMergeShas: ["5644f01b4c0443a81f3af0bcce80f44c847cd986"],
    contractHashes: [{ name: "command-owner-activation", sha256: sha256(activationBytes) }],
    fixtureHashes: [{ name: "promotion-trust-vite-binding", sha256: sha256(bindingBytes) }],
    schemaHashes: [{ name: "fitness-result-v2", sha256: sha256(schemaBytes) }],
    toolchain: [{ name: "node", version: admission.node }, { name: "npm", version: admission.npm }], lockSha256: admission.lockSha256,
    invocation: { publicArgv, canonicalChildArgv: ["node", "apps/learning-portal/scripts/verify-stage-a-release.mjs", "--stage-b-block", commandId], actualChildArgvSha256: sha256(Buffer.from(canonical(childArgv))), cwdRole: "repository-root" },
    startedAt: now, finishedAt: now, durationMs: 0,
    rawLocator: null, projectionLocator: null, envelopeLocator: null, projectionSha256: null,
    artifacts: [{ locator: "apps/learning-portal/command-owner-activation.stage-a.json", mediaType: "application/json", size: activationBytes.length, sha256: sha256(activationBytes) }],
    redactionClass: "public-contract-evidence", retentionClass: "review-bundle", rollback: { supported: true, preserveEvidence: true }, canonicalization: "RFC8785",
  };
  value.payloadSha256 = sha256(Buffer.from(canonical(value)));
  process.stderr.write(`${canonical(value)}\n`);
  process.exit(2);
}

async function buildPortal(admission) {
  const vite = path.join(appRoot, "node_modules/vite/bin/vite.js");
  const generator = path.join(appRoot, "scripts/generate-static-routes.mjs");
  await regularBytes(vite, 1024 * 1024); await regularBytes(generator, 1024 * 1024);
  execute(process.execPath, [vite, "build"], { cwd: appRoot, inherit: true, timeout: 180000 });
  execute(process.execPath, [generator], { cwd: appRoot, inherit: true, timeout: 120000 });
  const inventoryBytes = await regularBytes(path.join(appRoot, "dist/.portal-build-inventory.json"), 1024 * 1024);
  const inventory = JSON.parse(inventoryBytes.toString("utf8"));
  for (const key of ["node", "npm", "nodeBinarySha256", "npmCliSha256", "packageJsonSha256", "lockSha256"]) if (inventory[key] !== admission[key]) throw new Error(`BUILD_ADMISSION_MISMATCH:${key}`);
  if (inventory.production !== true || inventory.routes.length !== 13) throw new Error("BUILD_PRODUCTION_IDENTITY_MISMATCH");
  return sha256(inventoryBytes);
}

const admission = await verifyPortalAdmission();
const { rows, model } = await verifyReleasedInputs();
const blockedIndex = process.argv.indexOf("--stage-b-block");
if (blockedIndex >= 0) await stageBBlocked(process.argv[blockedIndex + 1], admission);
if (process.argv.includes("--build")) { const buildInventorySha256 = await buildPortal(admission); console.log(JSON.stringify({ status: "pass", releasePaths: rows.length, bindingId: model.bindingId, admission, buildInventorySha256 })); process.exit(0); }
if (process.argv.includes("--local-only")) { console.log(JSON.stringify({ status: "pass", releasePaths: rows.length, bindingId: model.bindingId, admission })); process.exit(0); }

const runtimeRoot = path.join(repo, ".artifacts/workspaces/golden");
async function ensurePrivateDirectory(directory) { await fs.mkdir(directory, { recursive: true, mode: 0o700 }); const stat = await fs.lstat(directory); if (!stat.isDirectory() || stat.isSymbolicLink() || stat.uid !== process.getuid()) throw new Error(`ARTIFACT_ROOT_UNSAFE:${directory}`); await fs.chmod(directory, 0o700); const secured = await fs.lstat(directory); if ((secured.mode & 0o777) !== 0o700) throw new Error(`ARTIFACT_PERMISSIONS_UNSAFE:${directory}`); }
for (const directory of [path.join(repo, ".artifacts"), path.join(repo, ".artifacts/workspaces"), runtimeRoot]) await ensurePrivateDirectory(directory);
const candidate = await fs.mkdtemp(path.join(runtimeRoot, "i5-05-stage-a-")); const venv = path.join(candidate, "venv"); let pythonHash;
try {
  const pythonVersion = execute("python3.12", ["--version"]); if (pythonVersion.stdout.trim() !== "Python 3.12.3") throw new Error("PYTHON_RUNTIME_VERSION_MISMATCH");
  execute("python3.12", ["-m", "venv", venv]); const python = path.join(venv, "bin/python3.12");
  execute(python, ["-m", "pip", "install", "--require-hashes", "--only-binary=:all:", "--no-cache-dir", "--index-url", "https://pypi.org/simple", "-r", "requirements/golden-py312-macos-arm64.lock"], { timeout: 300000, inherit: true });
  execute(python, ["-m", "pip", "check"], { inherit: true }); pythonHash = sha256(await fs.readFile(python));
  const env = { ...safeEnvironment(), LEARNING_RUNTIME_ROOT: ".artifacts/workspaces/golden", LEARNING_RUNTIME_CANDIDATE: candidate, LEARNING_RUNTIME_INTERPRETER_SHA256: pythonHash };
  execute("make", ["learning-runtime-admit"], { env, inherit: true });
  for (const args of [["learning-contracts-check"], ["lesson-check", "LESSON=promotion-trust"], ["api-contracts-check"]]) execute("make", args, { env, inherit: true });
  for (const args of [["lesson-e2e", "LESSON=promotion-trust"], ["local-journey-e2e"]]) {
    const blocked = spawnSync("make", args, { cwd: repo, encoding: "utf8", timeout: 120000, env });
    if (blocked.status !== 2 || blocked.stdout !== "") throw new Error(`STAGE_B_BLOCKED_CONTRACT_FAILED:${args[0]}`);
    const document = blocked.stderr.trim().split("\n")[0];
    execute(python, ["-c", "import json,sys; from scripts.learning_contracts.schema import validate_document; validate_document(json.loads(sys.stdin.read()), family='fitness-result')"], { env, input: document });
  }
} finally { await fs.rm(candidate, { recursive: true, force: true }); }
const result = { status: "pass", releasePaths: rows.length, bindingId: model.bindingId, runtime: "cleaned", interpreterSha256: pythonHash, admission, commands: ["learning-contracts-check", "lesson-check LESSON=promotion-trust", "api-contracts-check"] };
console.log(JSON.stringify(result));
