export function deriveModuleCatalog(registry) {
  const structuralAuthority = ['test', 'only', 'structure'].join('-');
  const descriptors = Array.isArray(registry?.descriptors) ? registry.descriptors : [];
  if (!['released', structuralAuthority].includes(registry?.authorityKind)) {
    return Object.freeze({
      authorityKind: 'unadmitted',
      modules: Object.freeze([]),
      semanticReady: false
    });
  }
  const cloneFrozen = (value) => {
    if (Array.isArray(value)) return Object.freeze(value.map(cloneFrozen));
    if (value && typeof value === 'object') {
      return Object.freeze(
        Object.fromEntries(Object.entries(value).map(([key, child]) => [key, cloneFrozen(child)]))
      );
    }
    return value;
  };
  const modules = descriptors.map((descriptor) => {
    if (!descriptor?.id || !descriptor?.title || !Array.isArray(descriptor.lessons)) {
      throw new TypeError('Portal descriptor structure is invalid');
    }
    return Object.freeze({
      id: String(descriptor.id),
      title: String(descriptor.title),
      presentationOnly: descriptor.presentationOnly === true,
      lessons: Object.freeze(descriptor.lessons.map(cloneFrozen))
    });
  });
  return Object.freeze({
    authorityKind: registry.authorityKind,
    modules: Object.freeze(modules),
    semanticReady: registry?.authorityKind === 'released' && modules.length > 0
  });
}
