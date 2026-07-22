import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

process.umask(0o077);
const repo = path.resolve(import.meta.dirname, "../../..");
export const DEFAULT_EVIDENCE_ROOT = path.join(repo, ".hermes/issue-10-stage-a-v2/evidence/local-journey");
const OWNER = ".portal-evidence-owner.json";
const DATA = Object.freeze(["axe.json", "console-csp.json", "desktop-catalog.png", "desktop-decision.png", "desktop-grains.png", "desktop-unavailable.png", "dom-inventory.json", "narrow-catalog.png", "narrow-decision.png", "narrow-grains.png", "narrow-unavailable.png", "no-js-inventory.json"]);
const FINAL = Object.freeze([...DATA, "uat-checklist.md", "evidence-index.json", "hash-manifest.sha256", OWNER].sort());
const MAX_FILES = 16; const MAX_TEXT = 2 * 1024 * 1024; const MAX_IMAGE = 16 * 1024 * 1024; const MAX_AGGREGATE = 64 * 1024 * 1024;
const sha256 = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const evidenceRoot = (value) => path.resolve(value ?? process.env.PORTAL_EVIDENCE_ROOT ?? DEFAULT_EVIDENCE_ROOT);
const privacyPattern = /(?:\/Users\/[^/\s]+\/|-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|(?:password|secret|token)\s*[:=]\s*["'][^"']{8,}["']|"(?:customer_email|card_number|raw_record)"\s*:)/i;

async function safeRoot(root, create = false) {
  if (create) await fs.mkdir(root, { recursive: true, mode: 0o700 });
  const stat = await fs.lstat(root);
  if (!stat.isDirectory() || stat.isSymbolicLink() || stat.uid !== process.getuid()) throw new Error("EVIDENCE_OWNER_MISMATCH");
  if ((stat.mode & 0o777) !== 0o700) throw new Error("EVIDENCE_OWNER_MISMATCH");
  if (await fs.realpath(root) !== root) throw new Error("EVIDENCE_ALIAS_FORBIDDEN");
  return stat;
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
  if (value.schemaVersion !== "portal-evidence-owner-v1" || value.owner !== "I5-05" || !/^[0-9a-f]{64}$/.test(value.nonce) || Object.keys(value).sort().join(",") !== "nonce,owner,schemaVersion") throw new Error("EVIDENCE_OWNER_MISMATCH");
  return value;
}
async function removeFinalized(root) {
  await owner(root);
  const names = await inventory(root);
  if (JSON.stringify(names) !== JSON.stringify(FINAL)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  for (const name of names) await safeFile(path.join(root, name), name);
  for (const name of names) await fs.rm(path.join(root, name));
}

export async function prepareEvidenceRoot(value, options = {}) {
  const root = evidenceRoot(value); await safeRoot(root, true);
  const names = await inventory(root);
  if (names.length) {
    if (!names.includes(OWNER)) throw new Error("EVIDENCE_OWNER_MISMATCH");
    if (!options.reset) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
    await removeFinalized(root);
  }
  const marker = Buffer.from(JSON.stringify({ schemaVersion: "portal-evidence-owner-v1", owner: "I5-05", nonce: crypto.randomBytes(32).toString("hex") }));
  const handle = await fs.open(path.join(root, OWNER), "wx", 0o600); try { await handle.writeFile(marker); } finally { await handle.close(); }
  return root;
}

export async function writeOwnedEvidence(name, value, rootValue) {
  if (!DATA.includes(name)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  const root = evidenceRoot(rootValue); await safeRoot(root); await owner(root);
  const bytes = Buffer.isBuffer(value) ? value : Buffer.from(value);
  const limit = name.endsWith(".png") ? MAX_IMAGE : MAX_TEXT;
  if (bytes.length > limit) throw new Error("EVIDENCE_FILE_LIMIT");
  if (!name.endsWith(".png") && privacyPattern.test(bytes.toString("utf8"))) throw new Error("EVIDENCE_PRIVACY_REJECTED");
  const handle = await fs.open(path.join(root, name), "wx", 0o600); try { await handle.writeFile(bytes); } finally { await handle.close(); }
}

export async function finalizeEvidence(rootValue) {
  const root = evidenceRoot(rootValue); await safeRoot(root); await owner(root);
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
  console.log(JSON.stringify({ maturity: "static-portal-stage-a", files: FINAL.length, bytes: total, privacy: "pass" }));
}

async function verifyFinalized(root) {
  await safeRoot(root); await owner(root);
  if (JSON.stringify(await inventory(root)) !== JSON.stringify(FINAL)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  const manifest = (await safeFile(path.join(root, "hash-manifest.sha256"), "hash-manifest.sha256")).bytes.toString("utf8").trim().split("\n");
  const expected = new Map(manifest.map((line) => { const match = line.match(/^([0-9a-f]{64})  ([A-Za-z0-9._-]+)$/); if (!match) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED"); return [match[2], match[1]]; }));
  let total = 0;
  for (const name of FINAL.filter((name) => name !== "hash-manifest.sha256")) { const { bytes } = await safeFile(path.join(root, name), name); total += bytes.length; if (expected.get(name) !== sha256(bytes)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED"); if (!name.endsWith(".png") && privacyPattern.test(bytes.toString("utf8"))) throw new Error("EVIDENCE_PRIVACY_REJECTED"); }
  if (expected.size !== FINAL.length - 1 || total > MAX_AGGREGATE) throw new Error("EVIDENCE_AGGREGATE_LIMIT");
  console.log(JSON.stringify({ maturity: "static-portal-stage-a", files: FINAL.length, bytes: total, privacy: "pass", verified: true }));
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? "").href) {
  const root = evidenceRoot();
  const names = await fs.readdir(root).catch((error) => { if (error.code === "ENOENT") return []; throw error; });
  if (names.length && !names.includes(OWNER)) throw new Error("EVIDENCE_OWNER_MISMATCH");
  if (JSON.stringify(names.sort()) !== JSON.stringify(FINAL)) throw new Error("EVIDENCE_INVENTORY_UNEXPECTED");
  await verifyFinalized(root);
}
