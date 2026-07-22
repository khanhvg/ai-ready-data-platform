import { loadReleasedLearning } from "../contracts/released-learning-adapter.mjs";
import { createSafeViewModel } from "../contracts/safe-view-model.mjs";

export async function provideReleasedModules(options) {
  const model = createSafeViewModel(await loadReleasedLearning(options));
  return [Object.freeze({ title: "Lát cắt học tập tĩnh", description: "Một lát cắt trình bày, không phải toàn bộ sản phẩm học tập.", lessons: Object.freeze([model.lesson]), model })];
}
