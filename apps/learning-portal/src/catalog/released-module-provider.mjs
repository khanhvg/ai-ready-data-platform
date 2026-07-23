export function createReleasedModuleProvider(adapter) {
  if (!adapter || typeof adapter.readRegistry !== 'function') {
    throw new TypeError('A callable learning adapter is required');
  }
  return Object.freeze({
    readRegistry() {
      return adapter.readRegistry();
    }
  });
}
