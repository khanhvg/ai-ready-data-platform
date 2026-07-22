export function createModuleCatalog(modules = []) {
  return Object.freeze({ modules: [...modules] });
}
