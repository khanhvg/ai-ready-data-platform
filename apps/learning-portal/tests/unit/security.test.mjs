import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";

const appRoot = path.resolve(import.meta.dirname, "../..");

test("PTP-RED-A-012/022 source exposes no runner, mutation, storage, or unsafe injection", () => {
  const sourceFiles = fs.readdirSync(path.join(appRoot, "src"), { recursive: true }).filter((name) => /\.(mjs|jsx|css)$/.test(name));
  const authored = sourceFiles.map((name) => fs.readFileSync(path.join(appRoot, "src", name), "utf8")).join("\n");
  assert.doesNotMatch(authored, /dangerouslySetInnerHTML|localStorage|sessionStorage|indexedDB|serviceWorker|child_process|exec\(|spawn\(|Issue\s*#?9/i);
  assert.doesNotMatch(authored, /https?:\/\//);
});

test("PTP-RED-A-016 styles must prove visible focus and 360px reflow", () => {
  const cssPath = path.join(appRoot, "src/styles.css");
  const css = fs.existsSync(cssPath) ? fs.readFileSync(cssPath, "utf8") : "";
  assert.match(css, /:focus-visible/, "visible keyboard focus behavior is absent");
  assert.match(css, /max-width:\s*100%|overflow-wrap/, "narrow overflow protection is absent");
  assert.match(css, /prefers-reduced-motion/, "reduced-motion behavior is absent");
});
