import { createHash } from 'node:crypto';
import { chmod, mkdir, rename, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createReleasedLearningAdapter } from '../src/contracts/released-learning-adapter.mjs';
import { createReleasedModuleProvider } from '../src/catalog/released-module-provider.mjs';
import { deriveModuleCatalog } from '../src/catalog/module-catalog.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = resolve(appRoot, '../..');
const outputRoot = resolve(
  repositoryRoot,
  '.artifacts/evidence/local-journey/pending-scaffold-review'
);
const pendingPath = resolve(outputRoot, 'review.json.pending');
const finalPath = resolve(outputRoot, 'review.json');
const adapter = createReleasedLearningAdapter();
const catalog = deriveModuleCatalog(createReleasedModuleProvider(adapter).readRegistry());
const payload = {
  schemaVersion: 'portal-scaffold-review-v1',
  role: 'author-cook',
  semanticReady: catalog.semanticReady,
  descriptorCount: catalog.modules.length,
  independentlyReviewed: false,
  humanApproved: false
};
const bytes = `${JSON.stringify(payload)}\n`;
payload.payloadSha256 = createHash('sha256').update(bytes).digest('hex');
await mkdir(outputRoot, { recursive: true, mode: 0o700 });
await chmod(outputRoot, 0o700);
await writeFile(pendingPath, `${JSON.stringify(payload)}\n`, { mode: 0o600 });
await rename(pendingPath, finalPath);
await chmod(finalPath, 0o600);
process.stdout.write(`${JSON.stringify({ path: finalPath, semanticReady: payload.semanticReady })}\n`);
