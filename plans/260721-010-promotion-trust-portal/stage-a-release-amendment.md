# Stage A Exact-Release Amendment

## Decision

Issue #10 Stage A is ready to cook from the pristine released integration commit
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, subject to the exact scope and gates in this
amendment. Stage A is a runner-independent, static/read-only portal slice. It provides a
Vietnamese-first learning shell, catalog/module/lesson/step navigation, the released
promotion-trust lesson, deterministic no-JavaScript output, and an explicit runner-unavailable
state. It cannot execute a lab, reset a workspace, create fresh evidence, persist progress, or
complete a lesson.

This amendment supersedes the empty Stage A authority in the original validation and blocked
readiness snapshots. Those reports remain immutable historical evidence at their recorded input
SHAs. Stage B authority remains empty and blocked on a released Issue #9 runner.

## Exact Release Authority

| Authority | Exact identity | Proof |
|---|---|---|
| Issue #7 approved feature head | `b219ba2d3843934c3bce2fbbec2a844b48b2dfa9` | Owner exact-head approval comment `5041125607`; tree `8ebd0f9a8ead8a6f3c382088cf172f28742a9c0b` |
| Issue #7 PR #22 merge | `1806b6d515f2f7a2ace2be7077af84a745ff221f` | Ordered parents are prior integration then approved head; merge tree equals approved-head tree |
| Issue #8 Stage A PR #23 merge | `5c2244c2c860234d0df49cf0a42ad950c6495717` | Ordered parent 1 contains Issue #7; parent 2 is approved Stage A head `8bdf8ec39c6f21423284a11f7a8ab38c75eeadfa` |
| Composition PR #25 merge and released integration | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | Ordered parents are PR #23 merge then approved composition head `734cf637a20ae186597e23d96a194ed4e30220ea`; tree equality proved |
| Released integration tree | `27fc3667ef37892dad5c3fbfd76769f65a0760be` | 903 tracked entries; `git ls-tree -r --full-tree` SHA-256 `4b95afd87ee7702f74df4a4b09198e13b8fa7ba45434c8a6a511a3ff1c580018` |
| Issue #8 Stage A release evidence | comment `5043195549` | `56/56`, invalid fixtures `65/65`, API 16 operations, final gate `4/4`, inherited gates `19/19`, `1/1`, `13/13`; no CI success claim |

Fresh remote proof must still show `refs/heads/integration/issue-5-local-learning` exactly at the
released integration SHA immediately before the cook branch is created. The cook branch starts
from that commit, not from this plan branch and not from a dependency feature worktree.

## Released Read-Only Dependency Binding

Every listed blob and SHA-256 was recomputed from the fetched released integration object. The
Stage A gate reads these paths from the cook input tree only. Feature worktrees, ignored
artifacts, retained spike evidence, and locally generated copies are not inputs.

### Issue #7 Vite and ADR bytes

| Released path | Git blob | Bytes | SHA-256 |
|---|---|---:|---|
| `docs/decisions/0005-web-stack.md` | `d392e61da322166d02508a49368752498f08bdb3` | 3659 | `6e26c48a027d226d8529fda939c07cca99e9f4e1d88cac12708deb98d6fe5eee` |
| `docs/decisions/evidence/adr-0005-web-stack-scorecard.json` | `2532fd78d0eb9cc2e2eb039275fb9e8aa68c2d28` | 3860 | `8f0bb73c5bc88d5d5afb5721773af2f882c021bc71eebe8ae3b2fd2e8c761db6` |
| `spikes/web/harness/simple-vite-v3.json` | `752a8a148c7b152d02c8f7a21d45031040fe9c0f` | 3902 | `04aa41f272c27e93a89c8febf371e57d420c37cd3edc4308c61933042990a4ff` |
| `spikes/web/harness/toolchain.json` | `1a757a7b38756f754cce356dd5f025d916d730fd` | 361 | `da4ac9ddf640c49018403359a5eed4b97a7e20739da6883e9adac1d6a52fb086` |
| `spikes/web/candidates/vite/package.json` | `2a78e04619f1571151f4e46367e6332b55b2f135` | 509 | `c80eab653ba83702e37dc41d19f18408714863bbb4c5e4d5d7e2da66a7f1b871` |
| `spikes/web/candidates/vite/package-lock.json` | `9444c03ca517aab2fa07ec85369241826fc60a53` | 32897 | `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c` |
| `spikes/web/candidates/vite/playwright.config.mjs` | `6e0a4b6f1d038cfa9ab954036a05e9a99cb0432e` | 928 | `a30bac72e4395c46d63521fecece2a346a970ad9099459572e56ba263279b6df` |
| `spikes/web/candidates/vite/vite.config.mjs` | `26a8c14fecafa57214491545b8c9e062f95fe069` | 2032 | `35e94a6b5ba137edc105cecee543f48a4cbee253bcb8d37638bb3519bc740805` |
| `spikes/web/candidates/vite/index.html` | `1ec097273d7151d7d013ef4318bb3a9405ffca80` | 5437 | `a911a851e705766d8f7bdf07f327f78b8627428538df6f473f918cb45a9a8b5f` |
| `spikes/web/candidates/vite/src/fixture.mjs` | `4926285ba0a6dec544137ccb3dbf493e9a03d459` | 789 | `70bb86af536fa11dee5b5e4d6d9ec38a09ea9a028db847c32beb76f1beae7e3f` |
| `spikes/web/candidates/vite/src/lesson-contract.mjs` | `dfb4a62ea1f73027d1ca9852952ebe7361c4c2ef` | 1542 | `32b19a5f2e25bd805f340917071c7935a70ae27397b366ca34f1a89054fc35d9` |
| `spikes/web/candidates/vite/src/main.jsx` | `3621b864a21e9bbac2f66d62be517797edecfda1` | 1122 | `a8e2b2521759d580932210e92803b448b82847ce30660627f937eda7c7311183` |
| `spikes/web/candidates/vite/src/styles.css` | `48b0f3ff9d03bce4c29287472439f65d2d390632` | 1875 | `01869583850d3ff5ab2b4b1448476e117ee62a5d3b92af0a821947979d069564` |
| `spikes/web/candidates/vite/tests/foundation.test.mjs` | `4954cc96ccece82b92c5a42793741be6ae64bba1` | 1587 | `79f34178f9651d99e861687de3acfdc3e8499b1d3366b3e3efa4abffff88e9e9` |
| `spikes/web/candidates/vite/tests/promotion-trust-contract.test.mjs` | `fce89b00e2e17da0bcc67b7d5752c2646ad0c60d` | 4917 | `323a8608399dc6cc12fc59185979087477af7553d23aeb6c2e0b87090e7ac8f9` |
| `spikes/web/candidates/vite/tests/simple-vite-smoke.spec.mjs` | `1add2452a278519231f4eaf514c466317833e724` | 9843 | `ac7f5d7b6a385d7bb1f37afac3f3fe9deba11728ce230763caf7dee709442aaa` |

