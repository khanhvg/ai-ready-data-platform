#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

async function main(argv) {
  if (argv.length !== 1) throw new Error('expected one regular input path');
  const bytes = await readFile(argv[0]);
  process.stdout.write(`${createHash('sha256').update(bytes).digest('hex')}\n`);
}

main(process.argv.slice(2)).catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
