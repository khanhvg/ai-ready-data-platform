import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import test from 'node:test';
import { AUTHORITIES, loadPortalCatalog, repositoryRoot } from '../../src/sources/portal-source-loader.mjs';

test('source loader binds exact schemas, hashes, counts, IDs, signatures, and order', async () => {
  const catalog = loadPortalCatalog();
  assert.equal(catalog.schemaVersion, 'portal-read-only-catalog-v1');
  assert.deepEqual(catalog.counts, { modules:20, flows:11, bridges:8, views:5, templates:12, patterns:2, labs:3 });
  assert.deepEqual(catalog.curriculum.modules.map(({id})=>id), ['F01','F02','F03','F04','J01','J02','J03','J04','J05','J06','D01','D02','D03','D04','D05','D06','M01','M02','M03','M04']);
  assert.deepEqual(catalog.curriculum.collections.map(({id})=>id), ['foundation','junior','data','mid']);
  for (const [path, expected] of Object.entries(AUTHORITIES)) {
    const actual = createHash('sha256').update(await readFile(resolve(repositoryRoot,path))).digest('hex');
    assert.equal(actual, expected, path);
  }
});

test('source loader exposes no copied source registry or runnable candidate operation', () => {
  const catalog = loadPortalCatalog();
  assert.equal(catalog.manualOnly, true);
  assert.equal(catalog.labs.every((lab)=>lab.descriptor.commands.every(({id})=>id.startsWith('candidate.'))), true);
  assert.equal(catalog.labs.flatMap(({commands})=>commands).every((command)=>/^make [a-z-]+(?: [A-Z]+=[a-z0-9]+)*$/.test(command)), true);
});
