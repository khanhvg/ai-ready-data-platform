import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

process.umask(0o077);
const repo = path.resolve(import.meta.dirname, "../../..");
const EVIDENCE_PARENT = path.join(repo, ".hermes/issue-10-stage-a-v2/evidence");
export const DEFAULT_EVIDENCE_ROOT = path.join(EVIDENCE_PARENT, "local-journey");
const OWNER = ".portal-evidence-owner.json";
const DATA = Object.freeze(["axe.json", "console-csp.json", "desktop-catalog.png", "desktop-decision.png", "desktop-grains.png", "desktop-unavailable.png", "dom-inventory.json", "narrow-catalog.png", "narrow-decision.png", "narrow-grains.png", "narrow-unavailable.png", "no-js-inventory.json"]);
const FINAL = Object.freeze([...DATA, "uat-checklist.md", "evidence-index.json", "hash-manifest.sha256", OWNER].sort());
const MAX_FILES = 16; const MAX_TEXT = 2 * 1024 * 1024; const MAX_IMAGE = 16 * 1024 * 1024; const MAX_AGGREGATE = 64 * 1024 * 1024;
const sha256 = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const evidenceRoot = (value) => path.resolve(value ?? process.env.PORTAL_EVIDENCE_ROOT ?? DEFAULT_EVIDENCE_ROOT);
const privacyPattern = /(?:\/Users\/[^/\s]+\/|-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|(?:password|secret|token)\s*[:=]\s*["'][^"']{8,}["']|"(?:customer_email|card_number|raw_record)"\s*:)/i;

