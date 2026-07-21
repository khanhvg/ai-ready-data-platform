#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { Graphviz } from '@hpcc-js/wasm-graphviz';

const [dotDir, outDir] = process.argv.slice(2);
if (!dotDir || !outDir || fs.existsSync(outDir)) {
  process.stderr.write('ARCH_RENDER_FAILED: fresh dot and output directories are required\n');
  process.exit(2);
}
fs.mkdirSync(outDir, { recursive: false, mode: 0o700 });
const mapping = {
  index: 'C4-L0', c4_l1: 'C4-L1', c4_l2_local: 'C4-L2-LOCAL',
  c4_l3_runner: 'C4-L3-RUNNER', dep_local: 'DEP-LOCAL', dyn_journey: 'DYN-JOURNEY'
};
const graphviz = await Graphviz.load();
for (const [key, external] of Object.entries(mapping)) {
  const source = path.join(dotDir, 'views', `${key}.dot`);
  if (!fs.statSync(source, { throwIfNoEntry: false })?.isFile()) {
    throw new Error(`ARCH_VIEW_SET_MISMATCH:${key}`);
  }
  const svg = graphviz.layout(fs.readFileSync(source, 'utf8'), 'svg', 'dot');
  fs.writeFileSync(path.join(outDir, `${external}.raw.svg`), svg, { mode: 0o600 });
}
process.stdout.write(`graphviz=${graphviz.version()} views=6\n`);
