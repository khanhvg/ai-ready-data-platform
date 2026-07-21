import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { loadFixture } from './src/fixture.mjs';
import { lessonContract } from './src/lesson-contract.mjs';

const escapeHtml = value => String(value).replace(
  /[&<>"']/g,
  character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character],
);

function assertFixtureContract(evidence) {
  const actualGrains = evidence.sources.map(({ grain }) => grain.join(' × '));
  const expectedGrains = lessonContract.grains.map(({ value }) => value);
  if (JSON.stringify(actualGrains) !== JSON.stringify(expectedGrains)) {
    throw new Error('Tracked evidence grains do not match the lesson contract.');
  }
  if (
    evidence.decision.value !== lessonContract.decision.value
    || evidence.decision.reason !== lessonContract.decision.reason
  ) {
    throw new Error('Tracked evidence decision does not match the lesson contract.');
  }
}

function fixtureHtml() {
  return {
    name: 'tracked-fixture-html',
    transformIndexHtml(html) {
      const { evidence, manifest, digests } = loadFixture();
      assertFixtureContract(evidence);

      const sourceSignatures = evidence.sources
        .map(({ grain }) => `<li><code>${escapeHtml(grain.join(', '))}</code></li>`)
        .join('');
      const digestFacts = Object.entries(digests)
        .map(([name, digest]) => `<li><span>${escapeHtml(name)}</span>: <code>${escapeHtml(digest)}</code></li>`)
        .join('');
      const metadata = `<details class="fixture-metadata"><summary>Dữ liệu fixture đã theo dõi</summary><p>Manifest ${escapeHtml(manifest.schemaVersion)}; chỉ xác minh tính toàn vẹn của dữ liệu cục bộ.</p><p>Định dạng mảng mức hạt trong fixture:</p><ul>${sourceSignatures}</ul><p>SHA-256:</p><ul>${digestFacts}</ul></details>`;

      return html.replace('<!--FIXTURE-METADATA-->', metadata);
    },
  };
}

export default defineConfig({
  plugins: [react(), fixtureHtml()],
  build: { sourcemap: false },
});