The portal preserves the exact transitive package tuples and integrity fields from the released
lock. Only the lock root package name and script metadata may differ to identify the portal; the
dependency graph must compare equal. Node `22.22.3`, npm `10.9.8`, lockfile v3, Vite `8.1.5`,
React/React DOM `19.2.7`, Playwright `1.61.1`, axe Playwright `4.12.1`, and React plugin `6.0.1`
are exact. This promotes the accepted toolchain, not the spike's page structure, state machine,
fixture adapter, score/timer harness, retained evidence, or product architecture.

### Issue #8 Stage A contracts and validators

| Released path | Git blob | Bytes | SHA-256 |
|---|---|---:|---|
| `contracts/openapi/learning-platform-openapi-profile-v1.schema.json` | `6a2d429c0299788ca7e5b1602a17d49c142c66d9` | 7715 | `208fa1686caf9685483ba889e38974fb696c1d0015721bd639ad6d27fe6439bd` |
| `contracts/openapi/learning-platform-problem-details-v1.schema.json` | `ec9cd805c91c18ae28070f89db32a1f48c19efd6` | 1323 | `1af9440068c722732784d6c8a606da436de333ea8a77c12b4e545530ea11a1e9` |
| `contracts/openapi/learning-platform-v1.yaml` | `6544b3ede848bacf782ebbb5d0f2b7a9bde4f8d8` | 61375 | `f82434b815decd5f200aac08650e3d2cd7f572a600d0a0d7e5a4e8d2f09efe87` |
| `learning/contracts/command-owner-activation-i5-03-v1.json` | `deca53d4cddf46705f748ead764ce92c838fd7bb` | 939 | `d20c5db284c4528106a0943a1970e665c6dbcc33dfc3dd05f2a9b01570ae8941` |
| `learning/contracts/completion-reconciliation-v1.json` | `0ca00ab1dc9d7a16cdc11e45dfba3c5c9a867d70` | 2413 | `8fd50ced7a068c81f9868c23842ce680a46aba94a211bb932afef2beecc2d9ff` |
| `learning/contracts/completion-reconciliation-v1.schema.json` | `ad24178f2de30d8f66738381c59902898ca01ae3` | 5176 | `64fed79f088cff1d0d548448c7d40fdbc4b8e60b6d4e57c0f08cdfbcd0c2f769` |
| `learning/contracts/fitness-result-v2.schema.json` | `4cc4a9b1b51afbaa94a0dd3f9912ef51f4f8994d` | 5094 | `d53f9b7b68b9f313bf0b9259fe5042bfb8cdbca0001570c18cd937de4971d6c6` |
| `learning/contracts/lab-v1.schema.json` | `448d20d86d3c5e157147f9b16c52dc4ee78d6def` | 11679 | `891c41100a28548e603ca1714aeaf5be2d541cd1780ab2ef72e3ef0740c6c16d` |
| `learning/contracts/learning-contract-set-v1.json` | `0a85119871f769a17dc464591bf0623524e9a97e` | 7585 | `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638` |
| `learning/contracts/learning-contract-set-v1.schema.json` | `bee2ded5cf3af4ffc3b67838ee7ab7a61c4c8be7` | 1854 | `1cf55a7eeeff3d4a08340ae903d5f4e1812deb34849d99600296be507dd19648` |
| `learning/contracts/learning-contract-version-registry-v1.json` | `67278f8b36a62efe8b449ee1a50fe027b9012d87` | 6676 | `a34c907e8870e89a182a180250a284f1a3c2ab3b6f1c4217c087cbc57775f9cb` |
| `learning/contracts/learning-contract-version-registry-v1.schema.json` | `212fcbc44bc1a3d69efa116acf3a37f80fe20ceb` | 6301 | `d8c1881982e39e727a95f7491e6efeb288335bbef4a80d76efa891c3a8009ab8` |
| `learning/contracts/learning-evidence-v1.schema.json` | `ca5d355d9ee6236554db58421b4f3f252fc59532` | 5002 | `52a68529b72ecb7f24c59ebe52e16e4ee5f21660164b1d20570827b18be3fe47` |
| `learning/contracts/lesson-v1.schema.json` | `d053f69ac80e279e8ad0022d4ef671d9810cf52d` | 10939 | `9ece4e9cf5bf2a4dc375da13ce33ac7a696a374a225b0a7f9d1b9e089e7ea505` |
| `learning/contracts/operation-matrix-v1.json` | `311b28d4650ce2e428571fec6271264be166f090` | 27271 | `ffabcc11ca3943e3e520cd7b98c535032be439b1e2d1b920fe9ee17806180b1e` |
| `learning/contracts/operation-matrix-v1.schema.json` | `91a036290652610b965f2bd5c6169605415de016` | 6560 | `98d77f883da45c47c6e277956ad31614003410ff43fea585fcdb432c4a12a128` |
| `learning/contracts/progress-v1.schema.json` | `0822f00644dbff3ccf760a18d59fe7a0c6d2766d` | 1883 | `a24c27b0c9abf0d553f1005c6ff4b19506fa2b9be3888b5315356b91cdc30767` |
| `learning/contracts/promotion-trust-learning-manifest-v1.schema.json` | `81faf51e5d0c1eccbc73ae0bd9bc7ddef5dd32b2` | 2551 | `6b04b9acdc6097c43ede39f22d048b1b3095b96563e568ec6e2bc52527bd0255` |
| `learning/contracts/canonicalization-v1.json` | `345259c707a550612ffd189c12e69d98c625b5e6` | 403 | `2b985ef9c28e78c05b192c105b7f9d15fd60516c3a2c698d7da1bc315c605fce` |
| `learning/contracts/command-owner-activation-v1.schema.json` | `dd9d5c0a68e012c87f5467ce8113d4347284bdd2` | 1870 | `8fe337b7646fddc2dff4d1fc30e4a9120d0edec3f7eb293e8ead0e5d82f7a1f0` |
| `learning/contracts/evidence-envelope-v1.schema.json` | `759f64dbd8cc57c56a96f13aa771555f0cc7f7d7` | 721 | `5586e5fbfb7621a2c8a132068ac359f8b3ef6b13e62f8224916a9c8c0ece3e69` |
| `learning/contracts/fitness-result-v1.schema.json` | `0212ca96614aea02dbb60434d67a0cbb379a8213` | 1375 | `a104ad6330bcfc22bda0fb661fef96f067c09153da7dc2f306103e5f93a4ab6d` |
| `learning/contracts/golden-evidence-v1.schema.json` | `c36cc0fd786d1b85414d9c2c4dd6450b5c4c1a91` | 374 | `cfb8e957abf2c624787e71e9ae6e2297b525f49d097bbb82e0d1c853c78fc068` |
| `learning/contracts/make-input-contract-v1.json` | `904209e12566c5e8ff7eb5760cd7e83dc2fddbde` | 470 | `9ed76af1fca630de17acfcb904680f53d5d99a9692c2b2e10751c93587ca85c1` |
| `learning/contracts/promotion-trust-evidence-v1.schema.json` | `99f76dd0cd4b23fb42071070dcfc1dcf507a42e5` | 932 | `aaf0777012fe2905d19ba7c0bc3cca1e72f9e67d448a4b4b6a8b33824db70dab` |
| `learning/contracts/promotion-trust-fixture-manifest-v1.schema.json` | `6ea05017402e73ed894ea1592f28f47588e938d4` | 1396 | `82dc60e640b3f6d301bd739490b2928d88275926e26fb87e4457b7ff01a616bc` |
| `learning/contracts/promotion-trust-fixture-manifest-v2.schema.json` | `fdfa968ca02fc79e71fe683e671cec2df0d322d7` | 1520 | `221957acf9d09d74070b3ec8d34a7d2d730c7de1e9f8e25e3a81b2f04d8ae3bf` |
| `learning/contracts/promotion-trust-portable-run-attestation-v1.schema.json` | `4be78f6586c1602dcf20851241982fde7f934035` | 3425 | `5cff300e93e806084fe9357c05b21174f75e755a0c0dab8d30c128a40ef594ef` |
| `learning/contracts/promotion-trust-v1.schema.json` | `9b28a06f65528a4c163e6bc3576cc2916b6104a5` | 664 | `43fc68833237ef5b522f82fbbd18caba0f11e16bf66e0ff26cf44f0238c39871` |
| `learning/contracts/retail-golden-v1.schema.json` | `97adac7f07ed5a7db53348aa718e70c980cebbe3` | 826 | `d741261816c25e4e04f767d5475eac335de2eb24f9f0c2d5005c4cde4415eed5` |
| `learning/contracts/schema-version-registry.json` | `c63a41853c49fb16f381950f74339e14017fc355` | 5816 | `8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e` |
| `learning/labs/promotion-trust/lab-v1.json` | `fcd7d4dfd1bdde8afdfb53be0072e92c295cda37` | 4163 | `89ece51f41a17821d3266d2ba1fb7680cb70b07c2e9c5566d473aac9978d42d8` |
| `learning/lessons/promotion-trust/lesson-v1.json` | `39414e046027a9deb13a5acf74d78182515b15be` | 4395 | `758c6fb1ad75b283c313536d61bee61655bba6d27a2e685825ca20a28c838675` |
| `learning/manifests/promotion-trust-v1.json` | `1aa66a371aa2775213d3d9ef52c95eabd5f72600` | 2130 | `553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac` |
| `scripts/learning_contracts/__init__.py` | `9b47c17bff6ff9545086d6692de250ddc654feb5` | 596 | `996e6079e073e5d4175a7ecb67ab5a393ac921bb0129414179e771afe1571f76` |
| `scripts/learning_contracts/canonical.py` | `e8e1d12a13ede2ce0d3db33deac27c5f82e06a0f` | 2162 | `8649585335007e4afebf113263901f7ed84a28163ff648db95c930bf42e59113` |
| `scripts/learning_contracts/check.py` | `0b5067d3a909b69b43520b093dd47204c7b8a914` | 29986 | `7734233a9d704ef5720f7a97f97ce822900c9c880021fc843cfd529b86b3c955` |
| `scripts/learning_contracts/completion.py` | `5b385faf8a818b8e0c28ad358fec1b64d97db3ea` | 4046 | `ce557d4f03d574a902ea2d20c60b3f62e292e92fa6507c45ef8e393b6405f0ac` |
| `scripts/learning_contracts/evidence.py` | `b1bd673e8cdd72eec171f3ac371086cef2901b53` | 8499 | `aae9633c26e3e210e5f5b294bb44534795bae7e6002b8acbf9ecf46232b4949b` |
| `scripts/learning_contracts/fitness.py` | `854752fcb52d330ba0df70dc4477d571efc61466` | 7049 | `63c9729ffaa09f85d95d798c622565e106a9a730234e9102e5b6f20e3b060c20` |
| `scripts/learning_contracts/guidance.py` | `d0825c25bc696bfaadf5e3ac0954d8b9dddb6c19` | 2399 | `413af50bce69e66822e0d82b4debdd29e15fc6f528ee72e6319dc0f80972a141` |
| `scripts/learning_contracts/openapi.py` | `ff1221bc54a066fadb243b9c312dcb84629441b4` | 40995 | `792e9805b2fa0d98fdd30a5b266457597c9b1f19d317a26c130a87cecb43c2c6` |
| `scripts/learning_contracts/references.py` | `9c9ccc930a8e86fe631b81661ab933761c0060c0` | 5924 | `5365c5ebf1fbf3e4d10d015fad3a216d15ea9bbb2327bc332166da561440ef54` |
| `scripts/learning_contracts/registry.py` | `adcd803fef2e219859db6c3349ffca84d7ed9cfb` | 6540 | `ca854421cef9880363929f3bea882f654cf3c8359ce3feecd3018febd1ce195d` |
| `scripts/learning_contracts/runtime.py` | `021a549bd8bf3049152f74b62ff5d6cc63069fd0` | 31758 | `6a8aaa88c4d38b85c8a889779be900d1d99d95f7bbca3977a03a3a4f2642808d` |
| `scripts/learning_contracts/schema.py` | `89193411c92e0695afe95accb128d729fcdce26b` | 5253 | `caa137de02542a330a3621a057912eefce95c64775e423db6c61a8ef5f58d005` |
| `scripts/learning_contracts/state.py` | `92a2a804c87b139fce1ef478877209a9a9ccdfa8` | 2855 | `8149c9e976e2460570932d11b706a384587f00485ac078c63203d076f7e5c6a8` |

