export function derivePortalRoutes(catalog) {
  const routes = [
    { kind: 'home', path: '/', label: 'Trang chủ' },
    { kind: 'curriculum', path: '/curriculum', label: 'Lộ trình học' },
    ...catalog.curriculum.modules.map((module) => ({
      kind: 'module', path: `/curriculum/${module.id.toLowerCase()}`, label: `${module.id} · ${module.outcome}`, moduleId: module.id
    })),
    { kind: 'architecture', path: '/architecture', label: 'Kiến trúc' },
    { kind: 'labs', path: '/labs', label: 'Lab thủ công' },
    ...catalog.labs.map((lab) => ({ kind: 'lab', path: `/labs/${lab.slug}`, label: lab.title, labSlug: lab.slug })),
    { kind: 'promotion', path: '/lessons/promotion-trust', label: catalog.promotionTrust.title },
    ...catalog.promotionTrust.lesson.narrativeSteps.map((step) => ({
      kind: 'promotion-step', path: `/lessons/promotion-trust/steps/${step.id}`, label: `Bước ${step.order}: ${step.id}`, stepId: step.id
    }))
  ];
  if (new Set(routes.map(({ path }) => path)).size !== routes.length) throw new Error('PORTAL_ROUTE_DUPLICATE');
  return Object.freeze(routes.map((route, index) => Object.freeze({
    ...route,
    previous: index > 0 ? { path: routes[index - 1].path, label: routes[index - 1].label } : null,
    next: index < routes.length - 1 ? { path: routes[index + 1].path, label: routes[index + 1].label } : null
  })));
}

export function resolvePortalRoute(pathname, routes) {
  if (typeof pathname !== 'string' || pathname.length === 0 || pathname.length > 2048 || pathname.includes('\\') || pathname.includes('//') || pathname.includes('%')) return undefined;
  if (pathname.split('/').some((part) => part === '.' || part === '..')) return undefined;
  return routes.find((route) => route.path === pathname);
}