async function safeRoot(root, create = false) {
  if (create) await fs.mkdir(root, { mode: 0o700 });
  const stat = await fs.lstat(root);
  if (!stat.isDirectory() || stat.isSymbolicLink() || stat.uid !== process.getuid()) throw new Error("EVIDENCE_OWNER_MISMATCH");
  if ((stat.mode & 0o777) !== 0o700) throw new Error("EVIDENCE_OWNER_MISMATCH");
  if (await fs.realpath(root) !== root) throw new Error("EVIDENCE_ALIAS_FORBIDDEN");
  return stat;
}
async function ensureEvidenceParent() {
  let cursor = repo;
  for (const segment of [".hermes", "issue-10-stage-a-v2", "evidence"]) { cursor = path.join(cursor, segment); await fs.mkdir(cursor, { mode: 0o700 }).catch((error) => { if (error.code !== "EEXIST") throw error; }); const stat = await fs.lstat(cursor); if (!stat.isDirectory() || stat.isSymbolicLink() || stat.uid !== process.getuid()) throw new Error("EVIDENCE_ALIAS_FORBIDDEN"); }
  await fs.chmod(EVIDENCE_PARENT, 0o700); return safeRoot(EVIDENCE_PARENT);
}
async function approvedTarget(root) {
  await ensureEvidenceParent();
  const parent = await fs.realpath(EVIDENCE_PARENT); const resolved = path.resolve(root); const relative = path.relative(parent, resolved);
  if (!relative || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) throw new Error("EVIDENCE_ROOT_OUTSIDE_APPROVED_NAMESPACE");
  let cursor = parent;
  for (const segment of relative.split(path.sep).slice(0, -1)) { if (!/^[A-Za-z0-9._-]+$/.test(segment)) throw new Error("EVIDENCE_ROOT_OUTSIDE_APPROVED_NAMESPACE"); cursor = path.join(cursor, segment); const stat = await fs.lstat(cursor); if (!stat.isDirectory() || stat.isSymbolicLink() || stat.uid !== process.getuid()) throw new Error("EVIDENCE_ALIAS_FORBIDDEN"); }
  if (!/^[A-Za-z0-9._-]+$/.test(path.basename(resolved))) throw new Error("EVIDENCE_ROOT_OUTSIDE_APPROVED_NAMESPACE");
  return resolved;
}
async function safeFile(file, name) {
  const stat = await fs.lstat(file);
  if (!stat.isFile() || stat.isSymbolicLink() || stat.nlink !== 1 || stat.uid !== process.getuid() || (stat.mode & 0o777) !== 0o600) throw new Error("EVIDENCE_ALIAS_FORBIDDEN");
  const limit = name.endsWith(".png") ? MAX_IMAGE : MAX_TEXT;
  if (stat.size > limit) throw new Error("EVIDENCE_FILE_LIMIT");
  const handle = await fs.open(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  try { const opened = await handle.stat(); if (opened.dev !== stat.dev || opened.ino !== stat.ino || opened.nlink !== 1) throw new Error("EVIDENCE_ALIAS_FORBIDDEN"); return { bytes: await handle.readFile(), stat: opened }; } finally { await handle.close(); }
}
async function inventory(root) {
  const names = await fs.readdir(root);
  if (names.length > MAX_FILES || names.some((name) => name.includes("/") || name.endsWith("." + "zip"))) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  return names.sort();
}
async function owner(root) {
  const { bytes } = await safeFile(path.join(root, OWNER), OWNER);
  const value = JSON.parse(bytes.toString("utf8"));
  if (value.schemaVersion === "portal-evidence-owner-v1" && value.owner === "I5-05" && /^[0-9a-f]{64}$/.test(value.nonce) && Object.keys(value).sort().join(",") === "nonce,owner,schemaVersion") return { ...value, target: path.basename(root) };
  if (value.schemaVersion !== "portal-evidence-owner-v2" || value.owner !== "I5-05" || !/^[0-9a-f]{64}$/.test(value.nonce) || !/^[A-Za-z0-9._-]+$/.test(value.target) || Object.keys(value).sort().join(",") !== "nonce,owner,schemaVersion,target") throw new Error("EVIDENCE_OWNER_MISMATCH");
  return value;
}
async function verifyFinalized(root, quiet = false) {
  await safeRoot(root); await owner(root);
  if (JSON.stringify(await inventory(root)) !== JSON.stringify(FINAL)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  const manifest = (await safeFile(path.join(root, "hash-manifest.sha256"), "hash-manifest.sha256")).bytes.toString("utf8").trim().split("\n");
  const expected = new Map(manifest.map((line) => { const match = line.match(/^([0-9a-f]{64})  ([A-Za-z0-9._-]+)$/); if (!match) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED"); return [match[2], match[1]]; }));
  let total = 0;
  for (const name of FINAL.filter((name) => name !== "hash-manifest.sha256")) { const { bytes } = await safeFile(path.join(root, name), name); total += bytes.length; if (expected.get(name) !== sha256(bytes)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED"); if (!name.endsWith(".png") && privacyPattern.test(bytes.toString("utf8"))) throw new Error("EVIDENCE_PRIVACY_REJECTED"); }
  if (expected.size !== FINAL.length - 1 || total > MAX_AGGREGATE) throw new Error("EVIDENCE_AGGREGATE_LIMIT");
  if (!quiet) console.log(JSON.stringify({ maturity: "static-portal-stage-a", files: FINAL.length, bytes: total, privacy: "pass", verified: true }));
}

async function cleanupOwnedDirectory(root) {
  await safeRoot(root); const names = await inventory(root);
  if (!names.length) { await fs.rmdir(root); return; }
  await owner(root);
  if (names.some((name) => !FINAL.includes(name))) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  for (const name of names) await safeFile(path.join(root, name), name);
  for (const name of names.filter((name) => name !== OWNER)) await fs.rm(path.join(root, name));
  await fs.rm(path.join(root, OWNER)); await fs.rmdir(root);
}
const pointerPath = (target) => `${target}.current`;
async function readPointer(target, required = false) {
  const file = pointerPath(target); const exists = await fs.lstat(file).then(() => true, (error) => { if (error.code === "ENOENT") return false; throw error; });
  if (!exists) { if (required) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED"); return null; }
  const { bytes } = await safeFile(file, path.basename(file)); let value; try { value = JSON.parse(bytes.toString("utf8")); } catch { throw new Error("EVIDENCE_INVENTORY_UNEXPECTED"); }
  const prefix = `.${path.basename(target)}.generation-`;
  if (value.schemaVersion !== "portal-evidence-pointer-v1" || !value.generation.startsWith(prefix) || !/^[0-9a-f]{64}$/.test(value.generation.slice(prefix.length)) || !/^[0-9a-f]{64}$/.test(value.manifestSha256) || Object.keys(value).sort().join(",") !== "generation,manifestSha256,schemaVersion") throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  const generation = await approvedTarget(path.join(path.dirname(target), value.generation)); await verifyFinalized(generation, true);
  const manifest = (await safeFile(path.join(generation, "hash-manifest.sha256"), "hash-manifest.sha256")).bytes;
  if (sha256(manifest) !== value.manifestSha256) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  return generation;
}
async function publishPointer(target, generation) {
  const manifest = (await safeFile(path.join(generation, "hash-manifest.sha256"), "hash-manifest.sha256")).bytes; const nonce = crypto.randomBytes(32).toString("hex"); const temporary = path.join(path.dirname(target), `.${path.basename(target)}.pointer-${nonce}`);
  const bytes = Buffer.from(JSON.stringify({ schemaVersion: "portal-evidence-pointer-v1", generation: path.basename(generation), manifestSha256: sha256(manifest) }));
  const handle = await fs.open(temporary, "wx", 0o600); try { await handle.writeFile(bytes); } finally { await handle.close(); }
  await safeFile(temporary, path.basename(temporary)); await fs.rename(temporary, pointerPath(target));
}
async function cleanupResidue(target, current) {
  const parent = path.dirname(target); const base = path.basename(target); const names = await fs.readdir(parent); const managed = names.filter((name) => name.startsWith(`.${base}.staging-`) || name.startsWith(`.${base}.generation-`) || name.startsWith(`.${base}.pointer-`));
  if (managed.length > 8) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  for (const name of managed) { const item = path.join(parent, name); if (item === current) continue; if (name.startsWith(`.${base}.pointer-`)) { await safeFile(item, name); await fs.rm(item); } else await cleanupOwnedDirectory(item); }
}

export async function prepareEvidenceRoot(value, options = {}) {
  const target = await approvedTarget(evidenceRoot(value)); let current = await readPointer(target);
  const existing = await fs.lstat(target).then(() => true, (error) => { if (error.code === "ENOENT") return false; throw error; });
  if (existing) { if (current) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED"); await safeRoot(target); const names = await inventory(target); if (!names.length) await fs.rmdir(target); else { if (!options.reset) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED"); await verifyFinalized(target, true); const marker = await owner(target); const generation = path.join(path.dirname(target), `.${path.basename(target)}.generation-${marker.nonce}`); await fs.rename(target, generation); await publishPointer(target, generation); current = generation; } }
  if (current && !options.reset) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  await cleanupResidue(target, current);
  const nonce = crypto.randomBytes(32).toString("hex"); const root = path.join(path.dirname(target), `.${path.basename(target)}.staging-${nonce}`); await fs.mkdir(root, { mode: 0o700 }); await safeRoot(root);
  const marker = Buffer.from(JSON.stringify({ schemaVersion: "portal-evidence-owner-v2", owner: "I5-05", nonce, target: path.basename(target) }));
  const handle = await fs.open(path.join(root, OWNER), "wx", 0o600); try { await handle.writeFile(marker); } finally { await handle.close(); }
  return root;
}

export async function writeOwnedEvidence(name, value, rootValue) {
  if (!DATA.includes(name)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  const root = await approvedTarget(evidenceRoot(rootValue)); await safeRoot(root); await owner(root);
  const bytes = Buffer.isBuffer(value) ? value : Buffer.from(value);
  const limit = name.endsWith(".png") ? MAX_IMAGE : MAX_TEXT;
  if (bytes.length > limit) throw new Error("EVIDENCE_FILE_LIMIT");
  if (!name.endsWith(".png") && privacyPattern.test(bytes.toString("utf8"))) throw new Error("EVIDENCE_PRIVACY_REJECTED");
  const handle = await fs.open(path.join(root, name), "wx", 0o600); try { await handle.writeFile(bytes); } finally { await handle.close(); }
}

export async function finalizeEvidence(rootValue) {
  const root = await approvedTarget(evidenceRoot(rootValue)); await safeRoot(root); const marker = await owner(root);
  const stagingMatch = path.basename(root).match(/^\.(.+)\.staging-([0-9a-f]{64})$/); if (!stagingMatch || stagingMatch[1] !== marker.target || stagingMatch[2] !== marker.nonce) throw new Error("EVIDENCE_OWNER_MISMATCH");
  const target = await approvedTarget(path.join(path.dirname(root), marker.target));
  const names = await inventory(root);
  if (JSON.stringify(names) !== JSON.stringify([...DATA, OWNER].sort())) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  const checklist = Buffer.from("# Stage A UAT checklist\n\nMaturity: static-portal-stage-a\nApproval: UNAPPROVED\n\n- [ ] Vietnamese-first hierarchy and status copy\n- [ ] Keyboard order and focus visibility\n- [ ] 360px readability and no horizontal overflow\n- [ ] Four-grain and decision honesty\n- [ ] No false run, evidence, progress, or completion claim\n");
  const checklistHandle = await fs.open(path.join(root, "uat-checklist.md"), "wx", 0o600); try { await checklistHandle.writeFile(checklist); } finally { await checklistHandle.close(); }
  const rows = []; let total = 0;
  for (const name of [...DATA, "uat-checklist.md", OWNER].sort()) { const { bytes } = await safeFile(path.join(root, name), name); total += bytes.length; if (!name.endsWith(".png") && privacyPattern.test(bytes.toString("utf8"))) throw new Error("EVIDENCE_PRIVACY_REJECTED"); rows.push({ name, bytes: bytes.length, sha256: sha256(bytes) }); }
  if (total > MAX_AGGREGATE) throw new Error("EVIDENCE_AGGREGATE_LIMIT");
  const git = (args) => spawnSync("git", args, { cwd: repo, encoding: "utf8", env: { PATH: "/usr/bin:/bin" } }).stdout.trim();
  const index = Buffer.from(JSON.stringify({ schemaVersion: "portal-evidence-index-v1", inputSha: "7cd01679c40bb014d6ea0f6f0403d50c97e82572", sourceSha: git(["rev-parse", "HEAD"]), sourceTree: git(["rev-parse", "HEAD^{tree}"]), privacy: "pass", bounds: { maxFiles: MAX_FILES, maxTextBytes: MAX_TEXT, maxImageBytes: MAX_IMAGE, maxAggregateBytes: MAX_AGGREGATE, actualBytes: total }, files: rows }, null, 2));
  const indexHandle = await fs.open(path.join(root, "evidence-index.json"), "wx", 0o600); try { await indexHandle.writeFile(index); } finally { await indexHandle.close(); }
  const manifestRows = [];
  for (const name of [...DATA, "uat-checklist.md", "evidence-index.json", OWNER].sort()) { const { bytes } = await safeFile(path.join(root, name), name); manifestRows.push(`${sha256(bytes)}  ${name}`); }
  const manifestHandle = await fs.open(path.join(root, "hash-manifest.sha256"), "wx", 0o600); try { await manifestHandle.writeFile(`${manifestRows.join("\n")}\n`); } finally { await manifestHandle.close(); }
  if (JSON.stringify(await inventory(root)) !== JSON.stringify(FINAL)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  await verifyFinalized(root, true);
  const generation = await approvedTarget(path.join(path.dirname(target), `.${path.basename(target)}.generation-${marker.nonce}`)); await fs.rename(root, generation); await verifyFinalized(generation, true); await publishPointer(target, generation); await readPointer(target, true); await cleanupResidue(target, generation);
  console.log(JSON.stringify({ maturity: "static-portal-stage-a", files: FINAL.length, bytes: total, privacy: "pass" }));
  return generation;
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  const target = await approvedTarget(evidenceRoot()); const root = await readPointer(target) ?? target;
  await verifyFinalized(root);
}
