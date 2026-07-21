import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const sources = [
  '../../preview/index.html', '../../preview/preview.mjs', '../../preview/preview.css',
  '../fixtures/synthetic-promotion-trust-v1.json', '../state/preview-state.mjs',
];

test('WEB-PREVIEW-002 staticLogical contains no completion, runner, cloud, mutation or remote-content authority', async () => {
  const text = (await Promise.all(sources.map((path) => readFile(new URL(path, import.meta.url), 'utf8')))).join('\n');
  assert.doesNotMatch(text, /\bcompleted\b|runner[_ -]?url|aws[_ -]?access|cloud[_ -]?endpoint|serviceWorker|dangerouslySetInnerHTML|innerHTML\s*=|eval\s*\(|new Function|https?:\/\//i);
  assert.doesNotMatch(text, /\b(fetch|XMLHttpRequest|WebSocket)\s*\(|method\s*:\s*['"](?:POST|PUT|PATCH|DELETE)/i);
});

test('WEB-STATE-001 browser owns the one reducer implementation and common state re-exports it', async () => {
  const source = await readFile(new URL('../../preview/preview.mjs', import.meta.url), 'utf8');
  const common = await readFile(new URL('../state/preview-state.mjs', import.meta.url), 'utf8');
  assert.equal((source.match(/function\s+reducePreviewState\s*\(/g) ?? []).length, 1);
  assert.equal((common.match(/function\s+reducePreviewState\s*\(/g) ?? []).length, 0);
  assert.match(common, /reducePreviewState[\s\S]*from\s*['"]\.\.\/\.\.\/preview\/preview\.mjs['"]/);
});

test('WEB-API-001 every browser module dependency is one of the exact served routes', async () => {
  const source = await readFile(new URL('../../preview/preview.mjs', import.meta.url), 'utf8');
  const imports = [...source.matchAll(/\b(?:import|export)\s+(?:[^'";]+?\s+from\s+)?['"]([^'"]+)['"]/g)].map((match) => match[1]);
  assert.deepEqual(imports, []);
});

test('WEB-A11Y-001 explicit previous/next commits and leaves native anchor navigation operable', async () => {
  const source = await readFile(new URL('../../preview/preview.mjs', import.meta.url), 'utf8');
  assert.doesNotMatch(source, /event\.preventDefault\(\)/);
  assert.doesNotMatch(source, /focus\(\s*\{\s*preventScroll\s*:\s*true/);
  assert.match(source, /reducePreviewState\([^)]*navigate-explicit/s);
});