### Repository integration and protected bytes

| Released path | Git blob | Bytes | SHA-256 |
|---|---|---:|---|
| `Makefile` | `e1a4332a9645ccbd37bec4be1f70372241e16b7b` | 6344 | `12926b16a797fded79b0b11b00147887258721f145c79e66472f44c5f0228458` |
| `learning/contracts/command-owner-registry-v1.json` | `18d05a010da0d462c4e146954a18560c6b826af4` | 13361 | `a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80` |
| `mk/issue-5/i5-03.mk` | `c9926d6a34474c1e3d0275f878bc2041bcb44e05` | 2603 | `566acfb4956eafca4d91cf5efdc7f4205198a60cc5b988249975a614ff742576` |
| `contracts/data/retail-golden-v1.json` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` | 3031 | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` |
| `contracts/data/promotion-trust-v1.yaml` | `876789d549276b44a6e64cc4c9a471886fd2752b` | 1682 | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` | 16252 | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `a4b32032962f5f787d733f7de8cf657491944e37` | 4364 | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` |
| `release-manifest.json` | `b27d231c5ee6d48fd7932b06807ef6a9a2220e21` | 366321 | `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` |
| `requirements/golden-py312-macos-arm64.lock` | `3afac7a4cc678cd68d2fe419c5b7b33561b9f93d` | 59389 | `f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2` |
| `plans/260721-008-version-learning-contracts/phase-05-stage-a-compatibility-release-and-staged-handoff.md` | `01ffbc5b7a58b79db27e840a6581514babb99c45` | 14863 | `b4fe608d10ae9c0e9211de4dcf16372ca06128fe631c6a388428639fe828b282` |

