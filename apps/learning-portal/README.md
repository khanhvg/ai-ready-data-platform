# Read-only learning portal

Vietnamese-first static reader for the released curriculum, architecture, Stage A lab material,
and promotion-trust lesson. The portal has no runner, API, database, progress state, browser
storage, external fetch, or command execution. Terminal commands are rendered only as
`<pre><code>` text for learners to run manually in their own local repository checkout.

From the repository root:

```bash
npm --prefix apps/learning-portal ci
make portal-test
make portal-a11y
make portal-e2e
make portal-visual-review
make portal-release-check
make learn
make learn-status
make learn-down
```

`make learn` serves the already built static inventory on an available loopback port. Every
released route has a generated HTML document, so direct links remain useful without JavaScript.
The `lesson-e2e` and `local-journey-e2e` targets remain fail-closed Stage B placeholders and are
not part of this read-only release.
