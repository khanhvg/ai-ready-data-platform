export function createSafeViewModel(route, catalog) {
  const modules = catalog.modules;
  const module = modules.find(({ id }) => id === route.moduleId) ?? modules[0];
  const lessons = module?.lessons ?? [];
  const lesson = lessons.find(({ id }) => id === route.lessonId) ?? lessons[0];
  const step = lesson?.narrativeSteps?.find(({ id }) => id === route.stepId);
  const sourceGrains = lesson?.sourceGrains ?? [];
  const factIds = Object.freeze([
    `decision-${lesson?.decision?.status ?? 'unavailable'}`,
    ...sourceGrains.map(({ id }) => `grain-${id}`),
    ...(lesson?.limitations ?? []).map(({ id }) => `limitation-${id}`)
  ]);
  const heading =
    route.kind === 'step'
      ? `Bước ${step?.order ?? ''}: ${step?.id ?? ''}`.trim()
      : route.kind === 'lesson'
        ? lesson?.titleVi ?? lesson?.title
        : route.kind === 'module'
          ? module?.title
          : 'Cổng học tập';
  return Object.freeze({
    routePath: route.path,
    routeKind: route.kind,
    heading,
    eyebrow: route.kind === 'catalog' ? 'Stage A · bản trình bày tĩnh' : 'Hành trình Stage A',
    message:
      'Trình chạy không khả dụng. Đây là nội dung trình bày chỉ đọc; không ghi nhận hoàn thành.',
    semanticReady: false,
    releasedContentReady: catalog.semanticReady,
    module,
    lesson,
    step,
    sourceGrains,
    factIds,
    navigation: Object.freeze(
      route.navigation.map((item) => Object.freeze({ path: item.path, label: item.label }))
    )
  });
}
