export const PREVIEW_NOTICE = 'SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE';
export const FIXTURE_KIND = 'synthetic-preview';
export const FIXTURE_DIGEST = 'sha256:572c052ff546d19dab35ef988bba8da7ecc70b808c7c91caeea7fd453703c9de';

export const ALLOWED_STATES = new Set([
  'not-started',
  'exploring',
  'controlled-failure-shown',
  'diagnosing',
  'reset-demonstrated',
  'fixture-verified',
  'evidence-reviewed',
  'reflection-open',
]);
const HINT_LEVELS = new Set(['orient', 'connect', 'explain']);
const PASSIVE_EVENTS = new Set([
  'scroll',
  'hover',
  'animation-end',
  'elapsed-time',
  'card-visited',
  'focus-moved',
  'intersection',
]);
const COMMITTED_ACTIONS = new Set([
  null, 'hint-explicit', 'next-explicit', 'navigate-explicit', 'previous-explicit', 'frame-explicit',
  'controlled-failure-explicit', 'diagnose-explicit', 'alternative-explicit', 'reset-explicit',
  'verify-fixture-explicit', 'review-evidence-explicit',
]);

const baseFields = () => ({
  attemptId: 'preview-attempt-synthetic-v1',
  fixtureKind: FIXTURE_KIND,
  fixtureDigest: FIXTURE_DIGEST,
  state: 'not-started',
  currentAct: 1,
  committedAct: 1,
  transientDraft: '',
  transientPolicy: 'discard-on-restore',
  hintLevel: 'orient',
  failureClass: null,
  resetAuditCount: 0,
  fixtureVerifyStatus: 'not-verified',
  evidenceReviewStatus: 'not-reviewed',
  evidenceCount: 0,
  lastExplicitAction: null,
  historyMode: 'replace',
  repositoryMutation: false,
  conclusion: 'insufficient evidence',
});

function persistedProjection(state) {
  return {
    attemptId: state.attemptId,
    fixtureKind: state.fixtureKind,
    fixtureDigest: state.fixtureDigest,
    state: state.state,
    committedAct: state.committedAct,
    hintLevel: state.hintLevel,
    failureClass: state.failureClass,
    resetAuditCount: state.resetAuditCount,
    fixtureVerifyStatus: state.fixtureVerifyStatus,
    evidenceReviewStatus: state.evidenceReviewStatus,
    evidenceCount: state.evidenceCount,
    lastExplicitAction: state.lastExplicitAction,
  };
}

function withProjection(state) {
  return { ...state, persistedProjection: persistedProjection(state) };
}

export function createBaselineState() {
  return withProjection(baseFields());
}

function commit(state, action, changes) {
  return withProjection({
    ...state,
    ...changes,
    transientDraft: '',
    lastExplicitAction: action,
    historyMode: action === 'reset-explicit' ? 'replace' : 'push',
    repositoryMutation: false,
  });
}

export function reducePreviewState(current, event = {}) {
  const state = isUsableState(current) ? current : createBaselineState();
  const type = typeof event.type === 'string' ? event.type : '';

  if (PASSIVE_EVENTS.has(type) || type === '') return state;
  if (type === 'draft-changed') {
    return { ...state, transientDraft: typeof event.value === 'string' ? event.value : '' };
  }
  if (type === 'hint-explicit' && HINT_LEVELS.has(event.value)) {
    return commit(state, type, { hintLevel: event.value });
  }
  if (type === 'next-explicit') {
    const act = Math.min(10, state.committedAct + 1);
    return commit(state, type, { state: 'exploring', currentAct: act, committedAct: act });
  }
  if (type === 'navigate-explicit' && integerInRange(event.act, 1, 10)) {
    return commit(state, type, {
      state: event.act === 1 ? 'not-started' : 'exploring',
      currentAct: event.act,
      committedAct: event.act,
    });
  }
  if (type === 'previous-explicit') {
    const act = Math.max(1, state.committedAct - 1);
    return commit(state, type, { state: act === 1 ? 'not-started' : 'exploring', currentAct: act, committedAct: act });
  }
  if (type === 'frame-explicit') {
    return commit(state, type, { state: 'exploring', currentAct: 1, committedAct: 1 });
  }
  if (type === 'controlled-failure-explicit') {
    return commit(state, type, {
      state: 'controlled-failure-shown',
      currentAct: 4,
      committedAct: 4,
      failureClass: 'controlled-analytical',
    });
  }
  if (type === 'diagnose-explicit') {
    return commit(state, type, { state: 'diagnosing', currentAct: 5, committedAct: 5 });
  }
  if (type === 'alternative-explicit') {
    return commit(state, type, { state: 'exploring', currentAct: 6, committedAct: 6 });
  }
  if (type === 'reset-explicit') {
    const baseline = baseFields();
    return commit({ ...baseline, resetAuditCount: state.resetAuditCount + 1 }, type, {
      state: 'reset-demonstrated',
      currentAct: 7,
      committedAct: 7,
    });
  }
  if (type === 'verify-fixture-explicit') {
    return commit(state, type, {
      state: 'fixture-verified',
      currentAct: 9,
      committedAct: 9,
      fixtureVerifyStatus: 'verified-synthetic-only',
      evidenceCount: 1,
    });
  }
  if (type === 'review-evidence-explicit') {
    if (state.fixtureVerifyStatus !== 'verified-synthetic-only') return state;
    return commit(state, type, {
      state: 'evidence-reviewed',
      currentAct: 9,
      committedAct: 9,
      evidenceReviewStatus: 'reviewed-synthetic-only',
      evidenceCount: Math.max(2, state.evidenceCount),
    });
  }
  if (type === 'reflection-open-explicit') {
    return state;
  }
  return state;
}

