export function createSafeViewModel(released) {
  return Object.freeze({ ...released, routes: [] });
}