The root Make bytes prove the sorted `mk/issue-5/*.mk` include seam; `i5-03.mk` proves exact
validator command ownership and admitted-runtime invocation. The registry bytes prove all
nine I5-05 public commands are reserved to `mk/issue-5/i5-05.mk` as
`future-owner/not-runnable` with `fitness-result-v1` evidence ownership before Stage A activation.
The protected data/fixture/release bytes prove identity only. The Python lock and Issue #8 phase
bytes are exact transitive inputs of the released runtime admission marker. All remain read-only.

The Stage A adapter admits only registry-current `lesson-v1`, `lab-v1`,
`promotion-trust-learning-manifest-v1`, and the exact contract set. It invokes the released
`learning-contracts-check`, `lesson-check`, and `api-contracts-check` validators before mapping
safe fields. It binds the read-only `listLessons` and `getLesson` operation identities for
contract compatibility but does not start an HTTP API or call either operation. Progress,
completion, evidence, workspace, reset, verify, tool, and query operations are read only for
negative-boundary tests; Stage A exposes none of them.

## Exact Stage A Tracked Write Allowlist

Only these new tracked files may be created. There are no Stage A modifies or deletes because the
released tree contains neither the portal directory nor the Issue #10 Make fragment.

```text
apps/learning-portal/index.html
apps/learning-portal/package.json
apps/learning-portal/package-lock.json
apps/learning-portal/playwright.config.mjs
apps/learning-portal/command-owner-activation.stage-a.json
apps/learning-portal/release-binding.stage-a.json
apps/learning-portal/vite.config.mjs
apps/learning-portal/scripts/generate-static-routes.mjs
apps/learning-portal/scripts/portal-lifecycle.mjs
apps/learning-portal/scripts/serve-built-portal.mjs
apps/learning-portal/scripts/verify-stage-a-release.mjs
apps/learning-portal/scripts/write-review-artifacts.mjs
apps/learning-portal/src/app/app-shell.jsx
apps/learning-portal/src/app/lesson-navigation.jsx
apps/learning-portal/src/app/module-navigation.jsx
apps/learning-portal/src/app/portal-status.jsx
apps/learning-portal/src/catalog/module-catalog.mjs
apps/learning-portal/src/catalog/released-module-provider.mjs
apps/learning-portal/src/contracts/released-learning-adapter.mjs
apps/learning-portal/src/contracts/safe-view-model.mjs
apps/learning-portal/src/features/promotion-trust/promotion-trust-lesson.jsx
apps/learning-portal/src/main.jsx
apps/learning-portal/src/render/static-document.mjs
apps/learning-portal/src/routing/portal-router.mjs
apps/learning-portal/src/styles.css
apps/learning-portal/tests/e2e/stage-a.spec.mjs
apps/learning-portal/tests/e2e/visual-review.spec.mjs
apps/learning-portal/tests/unit/module-catalog.test.mjs
apps/learning-portal/tests/unit/portal-router.test.mjs
apps/learning-portal/tests/unit/release-binding.test.mjs
apps/learning-portal/tests/unit/released-learning-adapter.test.mjs
apps/learning-portal/tests/unit/render.test.mjs
apps/learning-portal/tests/unit/security.test.mjs
mk/issue-5/i5-05.mk
```

