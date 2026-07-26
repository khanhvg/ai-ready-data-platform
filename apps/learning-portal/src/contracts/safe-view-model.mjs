export function createSafeViewModel(released) {
  if (!released || released.bindingId !== "promotion-trust-vite-binding-v1" || released.grains?.length !== 4) throw new Error("SAFE_VIEW_RELEASE_REQUIRED");
  return Object.freeze({ ...released, productScope: "static-portal-slice", runner: "unavailable", execution: "disabled", reset: "not-run", freshEvidence: false, progress: "disabled", completion: "disabled" });
}
