import assert from 'node:assert/strict';
import test from 'node:test';

async function model() {
  return import(new URL('../state/preview-state.mjs', import.meta.url));
}

test('WEB-STATE-001 staticLogical commits only explicit navigation and restores committed history/reload state', async () => {
  const { createBaselineState, reducePreviewState, restoreCommittedState } = await model();
  const baseline = createBaselineState();
  const drafted = reducePreviewState(baseline, { type: 'draft-changed', value: 'temporary reasoning' });
  assert.equal(drafted.committedAct, baseline.committedAct);
  const committed = reducePreviewState(drafted, { type: 'next-explicit' });
  assert.equal(committed.committedAct, baseline.committedAct + 1);
  assert.equal(committed.lastExplicitAction, 'next-explicit');
  const restored = restoreCommittedState(committed.persistedProjection, committed.fixtureDigest);
  assert.equal(restored.committedAct, committed.committedAct);
  assert.notEqual(restored.transientDraft, 'temporary reasoning');

  const controlled = reducePreviewState(committed, { type: 'controlled-failure-explicit' });
  const controlledRestored = restoreCommittedState(controlled.persistedProjection, controlled.fixtureDigest);
  assert.equal(controlledRestored.state, controlled.state);
  assert.equal(controlledRestored.failureClass, controlled.failureClass);

  const reset = reducePreviewState(controlled, { type: 'reset-explicit' });
  const verified = reducePreviewState(reset, { type: 'verify-fixture-explicit' });
  const reviewed = reducePreviewState(verified, { type: 'review-evidence-explicit' });
  const reviewedRestored = restoreCommittedState(reviewed.persistedProjection, reviewed.fixtureDigest);
  for (const field of [
    'state', 'committedAct', 'hintLevel', 'resetAuditCount', 'fixtureVerifyStatus',
    'evidenceReviewStatus', 'evidenceCount', 'lastExplicitAction',
  ]) {
    assert.equal(reviewedRestored[field], reviewed[field], field);
  }
  assert.equal(reviewedRestored.transientDraft, '');

  const diagnosed = reducePreviewState(controlled, { type: 'diagnose-explicit' });
  const alternativeDraft = reducePreviewState(diagnosed, { type: 'draft-changed', value: 'headline-sufficient' });
  const alternative = reducePreviewState(alternativeDraft, { type: 'alternative-explicit' });

  assert.equal(alternative.state, 'exploring');
  assert.equal(alternative.currentAct, 6);
  assert.equal(alternative.committedAct, 6);
  assert.equal(alternative.lastExplicitAction, 'alternative-explicit');
  assert.equal(alternative.transientDraft, '');
  assert.equal(alternative.conclusion, 'insufficient evidence');
  assert.equal(alternative.fixtureVerifyStatus, 'not-verified');
  assert.equal(alternative.evidenceReviewStatus, 'not-reviewed');
  assert.equal(alternative.evidenceCount, 0);
  assert.equal(Object.hasOwn(alternative, 'selectedAlternative'), false);
  assert.equal(Object.hasOwn(alternative.persistedProjection, 'selectedAlternative'), false);

  const alternativeRestored = restoreCommittedState(alternative.persistedProjection, alternative.fixtureDigest);
  assert.equal(alternativeRestored.state, 'exploring');
  assert.equal(alternativeRestored.committedAct, 6);
  assert.equal(alternativeRestored.lastExplicitAction, 'alternative-explicit');
  assert.equal(alternativeRestored.transientDraft, '');
  assert.equal(Object.hasOwn(alternativeRestored, 'selectedAlternative'), false);
});

test('WEB-NOSCROLL-001 staticLogical ignores scroll, hover, motion, time, visitation and focus for commit/verify', async () => {
  const { createBaselineState, reducePreviewState, resettableDigest } = await model();
  const passiveEvents = ['scroll', 'hover', 'animation-end', 'elapsed-time', 'card-visited', 'focus-moved', 'intersection'];
  const baseline = createBaselineState();
  for (const type of passiveEvents) {
    const next = reducePreviewState(baseline, { type });
    assert.equal(next.committedAct, baseline.committedAct, type);
    assert.equal(next.fixtureVerifyStatus, baseline.fixtureVerifyStatus, type);
    assert.equal(next.evidenceCount, baseline.evidenceCount, type);
    assert.equal(resettableDigest(next), resettableDigest(baseline), type);
  }
});

