import { createHash, randomUUID } from 'node:crypto';
import { chmod, mkdir, readFile, rename, rm, stat, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createReleasedLearningAdapter } from '../src/contracts/released-learning-adapter.mjs';
import { createReleasedModuleProvider } from '../src/catalog/released-module-provider.mjs';
import { deriveModuleCatalog } from '../src/catalog/module-catalog.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = resolve(appRoot, '../..');
const evidenceRoot = resolve(repositoryRoot, '.artifacts/evidence/local-journey');
const generation = process.env.PORTAL_EVIDENCE_GENERATION ?? 'stage-a-author-cook-current';
const finalRoot = resolve(evidenceRoot, generation);
const pendingRoot = resolve(evidenceRoot, `${generation}.pending-${randomUUID()}`);

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

async function writePrivate(path, bytes) {
  await writeFile(path, bytes, { mode: 0o600 });
  await chmod(path, 0o600);
}

const adapter = createReleasedLearningAdapter();
const catalog = deriveModuleCatalog(createReleasedModuleProvider(adapter).readRegistry());
const payload = {
  schemaVersion: 'stage-a-current-generation-v1',
  role: 'author-cook',
  semanticReady: false,
  releasedContentReady: catalog.semanticReady,
  descriptorCount: catalog.modules.length,
  runner: 'unavailable',
  execution: 'disabled',
  reset: 'not-run',
  freshEvidence: false,
  progress: 'disabled',
  completion: 'disabled',
  stageB: 'blocked-on-issue9',
  independentlyReviewed: false,
  humanApproved: false
};
const payloadCore = `${JSON.stringify(payload)}\n`;
payload.payloadSha256 = sha256(payloadCore);
const reviewBytes = Buffer.from(`${JSON.stringify(payload)}\n`);

await mkdir(evidenceRoot, { recursive: true, mode: 0o700 });
await chmod(evidenceRoot, 0o700);
await mkdir(pendingRoot, { mode: 0o700 });
await chmod(pendingRoot, 0o700);
const reviewPath = resolve(pendingRoot, 'review.json');
await writePrivate(reviewPath, reviewBytes);
const reviewMetadata = await stat(reviewPath);
const inventory = {
  schemaVersion: 'stage-a-inventory-v1',
  nonSelf: true,
  fileCount: 1,
  aggregateBytes: reviewBytes.length,
  rows: [
    {
      path: 'review.json',
      mode: '0600',
      type: 'regular',
      nlink: reviewMetadata.nlink,
      mediaType: 'application/json',
      privacy: 'review-sanitized',
      bytes: reviewBytes.length,
      sha256: sha256(reviewBytes)
    }
  ]
};
const inventoryBytes = Buffer.from(`${JSON.stringify(inventory)}\n`);
await writePrivate(resolve(pendingRoot, 'inventory.json'), inventoryBytes);
const aggregateRows = `${inventory.rows
  .map((row) => `${row.path}\t${row.bytes}\t${row.sha256}`)
  .join('\n')}\n`;
const generationIndex = {
  schemaVersion: 'stage-a-generation-index-v1',
  nonSelf: true,
  generation,
  inventory: {
    path: 'inventory.json',
    bytes: inventoryBytes.length,
    sha256: sha256(inventoryBytes)
  },
  payloadFileCount: inventory.fileCount,
  aggregateBytes: inventory.aggregateBytes,
  aggregateSha256: sha256(aggregateRows),
  role: 'author-cook',
  independentlyReviewed: false,
  humanApproved: false
};
const indexBytes = Buffer.from(`${JSON.stringify(generationIndex)}\n`);
await writePrivate(resolve(pendingRoot, 'generation-index.json'), indexBytes);

await rm(finalRoot, { recursive: true, force: true });
await rename(pendingRoot, finalRoot);
await chmod(finalRoot, 0o700);
const selector = {
  schemaVersion: 'stage-a-current-generation-selector-v1',
  generation,
  generationIndexSha256: sha256(indexBytes)
};
const selectorPending = resolve(evidenceRoot, `current-generation.${randomUUID()}.pending`);
await writePrivate(selectorPending, Buffer.from(`${JSON.stringify(selector)}\n`));
await rename(selectorPending, resolve(evidenceRoot, 'current-generation.json'));
await chmod(resolve(evidenceRoot, 'current-generation.json'), 0o600);

process.stdout.write(
  `${JSON.stringify({
    path: resolve(finalRoot, 'review.json'),
    generation,
    semanticReady: false,
    releasedContentReady: catalog.semanticReady
  })}\n`
);