`node_modules/**`, `dist/**`, Playwright output, PID files, logs, screenshots, traces, and review
manifests are run-owned generated state only. They remain untracked and must be absent after
cleanup. The app lock is currently ignored by the root pattern, so publication force-adds only
`apps/learning-portal/package-lock.json` after exact scope inspection; `.gitignore` does not
change.

`command-owner-activation.stage-a.json` is an app-owned instance of the released
`command-owner-activation-v1` schema. It binds the immutable base registry hash, owner `I5-05`,
the final `mk/issue-5/i5-05.mk` hash, all nine reserved command IDs, availability `implemented`,
and `fitness-result-v2`. “Implemented” means the recipe exists: the two Stage B recipes still emit
a truthful non-zero `STAGE_B_DEPENDENCY_UNAVAILABLE` fitness result. The activation is finalized
only after the Make fragment bytes stabilize, and its schema/base/fragment identities are
validated without editing the shared registry.

## Portal Architecture and Extension Seams

```text
released contract set + manifest + validators
                   |
                   v
released-module-provider -> safe PortalCatalog view model
                                  |
                catalog -> module -> lesson -> narrative step
                                  |
                    app shell + read-only router
                      |                   |
               React enhancement    static route renderer
                      \                   /
                       same escaped facts
```

- `PortalCatalog` is a closed app view model, not a new public contract. It contains only released
  IDs, versions, title/summary/level, stakeholder decision, ordered narrative-step IDs, lab
  availability, accessibility flags, source grains/limitations, and decision status.
