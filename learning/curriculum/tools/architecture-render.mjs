#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { Graphviz } from '@hpcc-js/wasm-graphviz';

const mapping = {
  c4_l2_aws: 'C4-L2-AWS', dep_aws: 'DEP-AWS', dyn_office: 'DYN-OFFICE',
  dyn_publish: 'DYN-PUBLISH', dyn_restore: 'DYN-RESTORE',
};

async function main(argv) {
  const [dotDir, outDir] = argv;
  if (!dotDir || !outDir || fs.existsSync(outDir)) throw new Error('fresh dot and output directories are required');
  fs.mkdirSync(outDir, { recursive: false, mode: 0o700 });
  const graphviz = await Graphviz.load();
  for (const [key, external] of Object.entries(mapping)) {
    const source = path.join(dotDir, 'views', `${key}.dot`);
    if (!fs.statSync(source, { throwIfNoEntry: false })?.isFile()) throw new Error(`missing expansion DOT: ${key}`);
    const svg = graphviz.layout(fs.readFileSync(source, 'utf8'), 'svg', 'dot');
    fs.writeFileSync(path.join(outDir, `${external}.raw.svg`), svg, { mode: 0o600 });
  }
  process.stdout.write(`graphviz=${graphviz.version()} views=5\n`);
}

main(process.argv.slice(2)).catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
