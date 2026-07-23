import { createSafeViewModel } from '../contracts/safe-view-model.mjs';

function escapeText(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

export function renderStaticDocument(route, catalog, assets = { scripts: [] }) {
  const model = createSafeViewModel(route, catalog);
  const navigation = model.navigation
    .map((item) => `<a href="${escapeText(item.path)}">${escapeText(item.label)}</a>`)
    .join('');
  const scripts = assets.scripts
    .map((source) => `<script type="module" src="${escapeText(source)}"></script>`)
    .join('');
  return `<!doctype html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeText(model.heading)}</title>
</head>
<body>
<div id="root">
<main data-semantic-ready="${String(model.semanticReady)}">
<h1>${escapeText(model.heading)}</h1>
<p>${escapeText(model.message)}</p>
<nav aria-label="Điều hướng cổng học tập">${navigation}</nav>
</main>
</div>
${scripts}
</body>
</html>
`;
}