- The current catalog has one vertical slice derived from manifest `promotion-trust-v1`; it is
  not labelled as the whole course. The shell supports foundation-to-mid level metadata without
  inventing foundation, junior, architecture, or data-lab content.
- Shell navigation, breadcrumbs, back/forward/reload, focus management, static-route generation,
  and empty/unavailable states operate on the view model rather than hard-coded lesson switches.
- Future #11/#12 releases may provide registered curriculum/module/lesson/lab manifests to the
  same provider. The provider accepts only exact hash-bound files under released contract sets
  and only schema families recognized by their released validators. Unknown families, paths,
  versions, fields, or hashes fail closed. New content may require a new release binding, but not
  a shell, router, navigation, or rendering redesign.
- Vietnamese is the default shell language for navigation, statuses, guidance, errors, and
  accessibility labels. Exact released English stakeholder questions, identifiers, failure
  codes, and decision values remain distinguishable and are never silently rewritten.
- The static renderer and React enhancement share the same safe view model. There is no second
  hand-maintained lesson, copied Issue #7 `lesson-contract.mjs`, copied fixture, raw HTML/MDX, or
  duplicated #8 schema/registry.
- Stage A serves files with one built-in Node static server. It has no BFF routes, database,
  session, cookie, CSRF state, API proxy, runner client, service worker, or browser persistence.

## Exact Stage A Command Allowlist

| Class | Exact command | Required disposition |
|---|---|---|
| Release runtime/orchestrator | `node apps/learning-portal/scripts/verify-stage-a-release.mjs` | Prepare one marker-owned exact-lock Python runtime, admit it, run the next three commands, then remove only that runtime |
| Release validation | `make learning-contracts-check` | Pass through the released #8 admitted runtime |
| Release validation | `make lesson-check LESSON=promotion-trust` | Pass and retain its emitted locator as dependency evidence only |
| Release validation | `make api-contracts-check` | Pass with 16 exact operations; Stage A admits only the two lesson reads |
| Install | `npm --prefix apps/learning-portal ci --ignore-scripts --no-audit --no-fund` | Exact #7 transitive lock; no lifecycle scripts |
| Unit/contract | `npm --prefix apps/learning-portal run test:unit` | Real release adapter, catalog, render, router, security RED/GREEN |
| Production build | `npm --prefix apps/learning-portal run build` | Vite production build plus deterministic static routes |
| Browser/a11y | `npm --prefix apps/learning-portal run test:stage-a -- --workers=1 --retries=0` | One Chromium journey at desktop and narrow, axe and no-JS |
| Visual artifacts | `npm --prefix apps/learning-portal run test:visual -- --workers=1 --retries=0` | Fixed bounded states; no UAT approval claim |
| Supply chain | `npm --prefix apps/learning-portal audit --audit-level=high --json` | Zero High/Critical; result interpreted, not hidden |
| Public Stage A | `make portal-test portal-a11y` | Pass focused unit/contract/security/build and axe gates |
| Public Stage A | `make portal-e2e` | Pass desktop+narrow/no-JS/runner-unavailable journey |
| Public Stage A | `make portal-visual-review` | Pass artifact bounds; checklist remains unapproved |
| Public Stage A | `make learn LESSON=promotion-trust` | Start static portal only; report runner unavailable and completion disabled |
| Public Stage A | `make learn-status` | Report only owned static portal process and Stage B blocked state |
| Public Stage A | `make learn-down` | Stop only owned portal process; preserve review artifacts |
| Required negative | `make lesson-e2e LESSON=promotion-trust` | Non-zero `STAGE_B_DEPENDENCY_UNAVAILABLE`; no runner action |
| Required negative | `make local-journey-e2e` | Non-zero `STAGE_B_DEPENDENCY_UNAVAILABLE`; no completion claim |

