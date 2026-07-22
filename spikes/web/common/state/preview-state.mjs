import { ALLOWED_STATES, FIXTURE_DIGEST, FIXTURE_KIND, PREVIEW_NOTICE } from '../../preview/preview.mjs';
export {
  ALLOWED_STATES,
  createBaselineState,
  exportEvidence,
  FIXTURE_DIGEST,
  FIXTURE_KIND,
  PREVIEW_NOTICE,
  reducePreviewState,
  resettableDigest,
  restoreCommittedState,
  TRUSTED_FIXTURE_PROJECTION,
  verifyTrustedFixtureProjection,
} from '../../preview/preview.mjs';

export function validatePreviewDocument(document) {
  const errors = [];
  if (!isPlainObject(document)) return invalid('/', 'expected an object');
  rejectUnsafeValues(document, '', errors);
  if (Array.isArray(document.cards)) validateFixture(document, errors);
  else if (typeof document.state === 'string' && Number.isInteger(document.committedAct)) validateStateView(document, errors);
  else errors.push({ path: '/', message: 'unrecognized or incomplete preview document' });
  return { ok: errors.length === 0, errors };
}

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (isPlainObject(value)) {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

function validateFixture(document, errors) {
  const allowed = new Set(['fixtureKind', 'fixtureVersion', 'fixtureDigest', 'notice', 'normalizedAt', 'cards', 'verifier', 'evidence']);
  rejectUnknown(document, allowed, '', errors);
  for (const field of allowed) if (!Object.hasOwn(document, field)) errors.push({ path: `/${field}`, message: 'required field missing' });
  if (document.fixtureKind !== FIXTURE_KIND) errors.push({ path: '/fixtureKind', message: 'unexpected fixture kind' });
  if (document.fixtureVersion !== 1) errors.push({ path: '/fixtureVersion', message: 'unexpected fixture version' });
  if (document.fixtureDigest !== FIXTURE_DIGEST) errors.push({ path: '/fixtureDigest', message: 'unexpected fixture digest' });
  if (document.notice !== PREVIEW_NOTICE) errors.push({ path: '/notice', message: 'notice must be exact' });
  if (!Array.isArray(document.cards)) {
    errors.push({ path: '/cards', message: 'cards must be an array' });
    return;
  }
  if (document.cards.length !== 4) errors.push({ path: '/cards', message: 'exactly four cards required' });
  const expected = [
    ['promotion', ['promo_name', 'channel']],
    ['fulfillment', ['carrier', 'region']],
    ['returns', ['return_reason', 'category', 'region']],
    ['global-dq', ['scenario', 'count']],
  ];
  const cardFields = new Set(['id', 'grain', 'timeScope', 'filterScope', 'numerator', 'denominator', 'weighting', 'limitations', 'supports', 'cannotEstablish', 'facts']);
  const expectedFacts = [
    ['promo_name', 'channel'],
    ['carrier', 'region'],
    ['return_reason', 'category', 'region'],
    ['scenario', 'count'],
  ];
  document.cards.forEach((card, index) => {
    if (!isPlainObject(card)) return errors.push({ path: `/cards/${index}`, message: 'card must be an object' });
    rejectUnknown(card, cardFields, `/cards/${index}`, errors);
    const pair = expected[index];
    if (!pair || card.id !== pair[0] || JSON.stringify(card.grain) !== JSON.stringify(pair[1])) errors.push({ path: `/cards/${index}/grain`, message: 'card grain mismatch' });
    for (const field of ['timeScope', 'filterScope', 'numerator', 'denominator', 'weighting', 'limitations', 'supports', 'cannotEstablish']) {
      if (typeof card[field] !== 'string' || card[field].trim() === '') errors.push({ path: `/cards/${index}/${field}`, message: 'non-empty text required' });
    }
    if (!isPlainObject(card.facts) || !expectedFacts[index] || JSON.stringify(Object.keys(card.facts).sort()) !== JSON.stringify([...expectedFacts[index]].sort())) {
      errors.push({ path: `/cards/${index}/facts`, message: 'facts must match only the declared grain' });
    }
  });
  const verifierFields = new Set(['naiveHeadlineAccepted', 'conclusion', 'decisionGrade', 'numericScore', 'missingFutureData']);
  if (!isPlainObject(document.verifier)) {
    errors.push({ path: '/verifier', message: 'fixture-only verifier authority mismatch' });
  } else {
    rejectUnknown(document.verifier, verifierFields, '/verifier', errors);
    if (document.verifier.naiveHeadlineAccepted !== false || document.verifier.conclusion !== 'insufficient evidence' || document.verifier.decisionGrade !== false || document.verifier.numericScore !== null || typeof document.verifier.missingFutureData !== 'string') {
      errors.push({ path: '/verifier', message: 'fixture-only verifier authority mismatch' });
    }
  }
  const evidenceFields = new Set(['id', 'sourceMart', 'assertionResult', 'locator']);
  if (!Array.isArray(document.evidence) || document.evidence.length === 0) {
    errors.push({ path: '/evidence', message: 'evidence records required' });
  } else {
    document.evidence.forEach((record, index) => {
      if (!isPlainObject(record)) return errors.push({ path: `/evidence/${index}`, message: 'evidence record must be an object' });
      rejectUnknown(record, evidenceFields, `/evidence/${index}`, errors);
      for (const field of evidenceFields) if (typeof record[field] !== 'string' || record[field].trim() === '') errors.push({ path: `/evidence/${index}/${field}`, message: 'non-empty text required' });
      if (typeof record.locator === 'string' && (record.locator.startsWith('/') || record.locator.split('/').includes('..'))) errors.push({ path: `/evidence/${index}/locator`, message: 'locator must be relative and contained' });
    });
  }
}

function validateStateView(document, errors) {
  const allowed = new Set(['attemptId', 'fixtureKind', 'fixtureDigest', 'state', 'currentAct', 'committedAct', 'hintLevel', 'fixtureVerifyStatus', 'evidenceReviewStatus', 'resetAuditCount', 'repositoryMutation']);
  rejectUnknown(document, allowed, '', errors);
  for (const field of allowed) {
    if (!Object.hasOwn(document, field)) errors.push({ path: `/${field}`, message: 'required field missing' });
  }
  if (typeof document.attemptId !== 'string' || !/^preview-attempt-[a-z0-9-]+$/.test(document.attemptId)) errors.push({ path: '/attemptId', message: 'invalid attempt ID' });
  if (!ALLOWED_STATES.has(document.state)) errors.push({ path: '/state', message: 'state is not allowed' });
  if (document.fixtureKind !== FIXTURE_KIND) errors.push({ path: '/fixtureKind', message: 'unexpected fixture kind' });
  if (document.fixtureDigest !== FIXTURE_DIGEST) errors.push({ path: '/fixtureDigest', message: 'unexpected fixture digest' });
  if (!integerInRange(document.currentAct, 1, 10) || !integerInRange(document.committedAct, 1, 10)) errors.push({ path: '/committedAct', message: 'act out of range' });
  if (!['orient', 'connect', 'explain'].includes(document.hintLevel)) errors.push({ path: '/hintLevel', message: 'hint level is not allowed' });
  if (!['not-verified', 'verified-synthetic-only'].includes(document.fixtureVerifyStatus)) errors.push({ path: '/fixtureVerifyStatus', message: 'fixture status is not allowed' });
  if (!['not-reviewed', 'reviewed-synthetic-only'].includes(document.evidenceReviewStatus)) errors.push({ path: '/evidenceReviewStatus', message: 'evidence status is not allowed' });
  if (!nonNegativeInteger(document.resetAuditCount)) errors.push({ path: '/resetAuditCount', message: 'reset count must be non-negative' });
  if (document.repositoryMutation !== false) errors.push({ path: '/repositoryMutation', message: 'mutation authority denied' });
}

function rejectUnsafeValues(value, path, errors) {
  if (typeof value === 'string') {
    if (/<\/?script\b|<\w+[^>]+on\w+\s*=|\b(?:eval|import)\s*\(|https?:\/\/|\bBearer\s|TEST_SECRET|\/Users\/|(?:^|\/)\.\.(?:\/|$)/i.test(value)) {
      errors.push({ path: path || '/', message: 'unsafe content rejected' });
    }
    return;
  }
  if (Array.isArray(value)) return value.forEach((item, index) => rejectUnsafeValues(item, `${path}/${index}`, errors));
  if (isPlainObject(value)) {
    for (const [key, item] of Object.entries(value)) rejectUnsafeValues(item, `${path}/${escapePointer(key)}`, errors);
  }
}

function rejectUnknown(object, allowed, path, errors) {
  for (const key of Object.keys(object)) {
    if (!allowed.has(key)) errors.push({ path: `${path}/${escapePointer(key)}` || '/', message: 'unknown field' });
  }
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
