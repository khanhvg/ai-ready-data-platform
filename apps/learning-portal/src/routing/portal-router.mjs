export function derivePortalRoutes(catalog) {
  const root = Object.freeze({
    kind: 'catalog',
    path: '/',
    label: 'Danh mục học tập'
  });
  if (!Array.isArray(catalog.modules) || catalog.modules.length === 0) {
    const route = { ...root };
    Object.defineProperty(route, 'navigation', {
      value: Object.freeze([{ path: '/', label: root.label }]),
      enumerable: false
    });
    return Object.freeze([Object.freeze(route)]);
  }
  const lessonRoutes = catalog.modules.flatMap((module) =>
    module.lessons.flatMap((lesson) => [
      {
        kind: 'lesson',
        path: `/lessons/${encodeURIComponent(lesson.id)}`,
        label: lesson.titleVi ?? lesson.title,
        moduleId: module.id,
        lessonId: lesson.id
      },
      ...[...lesson.narrativeSteps]
        .sort((left, right) => left.order - right.order)
        .map((step) => ({
          kind: 'step',
          path: `/lessons/${encodeURIComponent(lesson.id)}/steps/${encodeURIComponent(step.id)}`,
          label: `Bước ${step.order}: ${step.id}`,
          moduleId: module.id,
          lessonId: lesson.id,
          stepId: step.id
        }))
    ])
  );
  const routes = [
    root,
    {
      kind: 'module',
      path: '/module',
      label: catalog.modules[0]?.title ?? 'Mô-đun học tập',
      moduleId: catalog.modules[0]?.id
    },
    ...lessonRoutes
  ];
  const navigation = Object.freeze(
    routes.map(({ path, label }) => Object.freeze({ path, label }))
  );
  return Object.freeze(
    routes.map((source) => {
      const route = { ...source };
      Object.defineProperty(route, 'navigation', { value: navigation, enumerable: false });
      return Object.freeze(route);
    })
  );
}

export function resolvePortalRoute(pathname, routes) {
  if (
    typeof pathname !== 'string' ||
    pathname.length === 0 ||
    pathname.length > 2048 ||
    pathname.includes('\\') ||
    pathname.includes('//')
  ) return undefined;
  let decoded;
  try {
    decoded = decodeURIComponent(pathname);
  } catch {
    return undefined;
  }
  if (
    decoded !== pathname ||
    decoded.split('/').some((segment) => segment === '.' || segment === '..')
  ) return undefined;
  return routes.find((candidate) => candidate.path === pathname);
}
