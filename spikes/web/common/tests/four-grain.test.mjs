import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const fixtureUrl = new URL('../fixtures/synthetic-promotion-trust-v1.json', import.meta.url);

async function fixture() {
  return JSON.parse(await readFile(fixtureUrl, 'utf8'));
}

const expected = [
  ['promotion', ['promo_name', 'channel']],
  ['fulfillment', ['carrier', 'region']],
  ['returns', ['return_reason', 'category', 'region']],
  ['global-dq', ['scenario', 'count']],
];

test('WEB-CONTRACT-002 staticLogical exposes exactly four independent grain-honest cards', async () => {
  const data = await fixture();
  assert.equal(data.cards.length, 4);
  assert.deepEqual(data.cards.map(({ id, grain }) => [id, grain]), expected);
  for (const card of data.cards) {
    for (const field of ['timeScope', 'filterScope', 'numerator', 'denominator', 'weighting', 'limitations', 'supports', 'cannotEstablish']) {
      assert.ok(card[field] && (typeof card[field] === 'string' || card[field].length > 0), `${card.id}.${field}`);
    }
  }
});

test('WEB-CONTRACT-003 staticLogical forbids cross-grain relationships, joins, composites and visual edges', async () => {
  const data = await fixture();
  const serialized = JSON.stringify(data);
  for (const forbiddenKey of ['relationships', 'joins', 'composite', 'edges', 'promotionAttribution']) {
    assert.equal(Object.hasOwn(data, forbiddenKey), false, forbiddenKey);
  }
  assert.doesNotMatch(serialized, /promotion.{0,80}(caused|drove|led to).{0,80}(carrier|delay|return|refund|dq)/i);
});

test('WEB-TRUST-001 staticLogical rejects the naive headline with exactly insufficient evidence', async () => {
  const data = await fixture();
  assert.equal(data.verifier.naiveHeadlineAccepted, false);
  assert.equal(data.verifier.conclusion, 'insufficient evidence');
  assert.equal(data.verifier.decisionGrade, false);
  assert.equal(data.verifier.numericScore, null);
});

test('WEB-TRUST-002 staticLogical assigns no fulfillment, return or DQ fact to a promotion', async () => {
  const data = await fixture();
  const promotion = data.cards.find(({ id }) => id === 'promotion');
  assert.deepEqual(Object.keys(promotion.facts).sort(), ['channel', 'promo_name']);
  assert.doesNotMatch(JSON.stringify(promotion), /carrier|return_reason|refund|scenario|data.quality/i);
  for (const card of data.cards.filter(({ id }) => id !== 'promotion')) {
    assert.doesNotMatch(JSON.stringify(card), /promo_name|promotionId|campaignId/i);
  }
});