export function restoreCommittedState(projection, fixtureDigest = FIXTURE_DIGEST) {
  if (!isPlainObject(projection)
    || fixtureDigest !== FIXTURE_DIGEST
    || projection.fixtureDigest !== fixtureDigest
    || projection.fixtureKind !== FIXTURE_KIND
    || projection.attemptId !== 'preview-attempt-synthetic-v1') {
    return createBaselineState();
  }
  if (!integerInRange(projection.committedAct, 1, 10)) {
    return createBaselineState();
  }
  const baseline = baseFields();
  const persistedFields = new Set([
    'attemptId', 'fixtureKind', 'fixtureDigest', 'state', 'committedAct',
    'hintLevel', 'failureClass', 'resetAuditCount', 'fixtureVerifyStatus',
    'evidenceReviewStatus', 'evidenceCount', 'lastExplicitAction',
  ]);
  const safeStateReachable = projection.state === 'exploring'
    || (projection.state === 'not-started' && projection.committedAct === 1)
    || (projection.state === 'controlled-failure-shown'
      && projection.committedAct === 4 && projection.failureClass === 'controlled-analytical')
    || (projection.state === 'diagnosing'
      && projection.committedAct === 5 && projection.failureClass === 'controlled-analytical')
    || (projection.state === 'reset-demonstrated'
      && projection.committedAct === 7 && projection.failureClass === null)
    || (projection.state === 'fixture-verified'
      && projection.committedAct === 9
      && projection.fixtureVerifyStatus === 'verified-synthetic-only')
    || (projection.state === 'evidence-reviewed'
      && projection.committedAct === 9
      && projection.evidenceReviewStatus === 'reviewed-synthetic-only');
  const safeEvidence = (projection.fixtureVerifyStatus === 'not-verified'
      && projection.evidenceReviewStatus === 'not-reviewed'
      && projection.evidenceCount === 0)
    || (projection.fixtureVerifyStatus === 'verified-synthetic-only'
      && projection.evidenceReviewStatus === 'not-reviewed'
      && projection.evidenceCount === 1)
    || (projection.fixtureVerifyStatus === 'verified-synthetic-only'
      && projection.evidenceReviewStatus === 'reviewed-synthetic-only'
      && projection.evidenceCount === 2);
  const canonical = Object.keys(projection).length === persistedFields.size
    && Object.keys(projection).every((field) => persistedFields.has(field))
    && ALLOWED_STATES.has(projection.state)
    && safeStateReachable
    && HINT_LEVELS.has(projection.hintLevel)
    && (projection.failureClass === null || projection.failureClass === 'controlled-analytical')
    && nonNegativeInteger(projection.resetAuditCount)
    && safeEvidence
    && COMMITTED_ACTIONS.has(projection.lastExplicitAction);
  const restored = {
    ...baseline,
    ...(canonical ? {
      state: projection.state,
      hintLevel: projection.hintLevel,
      failureClass: projection.failureClass,
      resetAuditCount: projection.resetAuditCount,
      fixtureVerifyStatus: projection.fixtureVerifyStatus,
      evidenceReviewStatus: projection.evidenceReviewStatus,
      evidenceCount: projection.evidenceCount,
      lastExplicitAction: projection.lastExplicitAction,
    } : { state: projection.committedAct === 1 ? 'not-started' : 'exploring' }),
    currentAct: projection.committedAct,
    committedAct: projection.committedAct,
    historyMode: 'replace',
  };
  return withProjection(restored);
}

export function resettableDigest(state) {
  const resettable = {
    fixtureKind: state.fixtureKind,
    fixtureDigest: state.fixtureDigest,
    transientDraft: state.transientDraft,
    transientPolicy: state.transientPolicy,
    hintLevel: state.hintLevel,
    failureClass: state.failureClass,
    fixtureVerifyStatus: state.fixtureVerifyStatus,
    evidenceReviewStatus: state.evidenceReviewStatus,
    evidenceCount: state.evidenceCount,
    repositoryMutation: state.repositoryMutation,
    conclusion: state.conclusion,
  };
  return stableDigest(resettable);
}

