# Phase 2 — Bind Stage A and Measured Supply Chain

## Objective

Bind the runner to the exact released Stage A contract and acquire a reviewable linux/arm64 build
input set without predicting a base/image/release digest.

## Released Authority

- Stage A commit: fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9.
- Stage A tree: 27fc3667ef37892dad5c3fbfd76769f65a0760be.
- Lab: promotion-trust-v1 version 1.0.0, profile small-42.
- Commands: workspace.prepare, retail.generate, retail.load, retail.dbt-build, retail.export,
  promotion.configure, promotion.verify and workspace.reset.
- Operation API: learning-platform-v1/v1, sixteen synchronous operations and five mutations.
- Activation: one Issue #9 instance selecting only the three released I5-04 targets and
  fitness-result-v2.

## Exact Read-Only Interface Pins

| Path | Released SHA-256 |
|---|---|
| versions.md | a87ec218bdcbb1e69f12b06662ee0ecb3a6a467aea09a7552b98c61bcf5f54e8 |
| learning/contracts/learning-contract-set-v1.json | 92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638 |
| learning/contracts/learning-contract-set-v1.schema.json | 1cf55a7eeeff3d4a08340ae903d5f4e1812deb34849d99600296be507dd19648 |
| learning/contracts/learning-contract-version-registry-v1.json | a34c907e8870e89a182a180250a284f1a3c2ab3b6f1c4217c087cbc57775f9cb |
| learning/contracts/learning-contract-version-registry-v1.schema.json | d8c1881982e39e727a95f7491e6efeb288335bbef4a80d76efa891c3a8009ab8 |
| learning/contracts/schema-version-registry.json | 8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e |
| learning/contracts/canonicalization-v1.json | 2b985ef9c28e78c05b192c105b7f9d15fd60516c3a2c698d7da1bc315c605fce |
| learning/contracts/command-owner-registry-v1.json | a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80 |
| learning/contracts/command-owner-activation-v1.schema.json | 8fe337b7646fddc2dff4d1fc30e4a9120d0edec3f7eb293e8ead0e5d82f7a1f0 |
| learning/contracts/command-owner-activation-i5-03-v1.json | d20c5db284c4528106a0943a1970e665c6dbcc33dfc3dd05f2a9b01570ae8941 |
| learning/contracts/operation-matrix-v1.json | ffabcc11ca3943e3e520cd7b98c535032be439b1e2d1b920fe9ee17806180b1e |
| learning/contracts/operation-matrix-v1.schema.json | 98d77f883da45c47c6e277956ad31614003410ff43fea585fcdb432c4a12a128 |
| learning/contracts/completion-reconciliation-v1.json | 8fd50ced7a068c81f9868c23842ce680a46aba94a211bb932afef2beecc2d9ff |
| learning/contracts/completion-reconciliation-v1.schema.json | 64fed79f088cff1d0d548448c7d40fdbc4b8e60b6d4e57c0f08cdfbcd0c2f769 |
| learning/contracts/fitness-result-v1.schema.json | a104ad6330bcfc22bda0fb661fef96f067c09153da7dc2f306103e5f93a4ab6d |
| learning/contracts/fitness-result-v2.schema.json | d53f9b7b68b9f313bf0b9259fe5042bfb8cdbca0001570c18cd937de4971d6c6 |
| learning/contracts/learning-evidence-v1.schema.json | 52a68529b72ecb7f24c59ebe52e16e4ee5f21660164b1d20570827b18be3fe47 |
| learning/contracts/lab-v1.schema.json | 891c41100a28548e603ca1714aeaf5be2d541cd1780ab2ef72e3ef0740c6c16d |
| learning/labs/promotion-trust/lab-v1.json | 89ece51f41a17821d3266d2ba1fb7680cb70b07c2e9c5566d473aac9978d42d8 |
| learning/contracts/lesson-v1.schema.json | 9ece4e9cf5bf2a4dc375da13ce33ac7a696a374a225b0a7f9d1b9e089e7ea505 |
| learning/lessons/promotion-trust/lesson-v1.json | 758c6fb1ad75b283c313536d61bee61655bba6d27a2e685825ca20a28c838675 |
| learning/contracts/progress-v1.schema.json | a24c27b0c9abf0d553f1005c6ff4b19506fa2b9be3888b5315356b91cdc30767 |
| learning/contracts/promotion-trust-learning-manifest-v1.schema.json | 6b04b9acdc6097c43ede39f22d048b1b3095b96563e568ec6e2bc52527bd0255 |
| learning/manifests/promotion-trust-v1.json | 553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac |
| learning/contracts/make-input-contract-v1.json | 9ed76af1fca630de17acfcb904680f53d5d99a9692c2b2e10751c93587ca85c1 |
| contracts/openapi/learning-platform-v1.yaml | f82434b815decd5f200aac08650e3d2cd7f572a600d0a0d7e5a4e8d2f09efe87 |
| contracts/openapi/learning-platform-openapi-profile-v1.schema.json | 208fa1686caf9685483ba889e38974fb696c1d0015721bd639ad6d27fe6439bd |
| contracts/openapi/learning-platform-problem-details-v1.schema.json | 1af9440068c722732784d6c8a606da436de333ea8a77c12b4e545530ea11a1e9 |
| scripts/learning_contracts/schema.py | caa137de02542a330a3621a057912eefce95c64775e423db6c61a8ef5f58d005 |
| scripts/learning_contracts/registry.py | ca854421cef9880363929f3bea882f654cf3c8359ce3feecd3018febd1ce195d |
| scripts/learning_contracts/openapi.py | 792e9805b2fa0d98fdd30a5b266457597c9b1f19d317a26c130a87cecb43c2c6 |
| scripts/learning_contracts/state.py | 8149c9e976e2460570932d11b706a384587f00485ac078c63203d076f7e5c6a8 |
| scripts/learning_contracts/completion.py | ce557d4f03d574a902ea2d20c60b3f62e292e92fa6507c45ef8e393b6405f0ac |
| scripts/learning_contracts/fitness.py | 63c9729ffaa09f85d95d798c622565e106a9a730234e9102e5b6f20e3b060c20 |
| scripts/learning_contracts/evidence.py | aae9633c26e3e210e5f5b294bb44534795bae7e6002b8acbf9ecf46232b4949b |
| scripts/learning_contracts/canonical.py | 8649585335007e4afebf113263901f7ed84a28163ff648db95c930bf42e59113 |
| scripts/learning_contracts/check.py | 7734233a9d704ef5720f7a97f97ce822900c9c880021fc843cfd529b86b3c955 |
| mk/issue-5/i5-03.mk | 566acfb4956eafca4d91cf5efdc7f4205198a60cc5b988249975a614ff742576 |