test('WEB-STATE-001 untrusted history projection cannot author verifier, evidence, conclusion, mutation or extra fields', async () => {
  const { createBaselineState, reducePreviewState, restoreCommittedState } = await model();
  const baseline = createBaselineState();
  const hostile = {
    ...baseline.persistedProjection,
    state: 'fixture-verified',
    committedAct: 9,
    fixtureVerifyStatus: 'not-verified',
    evidenceReviewStatus: 'reviewed-synthetic-only',
    evidenceCount: 99,
    conclusion: 'promotion caused returns',
    repositoryMutation: true,
    numericScore: 100,
    completed: true,
  };
  const restored = restoreCommittedState(hostile, baseline.fixtureDigest);
  assert.equal(restored.committedAct, 9);
  assert.equal(restored.fixtureVerifyStatus, 'not-verified');
  assert.equal(restored.evidenceReviewStatus, 'not-reviewed');
  assert.equal(restored.evidenceCount, 0);
  assert.equal(restored.conclusion, 'insufficient evidence');
  assert.equal(restored.repositoryMutation, false);
  assert.equal(Object.hasOwn(restored, 'numericScore'), false);
  assert.equal(Object.hasOwn(restored, 'completed'), false);

  const reviewWithoutVerification = reducePreviewState(baseline, { type: 'review-evidence-explicit' });
  assert.equal(reviewWithoutVerification.evidenceReviewStatus, 'not-reviewed');
  assert.equal(reviewWithoutVerification.evidenceCount, 0);

  const internallyInvalidForgery = {
    attemptId: baseline.attemptId,
    fixtureKind: baseline.fixtureKind,
    fixtureDigest: baseline.fixtureDigest,
    state: 'evidence-reviewed',
    committedAct: 9,
    hintLevel: 'explain',
    failureClass: null,
    resetAuditCount: 0,
    fixtureVerifyStatus: 'not-verified',
    evidenceReviewStatus: 'reviewed-synthetic-only',
    evidenceCount: 2,
    lastExplicitAction: 'review-evidence-explicit',
  };
  const forged = restoreCommittedState(internallyInvalidForgery, baseline.fixtureDigest);
  assert.equal(forged.committedAct, 9);
  assert.equal(forged.fixtureVerifyStatus, 'not-verified');
  assert.equal(forged.evidenceReviewStatus, 'not-reviewed');
  assert.equal(forged.evidenceCount, 0);

  const impossibleCount = restoreCommittedState({
    ...baseline.persistedProjection,
    state: 'exploring',
    committedAct: 2,
    evidenceCount: 2,
    lastExplicitAction: 'next-explicit',
  }, baseline.fixtureDigest);
  assert.equal(impossibleCount.committedAct, 2);
  assert.equal(impossibleCount.fixtureVerifyStatus, 'not-verified');
  assert.equal(impossibleCount.evidenceReviewStatus, 'not-reviewed');
  assert.equal(impossibleCount.evidenceCount, 0);

  const impossibleVerifiedCount = restoreCommittedState({
    ...baseline.persistedProjection,
    state: 'fixture-verified',
    committedAct: 9,
    fixtureVerifyStatus: 'verified-synthetic-only',
    evidenceCount: 2,
    lastExplicitAction: 'verify-fixture-explicit',
  }, baseline.fixtureDigest);
  assert.equal(impossibleVerifiedCount.committedAct, 9);
  assert.equal(impossibleVerifiedCount.fixtureVerifyStatus, 'not-verified');
  assert.equal(impossibleVerifiedCount.evidenceReviewStatus, 'not-reviewed');
  assert.equal(impossibleVerifiedCount.evidenceCount, 0);
});

test('WEB-STATE-001 reflection, draft and visitation remain transient and never commit or verify', async () => {
  const { createBaselineState, reducePreviewState } = await model();
  const baseline = createBaselineState();
  for (const event of [
    { type: 'draft-changed', value: 'draft' },
    { type: 'reflection-open-explicit' },
    { type: 'card-visited' },
  ]) {
    const next = reducePreviewState(baseline, event);
    assert.equal(next.committedAct, baseline.committedAct, event.type);
    assert.equal(next.fixtureVerifyStatus, 'not-verified', event.type);
    assert.equal(next.evidenceReviewStatus, 'not-reviewed', event.type);
  }
});

test('WEB-FAIL-001 fixture verification maps unavailable, digest and asset failures without verified state', async () => {
  const { TRUSTED_FIXTURE_PROJECTION, verifyTrustedFixtureProjection } = await model();
  assert.deepEqual(verifyTrustedFixtureProjection(null), { ok: false, code: 'FIXTURE_UNAVAILABLE' });
  assert.deepEqual(
    verifyTrustedFixtureProjection({ ...TRUSTED_FIXTURE_PROJECTION, fixtureDigest: 'sha256:stale' }),
    { ok: false, code: 'FIXTURE_DIGEST_MISMATCH' },
  );
  assert.deepEqual(
    verifyTrustedFixtureProjection({ ...TRUSTED_FIXTURE_PROJECTION, cardGrains: [] }),
    { ok: false, code: 'STATIC_ASSET_UNAVAILABLE' },
  );
});
