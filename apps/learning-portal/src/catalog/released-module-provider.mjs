export function createReleasedModuleProvider(adapter) {
  if (!adapter || typeof adapter.readRegistry !== 'function') {
    throw new TypeError('A callable learning adapter is required');
  }
  return Object.freeze({
    readRegistry() {
      const registry = adapter.readRegistry();
      if (
        registry?.authorityKind !== 'released' ||
        registry?.registryType !== 'ReleasedPortalDescriptorRegistry'
      ) {
        throw new Error('PORTAL_DESCRIPTOR_AUTHORITY_FORBIDDEN');
      }
      return registry;
    }
  });
}
