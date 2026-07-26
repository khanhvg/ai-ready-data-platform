import { loadReleasedLearning } from "../contracts/released-learning-adapter.mjs";
import { createSafeViewModel } from "../contracts/safe-view-model.mjs";

export async function provideReleasedModules(options) {
  const model = createSafeViewModel(await loadReleasedLearning(options));
  const lesson = Object.freeze({ id: model.lesson.id, title: model.lesson.title, summary: model.lesson.summary, adapterId: "promotion-trust", steps: model.lesson.steps, model });
  return [Object.freeze({ title: "Lát cắt học tập tĩnh", description: "Một lát cắt trình bày, không phải toàn bộ sản phẩm học tập.", lessons: Object.freeze([lesson]) })];
}