export function exportEvidence(state) {
  const safe = isUsableState(state) ? state : createBaselineState();
  return {
    notice: PREVIEW_NOTICE,
    fixtureKind: FIXTURE_KIND,
    fixtureDigest: FIXTURE_DIGEST,
    conclusion: 'insufficient evidence',
    decisionGrade: false,
    numericScore: null,
    records: [
      {
        id: 'preview-state',
        locator: 'common/state/preview-state-vectors.json',
        result: safe.fixtureVerifyStatus,
      },
      {
        id: 'four-grain-fixture',
        locator: 'common/fixtures/synthetic-promotion-trust-v1.json',
        result: safe.evidenceReviewStatus,
      },
    ],
  };
}

export const TRUSTED_FIXTURE_PROJECTION = Object.freeze({
  fixtureKind: FIXTURE_KIND,
  fixtureDigest: FIXTURE_DIGEST,
  cardGrains: Object.freeze([
    'promotion:promo_name,channel',
    'fulfillment:carrier,region',
    'returns:return_reason,category,region',
    'global-dq:scenario,count',
  ]),
  conclusion: 'insufficient evidence',
});

export function verifyTrustedFixtureProjection(projection) {
  if (!isPlainObject(projection)) return { ok: false, code: 'FIXTURE_UNAVAILABLE' };
  if (projection.fixtureDigest !== FIXTURE_DIGEST || projection.fixtureKind !== FIXTURE_KIND) {
    return { ok: false, code: 'FIXTURE_DIGEST_MISMATCH' };
  }
  const expectedGrains = TRUSTED_FIXTURE_PROJECTION.cardGrains;
  if (!Array.isArray(projection.cardGrains)
    || JSON.stringify(projection.cardGrains) !== JSON.stringify(expectedGrains)
    || projection.conclusion !== 'insufficient evidence') {
    return { ok: false, code: 'STATIC_ASSET_UNAVAILABLE' };
  }
  return { ok: true, code: 'FIXTURE_VERIFIED', fixtureDigest: FIXTURE_DIGEST };
}

function stableDigest(value) {
  const text = JSON.stringify(value, Object.keys(value).sort());
  let hash = 2166136261;
  for (let index = 0; index < text.length; index += 1) {
    hash ^= text.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return `resettable-v1-${(hash >>> 0).toString(16).padStart(8, '0')}`;
}

function isUsableState(value) {
  return isPlainObject(value) && value.fixtureKind === FIXTURE_KIND && value.fixtureDigest === FIXTURE_DIGEST && ALLOWED_STATES.has(value.state) && integerInRange(value.committedAct, 1, 10);
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value) && Object.getPrototypeOf(value) === Object.prototype;
}

function integerInRange(value, minimum, maximum) {
  return Number.isInteger(value) && value >= minimum && value <= maximum;
}

function nonNegativeInteger(value) {
  return Number.isInteger(value) && value >= 0;
}

function escapePointer(value) {
  return value.replaceAll('~', '~0').replaceAll('/', '~1');
}

function invalid(path, message) {
  return { ok: false, errors: [{ path, message }] };
}

