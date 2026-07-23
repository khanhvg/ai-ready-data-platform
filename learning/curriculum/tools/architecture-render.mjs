import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { constants as fsConstants } from "node:fs";
import {
  access,
  lstat,
  mkdir,
  open,
  readFile,
  realpath,
  rename,
  rm,
} from "node:fs/promises";
import { createRequire } from "node:module";
import { basename, dirname, isAbsolute, join, relative, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const MAX_INPUT_BYTES = 2 * 1024 * 1024;
const MAX_TOOL_OUTPUT_BYTES = 1024 * 1024;
const EXPECTED_LIKEC4_VERSION = "1.59.1";
const EXPECTED_GRAPHVIZ_VERSION = "1.22.2";
const SOURCE_ROOT = "architecture/expansions/i5-06/likec4";
const PUBLISHED_ROOT = "architecture/expansions/i5-06/rendered";
const SOURCE_PATHS = Object.freeze([
  `${SOURCE_ROOT}/specification.c4`,
  `${SOURCE_ROOT}/model/architecture-curriculum.c4`,
  `${SOURCE_ROOT}/view-manifest.yaml`,
  `${SOURCE_ROOT}/views/C4-L2-AWS.c4`,
  `${SOURCE_ROOT}/views/DEP-AWS.c4`,
  `${SOURCE_ROOT}/views/DYN-OFFICE.c4`,
  `${SOURCE_ROOT}/views/DYN-PUBLISH.c4`,
  `${SOURCE_ROOT}/views/DYN-RESTORE.c4`,
]);

export const STAGE_A_VIEW_IDS = Object.freeze([
  "C4-L2-AWS",
  "DEP-AWS",
  "DYN-OFFICE",
  "DYN-PUBLISH",
  "DYN-RESTORE",
]);

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function stableJson(value) {
  return `${JSON.stringify(value, null, 2)}\n`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function decodeXml(value) {
  return value
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", '"')
    .replaceAll("&#39;", "'")
    .replace(/&#(\d+);/gu, (_match, codePoint) => String.fromCodePoint(Number(codePoint)))
    .replace(/&#x([0-9a-f]+);/giu, (_match, codePoint) => String.fromCodePoint(Number.parseInt(codePoint, 16)))
    .replaceAll("&amp;", "&");
}

function visibleXmlText(value) {
  return decodeXml(value.replace(/<[^>]*>/gu, " ").replace(/\s+/gu, " ").trim());
}

function assertSafeToken(value, label) {
  if (!/^[A-Za-z0-9._-]+$/u.test(value)) throw new Error(`${label} is unsafe`);
  return value;
}

async function pathExists(inputPath) {
  try {
    await lstat(inputPath);
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

async function regularFile(inputPath, maximum = MAX_INPUT_BYTES) {
  const metadata = await lstat(inputPath);
  if (!metadata.isFile() || metadata.isSymbolicLink()) throw new Error("input must be regular");
  if (metadata.size > maximum) throw new Error("input exceeds byte limit");
  return metadata;
}

async function privateDirectory(inputPath) {
  const canonical = await realpath(inputPath);
  const metadata = await lstat(canonical);
  if (!metadata.isDirectory() || metadata.isSymbolicLink() || (metadata.mode & 0o777) !== 0o700) {
    throw new Error("private directory must be real and mode 0700");
  }
  return canonical;
}

function inside(root, candidate, label) {
  const child = resolve(candidate);
  const childRelative = relative(root, child);
  if (!childRelative || childRelative.startsWith("..") || isAbsolute(childRelative)) {
    throw new Error(`${label} escaped or equals its root`);
  }
  return child;
}

export function visibleSemanticLines(source) {
  return source
    .split(/\r?\n/u)
    .map((line) => line.trim())
    .filter(
      (line) =>
        line.includes(" -> ") ||
        line.startsWith("deployment ") ||
        line.startsWith("group ") ||
        line.startsWith("deployment view ")
    );
}

export async function readBoundedText(inputPath) {
  if (!isAbsolute(inputPath)) throw new Error("input path must be absolute");
  await regularFile(inputPath);
  return await readFile(inputPath, "utf8");
}

export async function writeOwnedText(outputRoot, outputPath, value) {
  if (!isAbsolute(outputRoot) || !isAbsolute(outputPath)) throw new Error("output paths must be absolute");
  const canonicalRoot = await realpath(outputRoot);
  const target = inside(canonicalRoot, outputPath, "output");
  if (Buffer.byteLength(value, "utf8") > MAX_INPUT_BYTES) throw new Error("output exceeds byte limit");
  await mkdir(dirname(target), { recursive: true, mode: 0o700 });
  const temporary = `${target}.owned-${process.pid}`;
  const handle = await open(temporary, fsConstants.O_CREAT | fsConstants.O_EXCL | fsConstants.O_WRONLY, 0o600);
  try {
    await handle.writeFile(value, { encoding: "utf8" });
    await handle.sync();
  } finally {
    await handle.close();
  }
  await rename(temporary, target);
  await access(target, fsConstants.R_OK);
}

async function writePrivate(root, name, value) {
  const target = inside(root, join(root, name), "evidence");
  await mkdir(dirname(target), { recursive: true, mode: 0o700 });
  const handle = await open(target, fsConstants.O_CREAT | fsConstants.O_EXCL | fsConstants.O_WRONLY, 0o600);
  try {
    await handle.writeFile(value);
  } finally {
    await handle.close();
  }
}

function closedToolEnvironment(runtime) {
  return {
    PATH: "/usr/bin:/bin:/usr/sbin:/sbin",
    HOME: join(runtime, "home"),
    TMPDIR: join(runtime, "tmp"),
    XDG_CACHE_HOME: join(runtime, "cache"),
    TZ: "UTC",
    LC_ALL: "C.UTF-8",
    LANG: "C.UTF-8",
    NO_COLOR: "1",
    CI: "1",
  };
}

async function runTool(label, argv, cwd, environment, evidenceRoot, privateRoots) {
  const receipt = spawnSync(process.execPath, argv, {
    cwd,
    env: environment,
    encoding: null,
    input: Buffer.alloc(0),
    maxBuffer: MAX_TOOL_OUTPUT_BYTES,
    timeout: 120_000,
    windowsHide: true,
  });
  const stdout = receipt.stdout ?? Buffer.alloc(0);
  const stderr = receipt.stderr ?? Buffer.alloc(0);
  await writePrivate(evidenceRoot, `${label}.stdout.raw`, stdout);
  await writePrivate(evidenceRoot, `${label}.stderr.raw`, stderr);
  let sanitized = Buffer.concat([stdout, stderr]).toString("utf8");
  for (const privateRoot of privateRoots.sort((a, b) => b.length - a.length)) {
    sanitized = sanitized.replaceAll(privateRoot, "<PRIVATE_ROOT>");
  }
  await writePrivate(evidenceRoot, `${label}.sanitized.log`, sanitized);
  await writePrivate(
    evidenceRoot,
    `${label}.receipt.json`,
    stableJson({
      argv: argv.slice(1).map((item) => (isAbsolute(item) ? `<ABSOLUTE>/${basename(item)}` : item)),
      signal: receipt.signal ?? null,
      status: receipt.status,
      stderrBytes: stderr.length,
      stderrSha256: sha256(stderr),
      stdoutBytes: stdout.length,
      stdoutSha256: sha256(stdout),
    })
  );
  if (receipt.error || receipt.signal || receipt.status !== 0) {
    throw new Error(`${label} failed with status ${receipt.status ?? "none"}`);
  }
}

async function sourceIdentity(repositoryRoot) {
  const files = [];
  const digest = createHash("sha256");
  for (const relativePath of SOURCE_PATHS) {
    const absolutePath = inside(repositoryRoot, join(repositoryRoot, relativePath), "source");
    await regularFile(absolutePath);
    const bytes = await readFile(absolutePath);
    files.push({ bytes: bytes.length, path: relativePath, sha256: sha256(bytes) });
    digest.update(relativePath).update("\0").update(bytes).update("\0");
  }
  return { files, sha256: digest.digest("hex") };
}

function normalizeParentIds(nodes) {
  const groupIds = new Map(
    nodes.filter((node) => node.kind === "@group").map((node) => [node.id, `boundary:${node.title}`])
  );
  return nodes.map((node) => ({
    id: groupIds.get(node.id) ?? node.id,
    parent: node.parent === null ? null : groupIds.get(node.parent) ?? node.parent,
    title: node.title,
    kind: node.kind,
    technology: node.technology ?? null,
    children: (node.children ?? []).map((child) => groupIds.get(child) ?? child),
  }));
}

function projectView(view) {
  const nodes = normalizeParentIds(view.nodes ?? []);
  const relations = (view.edges ?? []).map((edge, index) => ({
    id: edge.id,
    ordinal: view._type === "dynamic" ? index : null,
    source: edge.source,
    target: edge.target,
    label: edge.label ?? null,
    technology: edge.technology ?? null,
    relationIds: [...(edge.relations ?? [])],
  }));
  const nodeIds = new Set(nodes.map((node) => node.id));
  if (nodeIds.size !== nodes.length) throw new Error(`duplicate node in ${view.id}`);
  const relationKeys = new Set();
  for (const relation of relations) {
    const key = [relation.source, relation.target, relation.label, relation.technology, relation.ordinal].join("\0");
    if (relationKeys.has(key)) throw new Error(`duplicate relation in ${view.id}`);
    relationKeys.add(key);
  }
  return {
    schemaVersion: "i5-06-likec4-projection-v1",
    viewId: view.id,
    type: view._type,
    title: view.title,
    description: view.description ?? null,
    autoLayout: view.autoLayout,
    nodes,
    relations,
  };
}

function assertDotParity(dot, rawProjection, projection) {
  const hasId = (id) => {
    const escaped = id.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&");
    return new RegExp(`likec4_id\\s*=\\s*(?:"${escaped}"|${escaped})(?:[,;\\]\\s]|$)`, "u").test(dot);
  };
  for (const node of rawProjection.nodes ?? []) {
    if (!hasId(node.id)) throw new Error(`DOT omitted node ${node.id}`);
  }
  const edgeBlocks = [...dot.matchAll(/^\s*(?:"([^"]+)"|([A-Za-z0-9_.:-]+))\s*->\s*(?:"([^"]+)"|([A-Za-z0-9_.:-]+))\s*\[([\s\S]*?)\];/gmu)].map(
    (match) => ({ source: match[1] ?? match[2], target: match[3] ?? match[4], body: match[5] })
  );
  for (const relation of rawProjection.edges ?? []) {
    if (!hasId(relation.id)) throw new Error(`DOT omitted relation ${relation.id}`);
    const escapedId = relation.id.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&");
    const edge = edgeBlocks.find((candidate) =>
      new RegExp(`likec4_id\\s*=\\s*(?:"${escapedId}"|${escapedId})(?:[,;\\]\\s]|$)`, "u").test(candidate.body)
    );
    if (!edge) throw new Error(`DOT relation block missing for ${relation.id}`);
    const source = relation.source.split(".").at(-1);
    const target = relation.target.split(".").at(-1);
    const forward = edge.source === source && edge.target === target;
    const reversed = edge.source === target && edge.target === source && /\bdir\s*=\s*"?back"?/u.test(edge.body);
    if (!forward && !reversed) throw new Error(`DOT relation endpoints drifted for ${relation.id}`);
  }
  if (!new RegExp(`likec4_viewId\\s*=\\s*"${projection.viewId}"`, "u").test(dot)) {
    throw new Error("DOT view identity mismatch");
  }
}

function assertVisibleParity(svg, projection) {
  const visible = visibleXmlText(svg);
  const includesVisible = (value) => visible.toLocaleLowerCase("vi").includes(value.toLocaleLowerCase("vi"));
  for (const node of projection.nodes) {
    if (!includesVisible(node.title)) throw new Error(`SVG omitted visible node ${node.id}`);
    if (node.technology && !includesVisible(node.technology)) throw new Error(`SVG omitted node technology ${node.id}`);
  }
  for (const relation of projection.relations) {
    if (relation.label && !includesVisible(relation.label)) throw new Error(`SVG omitted relation label ${relation.id}`);
    if (relation.technology && !includesVisible(relation.technology)) {
      throw new Error(`SVG omitted relation technology ${relation.id}`);
    }
  }
  const canonicalEndpoint = (source, target) =>
    [source.split(".").at(-1), target.split(".").at(-1)].sort().join("<->");
  const edgeEndpoints = [...svg.matchAll(/<g\b[^>]*\bclass="edge"[^>]*>[\s\S]*?<title>([\s\S]*?)<\/title>/gu)]
    .map((match) => decodeXml(match[1]).replace(/\s+/gu, "").trim().split("->"))
    .map(([source, target]) => canonicalEndpoint(source, target))
    .sort();
  const expectedEndpoints = projection.relations
    .map((relation) => canonicalEndpoint(relation.source, relation.target))
    .sort();
  if (edgeEndpoints.length !== expectedEndpoints.length || edgeEndpoints.some((value, index) => value !== expectedEndpoints[index])) {
    throw new Error(`SVG relation endpoint/order mismatch in ${projection.viewId}`);
  }
}

function normalizeSvg(rawSvg, projection) {
  if (/<!ENTITY|<script|<foreignObject|javascript:|\son[a-z]+\s*=|(?:href|src)\s*=\s*["'](?!#)/iu.test(rawSvg)) {
    throw new Error("unsafe SVG content");
  }
  let svg = rawSvg
    .replace(/^<\?xml[^>]*>\s*/u, "")
    .replace(/^<!DOCTYPE[^>]*(?:\[[\s\S]*?\]\s*)?>\s*/u, "")
    .replace(/<!-- Generated by graphviz[^>]*-->\s*/gu, "")
    .replaceAll("#3b82f6", "#dbeafe")
    .replaceAll("#eff6ff", "#111827")
    .replaceAll("#bfdbfe", "#1e3a8a")
    .replaceAll("#2563eb", "#1d4ed8")
    .replace(/#194b9e/giu, "#eff6ff")
    .replace(/#1b3d88/giu, "#1d4ed8")
    .replace(/#8d8d8d/giu, "#374151")
    .replace(/#c9c9c9/giu, "#111827")
    .replace(/#18191b/giu, "#f8fafc")
    .replace(/<svg\s+([^>]*?)>/u, (_match, attributes) => {
      const cleaned = attributes.replace(/\s+(?:role|aria-labelledby|preserveAspectRatio|style)="[^"]*"/gu, "");
      return `<svg ${cleaned} role="img" aria-labelledby="${projection.viewId}-title ${projection.viewId}-desc" preserveAspectRatio="xMidYMid meet" style="background:#ffffff;max-width:100%;height:auto">`;
    });
  const accessible = `<title id="${projection.viewId}-title">${escapeHtml(projection.title)} — ${projection.viewId}</title>\n<desc id="${projection.viewId}-desc">Sơ đồ ${projection.type} gồm ${projection.nodes.length} nút và ${projection.relations.length} quan hệ.</desc>`;
  svg = svg.replace(/(<svg[^>]*>)/u, `$1\n${accessible}`);
  if (!svg.endsWith("\n")) svg += "\n";
  assertVisibleParity(svg, projection);
  return svg;
}

function structuredText(projection) {
  const lines = [
    `${projection.title} — ${projection.viewId}`,
    `Loại view: ${projection.type}`,
    "Nút:",
    ...projection.nodes.map(
      (node, index) =>
        `${index + 1}. ${node.id} | ${node.title} | công nghệ=${node.technology ?? "không áp dụng"} | biên=${node.parent ?? "gốc"}`
    ),
    "Quan hệ:",
    ...projection.relations.map(
      (relation, index) =>
        `${relation.ordinal ?? index + 1}. ${relation.source} -> ${relation.target} | ${relation.label ?? "không nhãn"} | công nghệ=${relation.technology ?? "không áp dụng"}`
    ),
  ];
  return `${lines.join("\n")}\n`;
}

function fittedHtml(projection, svg, text, viewport) {
  return `<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHtml(projection.title)} — ${projection.viewId}</title>
<style>html{background:#fff;color:#111827;font:16px/1.5 Arial,sans-serif}body{box-sizing:border-box;margin:0 auto;max-width:${viewport}px;padding:24px}figure{margin:0}svg{display:block;max-width:100%;height:auto;margin:0 auto}figcaption{font-weight:700;margin:0 0 16px}pre{background:#f8fafc;border:1px solid #94a3b8;overflow-wrap:anywhere;padding:16px;white-space:pre-wrap}</style>
</head>
<body>
<main><figure><figcaption>${escapeHtml(projection.title)} — ${projection.viewId}</figcaption>${svg}</figure><pre>${escapeHtml(text)}</pre></main>
</body>
</html>
`;
}

async function atomicPublish(repositoryRoot, outputRoot, runId, files) {
  const runtime = await privateDirectory(process.env.I11_RUNTIME ?? "");
  const canonicalPublished = join(repositoryRoot, PUBLISHED_ROOT);
  const outputResolved = resolve(outputRoot);
  const publishToRepository = outputResolved === canonicalPublished;
  if (!publishToRepository) inside(runtime, outputResolved, "private publish root");
  const parent = dirname(outputResolved);
  await mkdir(parent, { recursive: true, mode: publishToRepository ? 0o755 : 0o700 });
  const stage = join(parent, `.rendered-stage-${runId}`);
  const backup = join(parent, `.rendered-backup-${runId}`);
  if ((await pathExists(stage)) || (await pathExists(backup))) {
    throw new Error("stale render transaction exists");
  }
  await mkdir(stage, { mode: 0o700 });
  try {
    for (const [name, value] of files) await writeOwnedText(stage, join(stage, name), value);
    const total = [...files.values()].reduce((sum, value) => sum + Buffer.byteLength(value), 0);
    if (files.size !== 11 || total > MAX_INPUT_BYTES) throw new Error("published render set is outside bounds");
    if (await pathExists(outputResolved)) await rename(outputResolved, backup);
    await rename(stage, outputResolved);
    await rm(backup, { recursive: true, force: true });
  } catch (error) {
    if (!(await pathExists(outputResolved)) && (await pathExists(backup))) {
      await rename(backup, outputResolved);
    }
    await rm(stage, { recursive: true, force: true });
    throw error;
  }
}

export async function renderLocked(repositoryPath, outputPath, evidencePath) {
  if (![repositoryPath, outputPath, evidencePath].every(isAbsolute)) throw new Error("render paths must be absolute");
  const repositoryRoot = await realpath(repositoryPath);
  const runtime = await privateDirectory(process.env.I11_RUNTIME ?? "");
  const toolRoot = await privateDirectory(process.env.I11_ARCH_TOOL_ROOT ?? "");
  const evidenceRoot = inside(runtime, evidencePath, "evidence root");
  if (await pathExists(evidenceRoot)) throw new Error("evidence root must be fresh");
  await mkdir(evidenceRoot, { recursive: false, mode: 0o700 });
  const runId = assertSafeToken(process.env.I11_RENDER_RUN_ID ?? "", "render run id");
  const sourceRoot = join(repositoryRoot, SOURCE_ROOT);
  const identity = await sourceIdentity(repositoryRoot);
  const repositoryLock = await readFile(join(repositoryRoot, "requirements/architecture/package-lock.json"));
  const toolLock = await readFile(join(toolRoot, "package-lock.json"));
  if (sha256(repositoryLock) !== sha256(toolLock)) throw new Error("tool lock identity mismatch");
  const likec4Package = JSON.parse(await readBoundedText(join(toolRoot, "node_modules/likec4/package.json")));
  const graphvizPackage = JSON.parse(
    await readBoundedText(join(toolRoot, "node_modules/@hpcc-js/wasm-graphviz/package.json"))
  );
  if (likec4Package.version !== EXPECTED_LIKEC4_VERSION) throw new Error("LikeC4 version mismatch");
  if (graphvizPackage.version !== EXPECTED_GRAPHVIZ_VERSION) throw new Error("Graphviz version mismatch");
  const exportPath = join(evidenceRoot, "likec4-export.json");
  const dotRoot = join(evidenceRoot, "dot");
  const cli = join(toolRoot, "node_modules/likec4/bin/likec4.mjs");
  await regularFile(cli, 16 * 1024 * 1024);
  const environment = closedToolEnvironment(runtime);
  await runTool(
    "likec4-export",
    [cli, "export", "json", "--skip-layout", "--pretty", "-o", exportPath, sourceRoot],
    repositoryRoot,
    environment,
    evidenceRoot,
    [repositoryRoot, runtime, toolRoot, evidenceRoot]
  );
  await runTool(
    "likec4-dot",
    [cli, "gen", "dot", "-o", dotRoot, sourceRoot],
    repositoryRoot,
    environment,
    evidenceRoot,
    [repositoryRoot, runtime, toolRoot, evidenceRoot]
  );
  const exported = JSON.parse(await readBoundedText(exportPath));
  const exportedIds = STAGE_A_VIEW_IDS.filter((viewId) => exported.views?.[viewId]);
  if (exportedIds.join("\0") !== STAGE_A_VIEW_IDS.join("\0")) throw new Error("five-view export mismatch");
  const requireFromTool = createRequire(join(toolRoot, "package.json"));
  const { Graphviz } = requireFromTool("@hpcc-js/wasm-graphviz");
  const graphviz = await Graphviz.load();
  const graphvizVersion = graphviz.version();
  const published = new Map();
  const manifestViews = [];
  for (const viewId of STAGE_A_VIEW_IDS) {
    const rawView = exported.views[viewId];
    const projection = projectView(rawView);
    const projectionBytes = stableJson(projection);
    const dot = await readBoundedText(join(dotRoot, "views", `${viewId}.dot`));
    assertDotParity(dot, rawView, projection);
    const rawSvg = graphviz.layout(dot, "svg", "dot");
    const repeatedRawSvg = graphviz.layout(dot, "svg", "dot");
    if (rawSvg !== repeatedRawSvg) throw new Error(`Graphviz produced nondeterministic SVG for ${viewId}`);
    assertVisibleParity(rawSvg, projection);
    const svg = normalizeSvg(rawSvg, projection);
    const text = structuredText(projection);
    const html1440 = fittedHtml(projection, svg, text, 1440);
    const html1024 = fittedHtml(projection, svg, text, 1024);
    if (/<script|<foreignObject|javascript:|\son[a-z]+\s*=/iu.test(`${svg}${html1440}${html1024}`)) {
      throw new Error("active render content rejected");
    }
    await writePrivate(evidenceRoot, `views/${viewId}.projection.json`, projectionBytes);
    await writePrivate(evidenceRoot, `views/${viewId}.dot`, dot);
    await writePrivate(evidenceRoot, `views/${viewId}.raw.svg`, rawSvg);
    await writePrivate(evidenceRoot, `views/${viewId}-1440.html`, html1440);
    await writePrivate(evidenceRoot, `views/${viewId}-1024.html`, html1024);
    published.set(`${viewId}.svg`, svg);
    published.set(`${viewId}.txt`, text);
    manifestViews.push({
      viewId,
      type: projection.type,
      nodes: projection.nodes.length,
      relations: projection.relations.length,
      projectionSha256: sha256(projectionBytes),
      dotSha256: sha256(dot),
      rawSvgSha256: sha256(rawSvg),
      svgSha256: sha256(svg),
      textSha256: sha256(text),
      fittedHtmlSha256: { "1024": sha256(html1024), "1440": sha256(html1440) },
    });
  }
  const toolIdentity = {
    graphvizPackage: graphvizPackage.version,
    graphvizRuntime: graphvizVersion,
    likec4: likec4Package.version,
    node: process.version,
    packageLockSha256: sha256(repositoryLock),
  };
  await writePrivate(
    evidenceRoot,
    "tool-identities.raw.json",
    stableJson({ ...toolIdentity, nodeExecutable: process.execPath, toolRoot })
  );
  await writePrivate(
    evidenceRoot,
    "tool-identities.sanitized.json",
    stableJson({ ...toolIdentity, nodeExecutable: "<NODE_EXECUTABLE>", toolRoot: "<PRIVATE_TOOL_ROOT>" })
  );
  const manifest = {
    schemaVersion: "i5-06-render-manifest-v2",
    renderer: "locked-likec4-dot-wasm-graphviz",
    deterministicRuns: 2,
    inProcessGraphvizPasses: 2,
    viewports: [1440, 1024],
    normalization: [
      "strip-xml-declaration-doctype-and-graphviz-generator-comment",
      "add-svg-title-description-role-and-responsive-fit",
      "map-locked-likec4-palette-to-wcag-readable-light-palette",
    ],
    sourceSha256: identity.sha256,
    sourceFiles: identity.files,
    toolIdentity,
    views: manifestViews,
  };
  const manifestBytes = stableJson(manifest);
  published.set("render-manifest.json", manifestBytes);
  await writePrivate(evidenceRoot, "render-manifest.json", manifestBytes);
  await atomicPublish(repositoryRoot, outputPath, runId, published);
  return manifest;
}

export async function main(argv = process.argv.slice(2)) {
  if (argv[0] === "copy-bounded" && argv.length === 3) {
    const input = resolve(argv[1]);
    const output = resolve(argv[2]);
    const sourceRoot = await realpath(process.cwd());
    const runtime = await privateDirectory(process.env.I11_RUNTIME ?? "");
    inside(sourceRoot, input, "input");
    await writeOwnedText(runtime, output, await readBoundedText(input));
    return;
  }
  if (argv[0] === "render" && argv.length === 4) {
    const result = await renderLocked(resolve(argv[1]), resolve(argv[2]), resolve(argv[3]));
    process.stdout.write(`${stableJson({ renderer: result.renderer, views: result.views.length })}`);
    return;
  }
  throw new Error("expected copy-bounded <absolute-input> <absolute-output> or render <repository> <output> <evidence>");
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) await main();