The release verifier is the sole Python acquisition/orchestration entry. It checks CPython
`3.12.3`, allocates one nonce/marker-owned child below `.artifacts/workspaces/golden/`, and permits
only these fixed argv shapes: `python3.12 -m venv OWNED/venv`; the owned interpreter with
`-m pip install --require-hashes --only-binary=:all: --no-cache-dir --index-url
https://pypi.org/simple -r requirements/golden-py312-macos-arm64.lock`; the owned interpreter with
`-m pip check`; and the released `make learning-runtime-admit` plus the three listed validator
targets. `OWNED` and `LEARNING_RUNTIME_INTERPRETER_SHA256` are containment-checked run values
allocated/measured by the verifier, not plan placeholders or claimed release SHAs. The exact
56-distribution lock SHA-256 is
`f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2`; normalized freeze must be
`cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba` before validators run.
After acquisition, validator reruns are network-disabled. The verifier removes only its admitted
runtime after retaining bounded dependency results.

No command may bootstrap data, call Docker, install a browser, invoke Issue #9,
start an optional service, access cloud/AWS/Terraform, or use an alternate runtime/package
manager. Direct ad hoc variants and root Make edits are denied.

## Resource, Output, and Artifact Bounds

- Preserve the released #7 ceilings: install 300 seconds, build 180 seconds, Node/unit 120
  seconds, host readiness 15 seconds, Playwright 300 seconds, and audit 180 seconds.
- One portal Node process; loopback `127.0.0.1`; runtime-selected port; no child after startup.
  Test orchestration uses one Playwright worker and the existing Chrome channel only.
- Production output: regular files only; at most 128 files, 1 MiB per file, and 16 MiB total; no
  source maps, symlink, hardlink alias, FIFO, device, socket, or executable content outside the
  declared JS/CSS/HTML assets.
- Static server: GET and HEAD only; request target at most 2048 bytes; no request body; response
  at most the admitted file size; directory traversal, percent-decoding ambiguity, dot segments,
  unknown routes, and foreign Host fail closed.
- Review output: exactly two viewports and at most eight named screenshots, one trace, one axe
  JSON, one no-JS inventory, one console/CSP record, and one hash manifest; 2 MiB per text log,
  16 MiB per binary artifact, 64 MiB aggregate.
- Runtime/review roots are marker- and nonce-bound beneath `.artifacts/runtime/i5-05-stage-a/`
  and `.artifacts/evidence/local-journey/`; cleanup rejects aliases and foreign ownership, stops
  only the recorded PID/start identity, preserves review evidence, and is idempotent twice.
- Missing measurement/enforcement is fail. These are Stage A app safety ceilings, not a runner,
  hosted performance, or course-completion claim.

## Requirements and Scenario Catalogue

| ID | Stage A requirement | Proof |
|---|---|---|
| SA-R01 | Exact #7/#8/integration identities and all admitted bytes match | Release-binding unit/mutation tests |
| SA-R02 | Frozen Vite dependency graph and exact tool versions | Lock comparison, `npm ci`, build, audit |
| SA-R03 | Vietnamese-first reusable catalog/module/lesson/step shell | Server render + Chromium semantics |
| SA-R04 | Promotion-trust is one vertical slice, not the complete course | Catalog and copy assertions |
| SA-R05 | Released lesson/lab/manifest facts map through released validators | Contract adapter tests |
| SA-R06 | Back/forward/reload navigate read-only state only | Router unit + Chromium history |
| SA-R07 | Runner unavailable, execution disabled, completion impossible | Bundle/DOM/network/storage negatives |
| SA-R08 | No-JavaScript and React modes expose equivalent released facts | Built HTML parser + JS-disabled Chromium |
| SA-R09 | CSP/XSS/Host/path/storage/cloud boundaries fail closed | S3 unit/browser/scanner tests |
| SA-R10 | Lifecycle, artifacts, cleanup, and rollback stay bounded | Process/path/limit/cleanup tests |
| SA-R11 | #11/#12 can supply later released manifests through the provider seam | Synthetic contract-shape unit test using in-memory registered descriptors only |

| ID | Scenario | Expected result |
|---|---|---|
| SA-SC01 | Load the portal root with JavaScript enabled | Vietnamese shell, one promotion-trust catalog entry, no false course-complete language |
| SA-SC02 | Navigate module, lesson, and narrative steps; use back/forward/reload | Same released selection; zero mutation/network replay |
| SA-SC03 | Inspect four independent grains and canonical decision | Exact released facts; no causal attribution |
| SA-SC04 | Reach run/reset/verify narrative steps in Stage A | Explanation only; runner unavailable; no actionable control |
| SA-SC05 | Load with JavaScript disabled | Same required facts and unavailable/non-completion notice |
| SA-SC06 | Supply wrong path/hash/version/unknown field or unregistered module family | Build/test fails closed before render |
| SA-SC07 | Inject script, event handler, URL, raw HTML, oversized content, or foreign Host | Inert/rejected; no CSP relaxation or data leak |
| SA-SC08 | Run desktop then narrow Chromium journey | No overflow, logical focus, live status, axe zero Critical/Serious |
| SA-SC09 | Start, query status, stop twice, then inspect evidence | Only owned process stopped; review artifacts retained; no leak |
| SA-SC10 | Invoke Stage B acceptance commands | Typed non-zero dependency-unavailable; no runner import or action |