if (typeof document !== 'undefined') {
  const one = (selector) => document.querySelector(selector);
  const all = (selector) => [...document.querySelectorAll(selector)];

  function actFromLocation() {
    const match = location.hash.match(/^#act-(10|[1-9])$/);
    return match ? Number(match[1]) : 1;
  }

  let state = restoreCommittedState(history.state?.preview);
  if (!history.state?.preview) {
    state = reducePreviewState(createBaselineState(), { type: 'navigate-explicit', act: actFromLocation() });
  }
  let pendingNativeNavigation = false;

  function render() {
    document.documentElement.dataset.jsReady = 'true';
    all('[data-act]').forEach((section) => { section.dataset.active = String(Number(section.dataset.act) === state.committedAct); });
    one('[data-rail-act]').textContent = `${String(state.committedAct).padStart(2, '0')} / 10`;
    one('[data-rail-state]').textContent = state.state;
    one('[data-rail-failure]').textContent = state.failureClass ?? 'chưa ghi nhận';
    one('[data-rail-action]').textContent = state.lastExplicitAction ?? 'chưa có';
    one('[data-rail-reset]').textContent = String(state.resetAuditCount);
    one('[data-rail-verify]').textContent = state.fixtureVerifyStatus;
    one('[data-rail-evidence]').textContent = String(state.evidenceCount);
    one('[data-reset-status]').textContent = state.resetAuditCount === 0
      ? 'Chưa yêu cầu đặt lại · bộ đếm 0.'
      : `Đã về cùng baseline digest · bộ đếm ${state.resetAuditCount}.`;
  }

  function projection() {
    return { preview: state.persistedProjection };
  }

  function commit(action, mode = 'push') {
    state = reducePreviewState(state, action);
    const url = `#act-${state.committedAct}`;
    if (mode === 'replace') history.replaceState(projection(), '', url);
    else history.pushState(projection(), '', url);
    render();
  }

  all('[data-nav]').forEach((link) => {
    link.addEventListener('click', () => {
      const act = Number(link.hash.replace('#act-', ''));
      if (!Number.isInteger(act)) return;
      state = reducePreviewState(state, { type: 'navigate-explicit', act });
      pendingNativeNavigation = true;
      render();
    });
  });

  all('[data-transient]').forEach((control) => {
    control.addEventListener('input', () => {
      state = reducePreviewState(state, { type: 'draft-changed', value: control.value });
    });
  });

  one('[data-action="simulate"]').addEventListener('click', () => {
    one('[data-simulation-status]').textContent = 'Mô phỏng đã phát lại: generate → load → transform → export; không thay đổi tài sản.';
  });

  one('[data-action="controlled-failure-explicit"]').addEventListener('click', () => commit({ type: 'controlled-failure-explicit' }));
  one('[data-action="diagnose-explicit"]').addEventListener('click', () => commit({ type: 'diagnose-explicit' }));
  one('[data-action="reset-explicit"]').addEventListener('click', () => {
    all('[data-transient]').forEach((control) => {
      if (control instanceof HTMLInputElement) control.checked = false;
      else control.value = '';
    });
    commit({ type: 'reset-explicit' }, 'replace');
  });
  one('[data-action="alternative-explicit"]').addEventListener('click', () => {
    const selected = one('input[name="alternative"]:checked');
    const selectedValue = selected?.value;
    commit({ type: 'alternative-explicit' });
    if (selected) selected.checked = false;
    one('[data-alternative-status]').textContent = selectedValue === 'insufficient evidence'
      ? 'Đã ghi hồi 6; lựa chọn phù hợp nhưng không được lưu.'
      : selectedValue
        ? 'Đã ghi hồi 6; lựa chọn không được lưu và kết quả fixture không đổi.'
        : 'Đã ghi hồi 6; không có lựa chọn nào được lưu và kết quả fixture không đổi.';
  });
  one('[data-action="verify-fixture-explicit"]').addEventListener('click', () => {
    const verified = verifyTrustedFixtureProjection(TRUSTED_FIXTURE_PROJECTION);
    if (!verified.ok) {
      state = { ...state, failureClass: `environmental:${verified.code}` };
      one('[data-verify-result] span').textContent = `Dừng kiểm chứng · ${verified.code}`;
      render();
      return;
    }
    commit({ type: 'verify-fixture-explicit' });
    one('[data-verify-result] span').textContent = 'Fixture tổng hợp hợp lệ · bốn grain vẫn độc lập';
  });
  one('[data-action="review-evidence-explicit"]').addEventListener('click', () => {
    commit({ type: 'review-evidence-explicit' });
    one('[data-evidence-json]').textContent = JSON.stringify(exportEvidence(state), null, 2);
  });
  one('[data-action="export-evidence-explicit"]').addEventListener('click', () => {
    const content = `${PREVIEW_NOTICE}\n${JSON.stringify(exportEvidence(state), null, 2)}\n`;
    const anchor = document.createElement('a');
    anchor.href = URL.createObjectURL(new Blob([content], { type: 'application/json' }));
    anchor.download = 'synthetic-preview-evidence.json';
    anchor.click();
    URL.revokeObjectURL(anchor.href);
  });
  one('[data-action="reflection-open-explicit"]').addEventListener('click', () => {
    state = reducePreviewState(state, { type: 'reflection-open-explicit' });
    one('[data-reflection]').focus();
  });
  one('[data-action="clear-reflection"]').addEventListener('click', () => {
    one('[data-reflection]').value = '';
    state = reducePreviewState(state, { type: 'draft-changed', value: '' });
  });

  addEventListener('hashchange', () => {
    if (!pendingNativeNavigation) return;
    pendingNativeNavigation = false;
    history.replaceState(projection(), '', location.hash);
  });

  addEventListener('popstate', (event) => {
    state = restoreCommittedState(event.state?.preview ?? {
      attemptId: 'preview-attempt-synthetic-v1',
      fixtureKind: TRUSTED_FIXTURE_PROJECTION.fixtureKind,
      fixtureDigest: TRUSTED_FIXTURE_PROJECTION.fixtureDigest,
      committedAct: actFromLocation(),
    });
    render();
  });

  history.replaceState(projection(), '', `#act-${state.committedAct}`);
  render();

}
