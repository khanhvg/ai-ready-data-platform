export function deriveModuleCatalog(registry) {
  const descriptors = Array.isArray(registry?.descriptors) ? registry.descriptors : [];
  const modules = descriptors.map((descriptor) =>
    Object.freeze({
      id: String(descriptor.id),
      title: String(descriptor.title),
      lessons: Object.freeze([...(descriptor.lessons ?? [])])
    })
  );
  return Object.freeze({
    authorityKind: registry?.authorityKind ?? 'unadmitted',
    modules: Object.freeze(modules),
    semanticReady: registry?.authorityKind === 'released' && modules.length > 0
  });
}
