export function createSafeViewModel(route, catalog) {
  return Object.freeze({
    routePath: route.path,
    heading: 'Cổng học tập',
    message: catalog.semanticReady
      ? 'Nội dung đã được xác thực.'
      : 'Nội dung phát hành chưa được nạp.',
    semanticReady: catalog.semanticReady,
    navigation: Object.freeze(
      route.navigation.map((item) => Object.freeze({ path: item.path, label: item.label }))
    )
  });
}
