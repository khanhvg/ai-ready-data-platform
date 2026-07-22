import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
const repo = path.resolve(import.meta.dirname, "../../.."); const root = path.join(repo, ".artifacts/evidence/local-journey"); await fs.mkdir(root, { recursive: true });
const checklist = `# Stage A UAT checklist\n\nMaturity: static-portal-stage-a\nApproval: UNAPPROVED\n\n- [ ] Vietnamese-first hierarchy and status copy\n- [ ] Keyboard order and focus visibility\n- [ ] 360px readability and no horizontal overflow\n- [ ] Four-grain and decision honesty\n- [ ] No false run, evidence, progress, or completion claim\n`;
await fs.writeFile(path.join(root, "uat-checklist.md"), checklist);
const files = (await fs.readdir(root, { recursive: true })).filter((name) => !name.endsWith("hash-manifest.sha256"));
const lines = []; for (const name of files.sort()) { const absolute = path.join(root, name); const stat = await fs.lstat(absolute); if (stat.isFile()) lines.push(`${crypto.createHash("sha256").update(await fs.readFile(absolute)).digest("hex")}  ${name}`); }
await fs.writeFile(path.join(root, "hash-manifest.sha256"), lines.join("\n") + "\n"); console.log(JSON.stringify({ maturity: "static-portal-stage-a", files: lines.length }));
