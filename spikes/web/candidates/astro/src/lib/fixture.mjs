import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
const paths = {
  retail: 'contracts/data/retail-golden-v1.json',
  contract: 'contracts/data/promotion-trust-v1.yaml',
  evidence: 'tests/fixtures/learning/promotion-trust/evidence-v1.json',
  manifest: 'tests/fixtures/learning/promotion-trust/manifest.json',
};
const repositoryRoot = resolve(process.cwd(), '../../../..');
const read = (path) => readFileSync(resolve(repositoryRoot, path));
export function loadFixture() {
  const bytes = Object.fromEntries(Object.entries(paths).map(([key, path]) => [key, read(path)]));
  const evidence = JSON.parse(bytes.evidence); const manifest = JSON.parse(bytes.manifest);
  return { evidence, manifest, contractText: bytes.contract.toString('utf8'), retail: JSON.parse(bytes.retail), digests: Object.fromEntries(Object.entries(bytes).map(([key, value]) => [key, createHash('sha256').update(value).digest('hex')])) };
}
