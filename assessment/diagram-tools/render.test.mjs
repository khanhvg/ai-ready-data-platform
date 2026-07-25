import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { normalizeSvg, validateSource } from "./render.mjs";

const diagram = {
  id: "security-test",
  title: "Security test title",
  description: "Security test description with sufficient detail.",
};
const safeSource = `flowchart LR
accTitle: ${diagram.title}
accDescr: ${diagram.description}
A[Source] --> B[Product]
`;

test("private renderer modes reject direct execution outside the sandbox", () => {
  const result = spawnSync(
    process.execPath,
    [fileURLToPath(new URL("./render.mjs", import.meta.url)), "--sandboxed-verify"],
    {
      encoding: "utf8",
      env: { ...process.env, ASSESSMENT_LOOPBACK_SANDBOX: "" },
    },
  );
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /network-denying wrapper/);
});

test("private renderer modes reject a forged sandbox marker", () => {
  const result = spawnSync(
    process.execPath,
    [fileURLToPath(new URL("./render.mjs", import.meta.url)), "--sandboxed-verify"],
    {
      encoding: "utf8",
      env: {
        ...process.env,
        ASSESSMENT_LOOPBACK_SANDBOX: "1",
        ASSESSMENT_LOOPBACK_CAPABILITY_FD: "",
      },
      timeout: 5_000,
    },
  );
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /inherited sandbox capability/);
});

test("source validation rejects active and remote Mermaid content", () => {
  validateSource(safeSource, diagram);
  for (const unsafe of [
    "click A callback",
    "%%{init: {'securityLevel': 'loose'}}%%",
    "<script>alert(1)</script>",
    "A[https://remote.invalid/image.svg]",
    "A[![remote](https://remote.invalid/image.svg)]",
    "A[icon:remote]",
    "A[javascript:alert(1)]",
  ]) {
    assert.throws(
      () => validateSource(`${safeSource}${unsafe}\n`, diagram),
      /forbidden content/,
    );
  }
});

test("source validation requires the allowlisted diagram type and accessibility text", () => {
  assert.throws(
    () => validateSource(safeSource.replace("flowchart", "sequenceDiagram"), diagram),
    /only flowchart/,
  );
  assert.throws(
    () => validateSource(safeSource.replace(diagram.title, "Changed title"), diagram),
    /accessible title/,
  );
  assert.throws(
    () => validateSource(safeSource.replace(diagram.description, "Changed description"), diagram),
    /accessible description/,
  );
});

test("SVG normalization rejects executable remote and metadata content", () => {
  const safeSvg = '<svg xmlns="http://www.w3.org/2000/svg"><g><rect/></g></svg>';
  assert.match(normalizeSvg(safeSvg, diagram), /^<svg .*role="img"/);
  for (const unsafe of [
    "<script>alert(1)</script>",
    "<foreignObject><p>HTML</p></foreignObject>",
    '<image href="https://remote.invalid/a.png"/>',
    '<rect onload="alert(1)"/>',
    '<a href="#target"><text>link</text></a>',
    "<metadata>generator details</metadata>",
    "<style>@font-face{src:url(https://remote.invalid/font)}</style>",
    '<text>/Users/example/private.txt</text>',
    "<animate attributeName=\"x\"/>",
  ]) {
    assert.throws(
      () => normalizeSvg(safeSvg.replace("</svg>", `${unsafe}</svg>`), diagram),
      /forbidden content/,
    );
  }
  assert.throws(
    () => normalizeSvg(`<!DOCTYPE svg>${safeSvg}`, diagram),
    /does not start with svg/,
  );
});
