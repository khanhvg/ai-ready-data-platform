export function derivePortalRoutes(catalog) {
  const root = Object.freeze({
    kind: 'catalog',
    path: '/',
    navigation: Object.freeze([{ path: '/', label: 'Cổng học tập' }])
  });
  if (!catalog.semanticReady) return Object.freeze([root]);
  return Object.freeze([root]);
}

export function resolvePortalRoute(pathname, routes) {
  const route = routes.find((candidate) => candidate.path === pathname);
  return route ?? routes[0];
}
