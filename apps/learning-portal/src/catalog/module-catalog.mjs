const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const MODULE_KEYS = new Set(["title", "description", "lessons"]);
const LESSON_KEYS = new Set(["id", "title", "summary", "adapterId", "steps", "model"]);
const STEP_KEYS = new Set(["id", "order", "label"]);
const ADAPTERS = new Set(["promotion-trust"]);

const plain = (value) => value !== null && typeof value === "object" && !Array.isArray(value) && Object.getPrototypeOf(value) === Object.prototype;
function closed(value, keys, code) {
  if (!plain(value)) throw new Error("CATALOG_DESCRIPTOR_INVALID");
  if (Object.keys(value).some((key) => !keys.has(key))) throw new Error(code);
}
function text(value) { return typeof value === "string" && value.length > 0 && value.length <= 256; }
function safeId(value) { if (!text(value) || !ID.test(value)) throw new Error("CATALOG_ID_UNSAFE"); return value; }

function normalizeStep(step, lessonId, index) {
  closed(step, STEP_KEYS, "CATALOG_DESCRIPTOR_UNKNOWN_FIELD");
  const id = safeId(step.id);
  if (step.order !== undefined && step.order !== index + 1) throw new Error("CATALOG_STEP_ORDER_INVALID");
  if (step.label !== undefined && !text(step.label)) throw new Error("CATALOG_DESCRIPTOR_INVALID");
  return Object.freeze({ id, order: index + 1, label: step.label ?? null, path: `/lesson/${lessonId}/step/${id}` });
}

function normalizeLesson(lesson) {
  closed(lesson, LESSON_KEYS, "CATALOG_DESCRIPTOR_UNKNOWN_FIELD");
  const id = safeId(lesson.id);
  if (![lesson.title, lesson.summary].every(text) || !plain(lesson.model) || !plain(lesson.model.lesson) || !Array.isArray(lesson.model.grains)) throw new Error("CATALOG_DESCRIPTOR_INVALID");
  if (!ADAPTERS.has(lesson.adapterId)) throw new Error("CATALOG_ADAPTER_UNKNOWN");
  if (!Array.isArray(lesson.steps) || lesson.steps.length < 1 || lesson.steps.length > 32) throw new Error("CATALOG_DESCRIPTOR_INVALID");
  const steps = lesson.steps.map((step, index) => normalizeStep(step, id, index));
  if (new Set(steps.map((step) => step.id)).size !== steps.length) throw new Error("DUPLICATE_RELEASED_STEP");
  return Object.freeze({ id, title: lesson.title, summary: lesson.summary, adapterId: lesson.adapterId, path: `/lesson/${id}`, steps: Object.freeze(steps), model: lesson.model });
}

export function createModuleCatalog(modules = []) {
  if (!Array.isArray(modules) || modules.length < 1 || modules.length > 32) throw new Error("CATALOG_DESCRIPTOR_INVALID");
  const suppliedIds = modules.flatMap((module) => plain(module) && Array.isArray(module.lessons) ? module.lessons.filter(plain).map((lesson) => lesson.id).filter((id) => typeof id === "string") : []);
  if (new Set(suppliedIds).size !== suppliedIds.length) throw new Error("DUPLICATE_RELEASED_LESSON");
  const normalized = modules.map((module) => {
    closed(module, MODULE_KEYS, "CATALOG_DESCRIPTOR_UNKNOWN_FIELD");
    if (!text(module.title) || !text(module.description) || !Array.isArray(module.lessons) || module.lessons.length < 1) throw new Error("CATALOG_DESCRIPTOR_INVALID");
    return Object.freeze({ title: module.title, description: module.description, lessons: Object.freeze(module.lessons.map(normalizeLesson)) });
  });
  const lessons = normalized.flatMap((module) => module.lessons);
  if (new Set(lessons.map((lesson) => lesson.id)).size !== lessons.length) throw new Error("DUPLICATE_RELEASED_LESSON");
  return Object.freeze({ title: "Danh mục học tập", modules: Object.freeze(normalized) });
}

export function findLesson(catalog, lessonId) {
  return catalog.modules.flatMap((module) => module.lessons).find((lesson) => lesson.id === lessonId) ?? null;
}
