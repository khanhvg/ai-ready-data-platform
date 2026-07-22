import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

const EXPECTED = Object.freeze({
  binding: ["learning/bindings/vite/promotion-trust-v1.json", "03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0"],
  contractSet: ["learning/contracts/learning-contract-set-v1.json", "92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638"],
  manifest: ["learning/manifests/promotion-trust-v1.json", "553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac"],
  lesson: ["learning/lessons/promotion-trust/lesson-v1.json", "758c6fb1ad75b283c313536d61bee61655bba6d27a2e685825ca20a28c838675"],
  lab: ["learning/labs/promotion-trust/lab-v1.json", "89ece51f41a17821d3266d2ba1fb7680cb70b07c2e9c5566d473aac9978d42d8"],
  fixture: ["tests/fixtures/learning/promotion-trust/manifest.json", "0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341"],
  evidence: ["tests/fixtures/learning/promotion-trust/evidence-v1.json", "2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5"]
});

export const PROMOTION_TRUST_PRESENTATION = Object.freeze({
  stepLabels: Object.freeze({ frame: "Đặt câu hỏi", inspect: "Kiểm tra bằng chứng", run: "Hiểu lượt chạy", fail: "Đọc lỗi có kiểm soát", trace: "Truy vết giới hạn", decide: "Ra quyết định", reset: "Hiểu đặt lại", configure: "Cấu hình giả định", verify: "Hiểu xác minh", reflect: "Phản tư kiến trúc" }),
  boundarySteps: Object.freeze(["run", "reset", "configure", "verify"]),
});

function repoRoot() {
  return path.resolve(import.meta.dirname, "../../../..");
}

async function readExact(root, [relative, expectedHash]) {
  const absolute = path.resolve(root, relative);
  if (!absolute.startsWith(`${root}${path.sep}`)) throw new Error("RELEASE_PATH_FORBIDDEN");
  const stat = await fs.lstat(absolute);
  if (!stat.isFile() || stat.isSymbolicLink() || stat.nlink !== 1) throw new Error("RELEASE_FILE_TYPE_FORBIDDEN");
  const bytes = await fs.readFile(absolute);
  const actualHash = crypto.createHash("sha256").update(bytes).digest("hex");
  if (actualHash !== expectedHash) throw new Error(`RELEASE_HASH_MISMATCH:${relative}`);
  return JSON.parse(bytes.toString("utf8"));
}

function splitDecision(value) {
  const [decision, reason, ...extra] = String(value).split("/");
  if (extra.length || decision !== "insufficient-evidence" || reason !== "no-common-grain") {
    throw new Error("RELEASE_DECISION_MISMATCH");
  }
  return Object.freeze({ value: decision, reason });
}

export async function loadReleasedLearning(options = {}) {
  const root = path.resolve(options.root ?? repoRoot());
  const [binding, contractSet, manifest, lesson, lab, fixture, evidence] = await Promise.all(
    Object.values(EXPECTED).map((entry) => readExact(root, entry))
  );
  if (binding.bindingId !== "promotion-trust-vite-binding-v1" || binding.schemaVersion !== binding.bindingId) throw new Error("BINDING_VERSION_MISMATCH");
  if (binding.stageA.contractSet.sha256 !== EXPECTED.contractSet[1] || binding.stageA.promotionManifest.sha256 !== EXPECTED.manifest[1]) throw new Error("BINDING_DEPENDENCY_HASH_MISMATCH");
  if (manifest.lesson.path !== EXPECTED.lesson[0] || manifest.lab.path !== EXPECTED.lab[0] || manifest.fixture.path !== EXPECTED.fixture[0]) throw new Error("BINDING_REFERENCE_MISMATCH");
  if (lesson.id !== "promotion-trust" || lab.lessonId !== lesson.id || fixture.fixtureId !== evidence.fixtureId) throw new Error("RELEASE_IDENTITY_MISMATCH");
  if (binding.grainBindings.length !== 4 || manifest.sources.length !== 4) throw new Error("BINDING_GRAIN_MISMATCH");
  const sourceByGrain = new Map(manifest.sources.map((source) => [source.grain, source]));
  const grains = binding.grainBindings.map((grain) => {
    const source = sourceByGrain.get(grain.stageAGrain);
    if (!source || JSON.stringify(source.keys) !== JSON.stringify(grain.stageAKeys)) throw new Error("BINDING_STAGE_A_KEY_MISMATCH");
    return Object.freeze({ id: grain.viteGrain, sourceGrain: grain.stageAGrain, keys: Object.freeze([...grain.viteKeys]), limitation: manifest.limitations.map((item) => item.statement).join("; ") });
  });
  const decision = splitDecision(manifest.decision);
  if (evidence.decision.value !== decision.value || evidence.decision.reason !== decision.reason) throw new Error("BINDING_FIXTURE_KEY_MISMATCH");
  return Object.freeze({
    bindingId: binding.bindingId,
    fixtureId: fixture.fixtureId,
    fixture: Object.freeze({ profile: fixture.profile, seed: fixture.seed }),
    grains: Object.freeze(grains),
    lesson: Object.freeze({
      id: lesson.id, version: lesson.version, title: lesson.title, summary: lesson.summary, level: lesson.level,
      stakeholderQuestion: lesson.stakeholder.decision, decisionQuestion: lesson.decision.question,
      decision, limitations: Object.freeze(manifest.limitations.map((item) => Object.freeze({ id: item.id, statement: item.statement }))),
      controlledFailure: Object.freeze({ code: lab.controlledFailure.expectedEvidence[0], symptom: lab.controlledFailure.symptom }),
      steps: Object.freeze(lesson.narrativeSteps.map((step) => Object.freeze({ id: step.id, order: step.order }))),
      reflection: lesson.reflection.prompt
    }),
    release: Object.freeze({ contractSetSha256: EXPECTED.contractSet[1], bindingSha256: EXPECTED.binding[1] })
  });
}
