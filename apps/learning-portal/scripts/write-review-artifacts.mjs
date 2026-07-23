import { createHash, randomUUID } from 'node:crypto';
import { chmod, lstat, mkdir, readFile, rename, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createReleasedLearningAdapter } from '../src/contracts/released-learning-adapter.mjs';
import { createReleasedModuleProvider } from '../src/catalog/released-module-provider.mjs';
import { deriveModuleCatalog } from '../src/catalog/module-catalog.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = resolve(appRoot, '../..');
const artifactsRoot = resolve(repositoryRoot, '.artifacts');
const evidenceParent = resolve(artifactsRoot, 'evidence');
const evidenceRoot = resolve(evidenceParent, 'local-journey');
const requestedGeneration = process.env.PORTAL_EVIDENCE_GENERATION;
const generation = requestedGeneration ?? `stage-a-author-cook-${randomUUID()}`;
if (!/^[a-z0-9][a-z0-9-]{0,95}$/.test(generation)) {
  throw new Error('PORTAL_EVIDENCE_GENERATION_INVALID');
}
const finalRoot = resolve(evidenceRoot, generation);
if (dirname(finalRoot) !== evidenceRoot) throw new Error('PORTAL_EVIDENCE_GENERATION_INVALID');
const pendingRoot = resolve(evidenceRoot, `.pending-${randomUUID()}`);
const selectorPath = resolve(evidenceRoot, 'current-generation.json');

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function assertCondition(condition, code = 'PORTAL_EVIDENCE_CLOSURE_INVALID') {
  if (!condition) throw new Error(code);
}

async function ensurePrivateDirectory(path) {
  try {
    await mkdir(path, { mode: 0o700 });
  } catch (error) {
    if (error?.code !== 'EEXIST') throw error;
  }
  const metadata = await lstat(path);
  assertCondition(
    metadata.isDirectory() &&
      !metadata.isSymbolicLink() &&
      metadata.uid === process.getuid() &&
      (metadata.mode & 0o777) === 0o700
  );
}

async function assertAbsent(path) {
  try {
    await lstat(path);
    throw new Error('PORTAL_EVIDENCE_GENERATION_EXISTS');
  } catch (error) {
    if (error?.code !== 'ENOENT') throw error;
  }
}

async function writePrivate(path, bytes, exclusive = false) {
  await writeFile(path, bytes, { mode: 0o600, flag: exclusive ? 'wx' : 'w' });
  await chmod(path, 0o600);
}

async function verifyRegularPrivate(path, expectedBytes) {
  const [metadata, bytes] = await Promise.all([lstat(path), readFile(path)]);
  assertCondition(
    metadata.isFile() &&
      !metadata.isSymbolicLink() &&
      metadata.nlink === 1 &&
      metadata.uid === process.getuid() &&
      (metadata.mode & 0o777) === 0o600 &&
      metadata.size === expectedBytes.length &&
      bytes.equals(expectedBytes)
  );
}

async function verifyClosedGeneration(root, reviewBytes, inventoryBytes, indexBytes) {
  const metadata = await lstat(root);
  assertCondition(
    metadata.isDirectory() &&
      !metadata.isSymbolicLink() &&
      metadata.uid === process.getuid() &&
      (metadata.mode & 0o777) === 0o700
  );
  await verifyRegularPrivate(resolve(root, 'review.json'), reviewBytes);
  await verifyRegularPrivate(resolve(root, 'inventory.json'), inventoryBytes);
  await verifyRegularPrivate(resolve(root, 'generation-index.json'), indexBytes);
  const inventory = JSON.parse(inventoryBytes);
  const index = JSON.parse(indexBytes);
  const aggregateRows = `${inventory.rows
    .map((row) => `${row.path}\t${row.bytes}\t${row.sha256}`)
    .join('\n')}\n`;
  assertCondition(
    inventory.fileCount === 1 &&
      inventory.rows.length === 1 &&
      inventory.rows[0].path === 'review.json' &&
      inventory.rows[0].bytes === reviewBytes.length &&
      inventory.rows[0].sha256 === sha256(reviewBytes) &&
      index.inventory.bytes === inventoryBytes.length &&
      index.inventory.sha256 === sha256(inventoryBytes) &&
      index.payloadFileCount === inventory.fileCount &&
      index.aggregateBytes === inventory.aggregateBytes &&
      index.aggregateSha256 === sha256(aggregateRows)
  );
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

for (const directory of [artifactsRoot, evidenceParent, evidenceRoot]) {
  await ensurePrivateDirectory(directory);
}
await assertAbsent(finalRoot);
await assertAbsent(pendingRoot);
await mkdir(pendingRoot, { mode: 0o700 });
await chmod(pendingRoot, 0o700);
const reviewPath = resolve(pendingRoot, 'review.json');
await writePrivate(reviewPath, reviewBytes, true);
const reviewMetadata = await lstat(reviewPath);
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
await writePrivate(resolve(pendingRoot, 'inventory.json'), inventoryBytes, true);
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
await writePrivate(resolve(pendingRoot, 'generation-index.json'), indexBytes, true);
await verifyClosedGeneration(pendingRoot, reviewBytes, inventoryBytes, indexBytes);

await rename(pendingRoot, finalRoot);
await verifyClosedGeneration(finalRoot, reviewBytes, inventoryBytes, indexBytes);
const selectorMetadata = await lstat(selectorPath).catch((error) => {
  if (error?.code === 'ENOENT') return undefined;
  throw error;
});
if (selectorMetadata) {
  assertCondition(
    selectorMetadata.isFile() &&
      !selectorMetadata.isSymbolicLink() &&
      selectorMetadata.nlink === 1 &&
      selectorMetadata.uid === process.getuid() &&
      (selectorMetadata.mode & 0o777) === 0o600
  );
}
const selector = {
  schemaVersion: 'stage-a-current-generation-selector-v1',
  generation,
  generationIndexSha256: sha256(indexBytes)
};
const selectorPending = resolve(evidenceRoot, `.selector-${randomUUID()}.pending`);
await writePrivate(selectorPending, Buffer.from(`${JSON.stringify(selector)}\n`), true);
await rename(selectorPending, selectorPath);
await chmod(selectorPath, 0o600);

process.stdout.write(
  `${JSON.stringify({
    path: resolve(finalRoot, 'review.json'),
    generation,
    semanticReady: false,
    releasedContentReady: catalog.semanticReady
  })}\n`
);
