import test from "node:test";
import assert from "node:assert/strict";
import { renderStaticDocument } from "../../src/render/static-document.mjs";

test("PTP-RED-A-014/021 static output carries facts, navigation, and non-claims", () => {
  const html = renderStaticDocument({ kind: "lesson", path: "/lesson/promotion-trust" });
  for (const fact of ["insufficient-evidence", "no-common-grain", "data-runner=\"unavailable\"", "Chưa phải sản phẩm học tập đầy đủ", "Bỏ qua đến nội dung chính"]) {
    assert.match(html, new RegExp(fact), `static renderer lacks ${fact}`);
  }
  assert.doesNotMatch(html, /<button|dangerouslySetInnerHTML|data-progress=\"enabled\"/);
});
