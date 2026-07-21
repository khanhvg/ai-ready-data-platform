import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

test('WEB-NONCOPY-001 staticLogical records principle-only inspiration and project-owned expression; reviewer remains pending', async () => {
  const inventory = await readFile(new URL('../../non-copy-inventory.md', import.meta.url), 'utf8');
  assert.match(inventory, /principle/i);
  assert.match(inventory, /project-owned|independently authored/i);
  assert.match(inventory, /wording|layout|visual|interaction/i);
  assert.match(inventory, /staticLogical[^\n]*(?:required|pass)/i);
  assert.match(inventory, /manualDecision[^\n]*required-pending/i);
  assert.match(inventory, /reviewer[^\n]*(?:required-pending|pending)/i);
  assert.doesNotMatch(inventory, /copied (?:source|prose|asset|layout)|derived from reference/i);
});
