export function createModuleCatalog(modules = []) {
  const ids = modules.flatMap((module) => module.lessons.map((lesson) => lesson.id));
  if (new Set(ids).size !== ids.length) throw new Error("DUPLICATE_RELEASED_LESSON");
  return Object.freeze({ title: "Danh mục học tập", modules: Object.freeze([...modules]) });
}