Recompute and retain the existing 38 Stage A path/blob/SHA-256 rows and the 21-member released
contract-set closure from the immutable Git object. The minimum set includes versions, learning
contract set and schemas, version registry, canonicalization, Make input/activation, command owner
registry, operation matrix, completion reconciliation, fitness v2, learning evidence, lab/lesson/
progress schemas, manifest/lab/lesson instances, OpenAPI/profile/problem schemas and the released
schema/registry/openapi/state/completion/check/fitness/evidence/canonical readers. No current
working-tree substitution is accepted.

## Supply-Chain Steps

1. Expand every read-only input family in planned-paths-and-admissions.md to an exact context row
   with path, mode, size and SHA-256. Reject links, special files, untracked bytes and additions.
2. Select a supported official Python slim/Debian base compatible with linux/arm64 and the pinned
   dbt/DuckDB stack. Resolve the tag to the actual platform manifest digest under the recorded
   network side-effect gate. Record source, publisher, tag, platform and observed digest.
3. Resolve Python dependencies for linux/arm64 into a fully hashed lock. Download the exact wheels
   under the same gated acquisition step, record wheel hashes, then prohibit index/network access
   during build and runtime.
4. Record build-tool identities and license texts. Generate an SPDX inventory and close direct and
   transitive licenses against licenses-policy-v1. Unknown/unlicensed, AGPL, SSPL,
   noncommercial/source-available terms stop; LGPL/GPL cases require the obligations defined in
   the platform amendment.
5. Define vulnerability admission: no unresolved Critical/High finding in the chosen base, OS
   packages, Python lock or build toolchain. A waiver is an owner decision and therefore blocks.
6. Create released-contract-lock, context-manifest and wheelhouse-manifest from actual bytes.
   Validate the activation owner/command/version shape, but do not emit the activation instance:
   its required fragment hash cannot exist until Phase 3 creates the RED-only i5-04.mk bytes.
   Container-build-lock and image-release digest fields remain absent until the actual Phase 4
   build and test results exist.
7. Verify the exact build context output path is .artifacts/build/issue-9/runner-context.tar and the
   Dockerfile is apps/lab-runner/container/runner.Dockerfile. The root repository is never passed
   as context.

## Negative Tests

- Contract path/blob/hash drift, missing contract-set member or schema version mismatch.
- Tag-only base, wrong platform, digest mismatch or unofficial/unreviewed publisher.
- Unhashed wheel, sdist, online installer path, dependency-resolution drift or license ambiguity.
- Context addition, untracked file, link, special file, case collision or root-context attempt.
- Placeholder/fabricated digest or image release record written before observation.

## Exit Criteria

- Released contract closure and exact context input closure pass.
- Base/platform and wheel inputs have measured hashes and closed license/vulnerability gates.
- No image build has yet supplied a predicted result; build/release locks clearly distinguish
  pending measured fields.
- Activation owner/command/version fields are closed, while the instance remains absent pending
  the actual Phase 3 fragment hash.
- Phase 3 can write RED shards and bounded public verifier tests against the closed specification.

## Rollback

Remove only marker-owned local acquisition/build staging after identity checks. Preserve hash,
license and vulnerability evidence. Never edit shared inputs, Docker global state or registry data.
