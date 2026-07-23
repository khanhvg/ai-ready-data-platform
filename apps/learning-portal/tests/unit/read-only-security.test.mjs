import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import test from 'node:test';

const appRoot=resolve(import.meta.dirname,'../..');
test('client and renderer contain no mutation, storage, network, runner, or execution surface',async()=>{
  const files=['src/main.jsx','src/app/app-shell.jsx','src/render/static-document.mjs'];
  const source=(await Promise.all(files.map((path)=>readFile(resolve(appRoot,path),'utf8')))).join('\n');
  for(const forbidden of [/<form\b/i,/<button\b/i,/localStorage/,/sessionStorage/,/indexedDB/,/serviceWorker/,/fetch\s*\(/,/XMLHttpRequest/,/WebSocket/,/child_process/]) assert.equal(forbidden.test(source),false,String(forbidden));
  assert.match(source,/<pre[^>]*>/); assert.match(source,/<code>/);
});
