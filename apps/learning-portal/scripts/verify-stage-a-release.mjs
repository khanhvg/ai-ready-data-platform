import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = resolve(appRoot, '../..');
const packageLock = await readFile(resolve(appRoot, 'package-lock.json'));
const expectedInputSha = '0972fa20dc7ec2dd30468fa700946a3e20808e43';
const sourceHead = execFileSync('git', ['rev-parse', 'HEAD'], {
  cwd: repositoryRoot,
  encoding: 'utf8'
}).trim();
let inputIsAncestor = false;
try {
  execFileSync('git', ['merge-base', '--is-ancestor', expectedInputSha, sourceHead], {
    cwd: repositoryRoot
  });
  inputIsAncestor = true;
} catch {
  inputIsAncestor = false;
}
const release = {
  inputSha: expectedInputSha,
  sourceHead,
  inputIsAncestor,
  node: process.versions.node,
  lockSha256: createHash('sha256').update(packageLock).digest('hex'),
  expectedNode: '22.22.3',
  expectedNpm: '10.9.8',
  expectedChrome: '150.0.7871.181',
  expectedChromeSha256: 'b724a4c5603cfc8b9d9f27a5153c8a39e7133e53666ced7f2a8b03bf49484f85',
  releasedInputsAdmitted: 0,
  releasedInputsRequired: 85
};
release.identityReady =
  release.inputIsAncestor && release.node === release.expectedNode;
release.semanticReady =
  release.identityReady && release.releasedInputsAdmitted === release.releasedInputsRequired;
process.stdout.write(`${JSON.stringify(release)}\n`);
process.exitCode = release.identityReady ? 0 : 1;