## TDD and RED Catalogue

Retain each RED at the pristine integration input or a tests-only descendant before its matching
behavior. RED must traverse the real portal render/router/adapter path and fail for the asserted
missing behavior, never because a tool/import is absent.

| RED ID | First real failure |
|---|---|
| `PTP-RED-A-001` | Wrong release SHA/tree/blob/hash/version/lock is admitted |
| `PTP-RED-A-002` | Protected Issue #6 bytes drift without failing |
| `PTP-RED-A-010` | Portal server render lacks catalog/module/lesson/step shell or required facts |
| `PTP-RED-A-011` | Cross-grain attribution or non-canonical decision renders |
| `PTP-RED-A-012` | Stage A exposes execution/reset/verify/completion or calls runner/progress/evidence operations |
| `PTP-RED-A-013` | Back/forward/reload changes anything beyond validated view state |
| `PTP-RED-A-014` | Built no-JS response lacks required facts/navigation/unavailable state |
| `PTP-RED-A-015` | Runner unavailable is confused with controlled lesson failure |
| `PTP-RED-A-016` | Vietnamese shell semantics, focus, narrow reflow, reduced motion, or live status fail |
| `PTP-RED-A-020` | Released-module provider accepts an unregistered family/path/hash/version/field |
| `PTP-RED-A-021` | Static and React renderers disagree on stable fact IDs or escaping |
| `PTP-RED-A-022` | Stage A build/bundle contains Issue #9, API mutation, browser storage, secret, cloud, or source map |
| `PTP-RED-A-023` | Output/artifact/process/request ceilings or alias/special-file controls are absent |
| `PTP-RED-A-024` | Cleanup/status can target foreign PID/path or remove retained artifacts |

## Stage A S3 Disposition

All `PTP-S3-01..14` IDs remain unique. Stage A must pass the applicable rows now: exact Host and
loopback binding; no cookie/session/runner credential; no CORS; no mutation/CSRF surface; no
browser-direct runner; no command/path/URL/SQL input; escaped content; no artifact inline
execution; no completion authority; no replayable mutation; bounded/redacted output; frozen lock
and audit; scoped cleanup; exact contract versions; and zero cloud/model credential propagation.
Rows whose exploit requires a Stage B mutation are still tested as absence assertions. They are
not marked passed by skip.

Production responses use this Stage A CSP without inline exceptions:

```text
default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:;
connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none';
form-action 'none'; worker-src 'none'
```

React interpolation and the static renderer both escape text. `dangerouslySetInnerHTML`, raw
HTML/MDX, runtime `eval`, external content fetch, service workers, local/session storage,
IndexedDB, caches, cookies, runner URLs/tokens, ambient environment, absolute paths, and raw
fixture rows are forbidden.

## Verification and Review Gate

1. Prove a clean cook branch whose start commit, tracking base, and fresh remote integration are
   the released integration SHA; prove Issue #7/#8 ancestry and tree identities.
2. Retain RED evidence, implement only the exact tracked write allowlist, and keep all dependency
   paths read-only.
3. Run the exact #8 validator commands, frozen install, unit/contract/security tests, production
   build twice, deterministic static digest comparison, audit, bundle scan, and protected hashes.
4. Run one Chrome-channel Chromium journey at `1280x800` and `360x800`, axe zero
   Critical/Serious, real JavaScript-disabled navigation, explicit runner-unavailable state, and
   bounded visual artifacts.
5. Run public Stage A commands, the two Stage B negative commands, lifecycle/status/down twice,
   cleanup, and static rollback rehearsal.
6. Re-run changed-path allowlist, command ownership, secret/private-path/cloud/source-map scans,
   `git diff --check`, package-lock tracking, artifact exclusion, and clean-tree checks.
7. Require two fresh independent exact-head implementation reviews and named human exact-head
   pre-merge approval. A later commit invalidates those gates.

Stage A review evidence may state that rendering, navigation, accessibility, security, build,
cleanup, and rollback passed. It must state `runner: unavailable`, `execution: disabled`,
`reset: not-run`, `freshEvidence: false`, and `completion: disabled`. It cannot close Issue #10.

## Stage B

Stage B file, command, and dependency SHA allowlists are `[]`. Issue #9 is open and unreleased;
its current planning/amendment branches are not consumable authority. Stage B remains
`blocked-on-issue9` until a later exact released runner SHA is pinned by a new amendment and passes
fresh independent validation/readiness.

## Rollback

Before merge, rollback is normal deletion of only the exact new Stage A tracked files plus
run-owned generated state; protected and dependency bytes remain untouched. After an accepted
Stage A merge, use a reviewed revert of that exact Stage A commit/PR. In both cases retain review
evidence, stop only the owned static process, and re-prove the pristine released integration
tree. No reset, history rewrite, dependency revert, cloud action, or broad cleanup is authorized.
