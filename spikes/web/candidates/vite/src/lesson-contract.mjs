const grains = [
  {
    id: 'promotion',
    value: 'promo_name × channel',
    limitation: 'Promotion aggregates cannot identify fulfillment, returns, or data-quality causes.',
  },
  {
    id: 'fulfillment',
    value: 'carrier × region_name',
    limitation: 'No shared key permits attribution to a promotion.',
  },
  {
    id: 'returns',
    value: 'reason × category_name × region_name',
    limitation: 'No shared key permits attribution to a promotion.',
  },
  {
    id: 'data-quality',
    value: 'scenario',
    limitation: 'Scenario evidence is independent and does not establish a cause.',
  },
].map(Object.freeze);

export const lessonContract = Object.freeze({
  language: 'vi',
  title: 'Can this promotion headline be trusted?',
  notice: 'TRACKED REAL FIXTURE — UNSCORED — CANNOT COMPLETE',
  grains: Object.freeze(grains),
  status: Object.freeze({
    baseline: 'Exploration is reversible and unverified.',
    failure: 'Controlled failure: no common grain; no answer, attribution, completion, or score saved.',
    reset: 'Reset: baseline restored; no answer, attribution, completion, or score persisted.',
  }),
  decision: Object.freeze({
    value: 'insufficient-evidence',
    reason: 'no-common-grain',
  }),
  relationships: Object.freeze([]),
  attribution: Object.freeze([]),
  noJsResetLimitation: 'Without JavaScript, reset is unavailable; all facts remain in their baseline state.',
  reflection: 'Reflection: What additional common-grain evidence would be needed before making a causal claim?',
});
