import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";
import { loadReleasedLearning } from "../src/contracts/released-learning-adapter.mjs";

const repo = path.resolve(import.meta.dirname, "../../..");
const amendment = await fs.readFile(path.join(repo, "plans/260721-010-promotion-trust-portal/stage-a-release-amendment.md"), "utf8");
const section = amendment.split("## Released Read-Only Dependency Binding")[1].split("## Exact Stage A Tracked Write Allowlist")[0];
const rows = [...section.matchAll(/^\| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \| `([0-9a-f]{64})` \|$/gm)].map((match) => ({ path: match[1], blob: match[2], bytes: Number(match[3]), sha: match[4] }));
if (rows.length !== 85) throw new Error(`RELEASE_CATALOGUE_COUNT:${rows.length}`);
for (const row of rows) {
  const absolute = path.join(repo, row.path); const stat = await fs.lstat(absolute);
  if (!stat.isFile() || stat.isSymbolicLink() || stat.nlink !== 1) throw new Error(`RELEASE_FILE_TYPE:${row.path}`);
  const bytes = await fs.readFile(absolute); const sha = crypto.createHash("sha256").update(bytes).digest("hex");
  if (bytes.length !== row.bytes || sha !== row.sha) throw new Error(`RELEASE_BYTES_DRIFT:${row.path}`);
}
const git = (args) => spawnSync("git", args, { cwd: repo, encoding: "utf8" });
const release = "5644f01b4c0443a81f3af0bcce80f44c847cd986";
if (git(["merge-base", "HEAD", release]).stdout.trim() !== release) throw new Error("RELEASE_ANCESTRY_MISMATCH");
if (git(["rev-parse", `${release}^{tree}`]).stdout.trim() !== "a38594d420fe7df2b30265a8a72bb5fad1698012") throw new Error("RELEASE_TREE_MISMATCH");
const model = await loadReleasedLearning({ root: repo });
if (process.argv.includes("--local-only")) { console.log(JSON.stringify({ status: "pass", releasePaths: rows.length, bindingId: model.bindingId })); process.exit(0); }

const runtimeRoot = path.join(repo, ".artifacts/workspaces/golden");
async function ensurePrivateDirectory(directory) {
  await fs.mkdir(directory, { recursive: true, mode: 0o700 });
  const stat = await fs.lstat(directory);
  if (!stat.isDirectory() || stat.isSymbolicLink() || stat.uid !== process.getuid()) throw new Error(`ARTIFACT_ROOT_UNSAFE:${directory}`);
  await fs.chmod(directory, 0o700);
  const secured = await fs.lstat(directory);
  if ((secured.mode & 0o777) !== 0o700) throw new Error(`ARTIFACT_PERMISSIONS_UNSAFE:${directory}`);
}
for (const directory of [path.join(repo, ".artifacts"), path.join(repo, ".artifacts/evidence"), path.join(repo, ".artifacts/workspaces"), runtimeRoot]) await ensurePrivateDirectory(directory);
const candidate = await fs.mkdtemp(path.join(runtimeRoot, "i5-05-stage-a-"));
const venv = path.join(candidate, "venv");
const run = (command, args, options = {}) => { const result = spawnSync(command, args, { cwd: repo, stdio: "inherit", timeout: options.timeout ?? 300000, env: { ...process.env, ...options.env } }); if (result.status !== 0) throw new Error(`COMMAND_FAILED:${command}:${result.status}`); };
let pythonHash;
try {
  run("python3.12", ["-m", "venv", venv]);
  const python = path.join(venv, "bin/python3.12");
  run(python, ["-m", "pip", "install", "--require-hashes", "--only-binary=:all:", "--no-cache-dir", "--index-url", "https://pypi.org/simple", "-r", "requirements/golden-py312-macos-arm64.lock"]);
  run(python, ["-m", "pip", "check"]);
  pythonHash = crypto.createHash("sha256").update(await fs.readFile(python)).digest("hex");
  const env = { LEARNING_RUNTIME_ROOT: ".artifacts/workspaces/golden", LEARNING_RUNTIME_CANDIDATE: candidate, LEARNING_RUNTIME_INTERPRETER_SHA256: pythonHash };
  run("make", ["learning-runtime-admit"], { env });
  for (const args of [["learning-contracts-check"], ["lesson-check", "LESSON=promotion-trust"], ["api-contracts-check"]]) run("make", args, { env });
} finally {
  await fs.rm(candidate, { recursive: true, force: true });
}
const result = { status: "pass", releasePaths: rows.length, bindingId: model.bindingId, runtime: "cleaned", interpreterSha256: pythonHash, commands: ["learning-contracts-check", "lesson-check LESSON=promotion-trust", "api-contracts-check"] };
const evidenceRoot = path.join(repo, ".artifacts/evidence/local-journey"); await fs.mkdir(evidenceRoot, { recursive: true }); await fs.writeFile(path.join(evidenceRoot, "release-verifier.json"), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result));
