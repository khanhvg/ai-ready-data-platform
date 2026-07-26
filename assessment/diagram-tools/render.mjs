import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  closeSync,
  copyFileSync,
  existsSync,
  fsyncSync,
  fstatSync,
  mkdtempSync,
  openSync,
  readSync,
  readFileSync,
  readdirSync,
  renameSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import os from "node:os";
import path from "node:path";
import net from "node:net";
import { fileURLToPath, pathToFileURL } from "node:url";

const TOOLS_ROOT = path.dirname(fileURLToPath(import.meta.url));
const ASSESSMENT_ROOT = path.dirname(TOOLS_ROOT);
const CONTENT_ROOT = path.join(
  ASSESSMENT_ROOT,
  "src",
  "assessment",
  "content",
  "catalog",
  "1.0.0",
  "diagrams",
);
const CONFIG_PATH = path.join(TOOLS_ROOT, "mermaid-config.json");
const MMDC_PATH = path.join(TOOLS_ROOT, "node_modules", ".bin", "mmdc");
const LOOPBACK_WRAPPER = path.join(
  ASSESSMENT_ROOT,
  "tools",
  "run-loopback-only.sh",
);
const EXPECTED_NODE_MAJOR = 22;
const MERMAID_CLI_VERSION = "11.16.0";
const PUPPETEER_VERSION = "25.3.0";
const LOOPBACK_CAPABILITY = "assessment-loopback-capability-v1\n";
const DIAGRAMS = [
  {
    id: "demo-evidence-mapping",
    title: "Demo evidence to catalog mapping",
    description:
      "Read-only sandbox artifacts illustrate ingestion, quality, lineage, governance, access, serving, and AI-ready publication patterns but never affect customer scores.",
  },
  {
    id: "engagement-lifecycle",
    title: "Architect engagement lifecycle",
    description:
      "An architect creates an engagement, records assessment evidence, reviews deterministic findings, plans deep dives, generates a report, and exports a portable archive.",
  },
  {
    id: "executive-ai-readiness",
    title: "Executive AI readiness decision flow",
    description:
      "Ten capability domains inform maturity, critical gates cap readiness, and accepted findings become a sequenced roadmap.",
  },
  {
    id: "logical-platform-context",
    title: "Vendor-neutral logical platform context",
    description:
      "Sources pass through integration, governed data products, and consumption while control planes provide quality, metadata, security, and operations.",
  },
  {
    id: "metadata-and-lineage",
    title: "Metadata and source-to-product lineage",
    description:
      "Source contracts, transformation metadata, product definitions, and run evidence combine into catalog and lineage views used for impact analysis.",
  },
  {
    id: "scoring-and-gates",
    title: "Scoring and readiness gate separation",
    description:
      "Customer answers determine maturity, evidence status determines confidence, diagnostic facts and domain scores drive gates, and demo illustrations never score.",
  },
  {
    id: "security-and-access",
    title: "Security privacy and access control pattern",
    description:
      "Classified data and approved purposes feed policy decisions that allow masked governed products or deny raw sensitive access while recording evidence.",
  },
];
const SOURCE_FORBIDDEN = [
  /%%\{/i,
  /\bclick\b/i,
  /<[^>]+>/,
  /https?:|www\.|file:|data:|javascript:/i,
  /!\[[^\]]*\]\(/,
  /\[[^\]]+\]\(/,
  /\bicon\b/i,
];
const SVG_FORBIDDEN = [
  /<!DOCTYPE|<!ENTITY|<\?|<!--|<metadata\b/i,
  /<(?:script|foreignObject|image|iframe|object|embed|audio|video|a|use|animate|set)\b/i,
  /\son[a-z]+\s*=/i,
  /\b(?:href|xlink:href|src)\s*=/i,
  /javascript:|data:|file:|https?:\/\/|\/(?:Users|home|private|tmp)\/|[A-Z]:\\/i,
  /@import|@font-face/i,
  /url\(\s*(?!#)[^)]+\)/i,
];

function fail(message) {
  throw new Error(message);
}

function sha256(content) {
  return createHash("sha256").update(content).digest("hex");
}

function xmlEscape(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

async function assertOutboundNetworkDenied() {
  await new Promise((resolve, reject) => {
    const socket = net.connect({ host: "1.1.1.1", port: 443 });
    const timer = setTimeout(() => {
      socket.destroy();
      reject(
        new Error(
          "diagram rendering cannot prove that outbound networking is denied",
        ),
      );
    }, 1_000);
    socket.once("connect", () => {
      clearTimeout(timer);
      socket.destroy();
      reject(new Error("diagram rendering detected usable outbound networking"));
    });
    socket.once("error", (error) => {
      clearTimeout(timer);
      if (error.code === "EPERM" || error.code === "EACCES") {
        resolve();
        return;
      }
      reject(
        new Error(
          `diagram rendering cannot prove network denial: ${error.code ?? "unknown"}`,
        ),
      );
    });
  });
}

async function validateEnvironment() {
  if (process.env.ASSESSMENT_LOOPBACK_SANDBOX !== "1") {
    fail("diagram rendering requires the repository network-denying wrapper");
  }
  const capabilityDescriptor = Number.parseInt(
    process.env.ASSESSMENT_LOOPBACK_CAPABILITY_FD ?? "",
    10,
  );
  if (!Number.isInteger(capabilityDescriptor) || capabilityDescriptor < 3) {
    fail("diagram rendering requires an inherited sandbox capability");
  }
  let capability;
  try {
    fstatSync(capabilityDescriptor);
    const buffer = Buffer.alloc(LOOPBACK_CAPABILITY.length);
    const bytesRead = readSync(
      capabilityDescriptor,
      buffer,
      0,
      buffer.length,
      null,
    );
    capability = buffer.subarray(0, bytesRead).toString("utf8");
  } catch {
    fail("diagram rendering requires a valid inherited sandbox capability");
  } finally {
    try {
      closeSync(capabilityDescriptor);
    } catch {
      // The error path is reported above; there is nothing else to release.
    }
  }
  if (capability !== LOOPBACK_CAPABILITY) {
    fail("diagram rendering rejected the inherited sandbox capability");
  }
  await assertOutboundNetworkDenied();
  const nodeMajor = Number.parseInt(process.versions.node.split(".")[0], 10);
  if (nodeMajor !== EXPECTED_NODE_MAJOR) {
    fail(`diagram renderer requires Node major ${EXPECTED_NODE_MAJOR}`);
  }
  if (!existsSync(MMDC_PATH)) {
    fail("diagram toolchain is not installed; run make assessment-diagram-install");
  }
}

function runInsideNetworkSandbox(mode) {
  const result = spawnSync(
    LOOPBACK_WRAPPER,
    [
      process.execPath,
      fileURLToPath(import.meta.url),
      mode === "--update" ? "--sandboxed-update" : "--sandboxed-verify",
    ],
    {
      cwd: TOOLS_ROOT,
      env: {
        ...process.env,
        ASSESSMENT_LOOPBACK_SANDBOX: "",
        ASSESSMENT_LOOPBACK_CAPABILITY_FD: "",
      },
      stdio: "inherit",
      timeout: 180_000,
    },
  );
  if (result.status !== 0) {
    fail(`diagram sandboxed render failed with status ${result.status}`);
  }
}

function walkDirectories(root, depth = 0) {
  if (depth > 6 || !existsSync(root)) {
    return [];
  }
  const results = [];
  for (const name of readdirSync(root)) {
    const candidate = path.join(root, name);
    let stat;
    try {
      stat = statSync(candidate);
    } catch {
      continue;
    }
    if (stat.isDirectory()) {
      results.push(...walkDirectories(candidate, depth + 1));
    } else if (
      stat.isFile() &&
      (
        name === "chrome-headless-shell" ||
        name === "chrome" ||
        name === "Google Chrome for Testing"
      )
    ) {
      results.push(candidate);
    }
  }
  return results;
}

function chromiumExecutable() {
  const explicit = process.env.PUPPETEER_EXECUTABLE_PATH;
  if (explicit) {
    const resolved = path.resolve(explicit);
    if (!existsSync(resolved)) {
      fail("PUPPETEER_EXECUTABLE_PATH does not identify a file");
    }
    return resolved;
  }
  const browserRoot = path.join(ASSESSMENT_ROOT, ".browser", "chromium-1228");
  const candidates = walkDirectories(browserRoot).sort();
  if (candidates.length !== 1) {
    fail(
      `expected exactly one Playwright chromium-1228 executable, found ${candidates.length}; ` +
        "run make assessment-browser-install",
    );
  }
  return candidates[0];
}

export function validateSource(source, diagram) {
  if (!source.startsWith("flowchart ")) {
    fail(`${diagram.id}: only flowchart sources are allowed`);
  }
  if (!source.includes(`accTitle: ${diagram.title}`)) {
    fail(`${diagram.id}: accessible title is missing or changed`);
  }
  if (!source.includes(`accDescr: ${diagram.description}`)) {
    fail(`${diagram.id}: accessible description is missing or changed`);
  }
  for (const pattern of SOURCE_FORBIDDEN) {
    if (pattern.test(source)) {
      fail(`${diagram.id}: source contains forbidden content ${pattern}`);
    }
  }
}

export function normalizeSvg(raw, diagram) {
  let svg = raw.replaceAll("\r\n", "\n").trim();
  svg = svg.replace(/<title\b[^>]*>[\s\S]*?<\/title>/gi, "");
  svg = svg.replace(/<desc\b[^>]*>[\s\S]*?<\/desc>/gi, "");
  const root = svg.match(/^<svg\b([^>]*)>/i);
  if (!root) {
    fail(`${diagram.id}: rendered output does not start with svg`);
  }
  let attributes = root[1]
    .replace(/\sxmlns(?::xlink)?=(?:"[^"]*"|'[^']*')/gi, "")
    .replace(/\srole=(?:"[^"]*"|'[^']*')/gi, "")
    .replace(
      /\saria-(?:describedby|labelledby|hidden|roledescription)=(?:"[^"]*"|'[^']*')/gi,
      "",
    )
    .trim();
  attributes = attributes ? ` ${attributes}` : "";
  const titleId = `${diagram.id}-title`;
  const descriptionId = `${diagram.id}-description`;
  const opening =
    `<svg xmlns="http://www.w3.org/2000/svg" role="img" ` +
    `aria-labelledby="${titleId} ${descriptionId}"${attributes}>` +
    `<title id="${titleId}">${xmlEscape(diagram.title)}</title>` +
    `<desc id="${descriptionId}">${xmlEscape(diagram.description)}</desc>`;
  svg = opening + svg.slice(root[0].length);
  const securityScan = svg
    .replaceAll("http://www.w3.org/2000/svg", "")
    .replaceAll("http://www.w3.org/1999/xlink", "")
    .replaceAll("http://www.w3.org/XML/1998/namespace", "");
  for (const pattern of SVG_FORBIDDEN) {
    if (pattern.test(securityScan)) {
      fail(`${diagram.id}: normalized SVG contains forbidden content ${pattern}`);
    }
  }
  if (!svg.endsWith("</svg>")) {
    fail(`${diagram.id}: normalized SVG is incomplete`);
  }
  return `${svg}\n`;
}

function renderOne(diagram, destination, executable) {
  const sourcePath = path.join(CONTENT_ROOT, `${diagram.id}.mmd`);
  const source = readFileSync(sourcePath, "utf8").replaceAll("\r\n", "\n");
  validateSource(source, diagram);
  const rawOutput = path.join(destination, `${diagram.id}.svg`);
  const puppeteerConfig = path.join(destination, "puppeteer-config.json");
  writeFileSync(
    puppeteerConfig,
    `${JSON.stringify(
      {
        // Chromium cannot initialize its inner Seatbelt profile from inside the
        // repository's outer macOS sandbox. The renderer therefore requires the
        // verified outer network-denying wrapper before using these flags.
        args: ["--disable-gpu", "--disable-setuid-sandbox", "--no-sandbox"],
        executablePath: executable,
      },
      null,
      2,
    )}\n`,
    "utf8",
  );
  const result = spawnSync(
    MMDC_PATH,
    [
      "--input",
      sourcePath,
      "--output",
      rawOutput,
      "--configFile",
      CONFIG_PATH,
      "--puppeteerConfigFile",
      puppeteerConfig,
      "--backgroundColor",
      "white",
      "--svgId",
      diagram.id,
      "--width",
      "1200",
      "--height",
      "700",
      "--scale",
      "1",
      "--quiet",
    ],
    {
      cwd: TOOLS_ROOT,
      encoding: "utf8",
      env: { ...process.env, NO_PROXY: "*", no_proxy: "*" },
      timeout: 60_000,
    },
  );
  if (result.status !== 0) {
    fail(`${diagram.id}: Mermaid render failed: ${result.stderr || result.stdout}`);
  }
  const normalized = normalizeSvg(readFileSync(rawOutput, "utf8"), diagram);
  writeFileSync(rawOutput, normalized, "utf8");
  return {
    id: diagram.id,
    source: `diagrams/${diagram.id}.mmd`,
    output: `diagrams/${diagram.id}.svg`,
    source_sha256: sha256(Buffer.from(source, "utf8")),
    output_sha256: sha256(Buffer.from(normalized, "utf8")),
  };
}

function toolDigest(name) {
  return sha256(readFileSync(path.join(TOOLS_ROOT, name)));
}

function buildManifest(diagrams) {
  return {
    schema_version: "1.0.0",
    node_major: EXPECTED_NODE_MAJOR,
    mermaid_cli_version: MERMAID_CLI_VERSION,
    packages: {
      "@mermaid-js/mermaid-cli": MERMAID_CLI_VERSION,
      puppeteer: PUPPETEER_VERSION,
    },
    browser: {
      provisioner: "assessment-browser-install",
      revision: "playwright-chromium-1228",
    },
    tool_files: {
      "mermaid-config.json": toolDigest("mermaid-config.json"),
      "package-lock.json": toolDigest("package-lock.json"),
      "package.json": toolDigest("package.json"),
      "render.mjs": toolDigest("render.mjs"),
      "render.test.mjs": toolDigest("render.test.mjs"),
    },
    diagrams,
  };
}

function atomicReplace(source, destination) {
  const temporary = `${destination}.phase5-tmp`;
  copyFileSync(source, temporary);
  const descriptor = openSync(temporary, "r");
  try {
    fsyncSync(descriptor);
  } finally {
    closeSync(descriptor);
  }
  renameSync(temporary, destination);
}

function compareBytes(actualPath, expectedPath, label) {
  const actual = readFileSync(actualPath);
  const expected = readFileSync(expectedPath);
  if (!actual.equals(expected)) {
    fail(`${label}: committed bytes differ from deterministic render`);
  }
}

async function main() {
  const requestedMode = process.argv[2];
  if (["--update", "--verify"].includes(requestedMode)) {
    runInsideNetworkSandbox(requestedMode);
    return;
  }
  const mode = {
    "--sandboxed-update": "--update",
    "--sandboxed-verify": "--verify",
  }[requestedMode];
  if (mode === undefined) {
    fail("usage: node render.mjs --update|--verify");
  }
  await validateEnvironment();
  const executable = chromiumExecutable();
  const firstRoot = mkdtempSync(path.join(os.tmpdir(), "assessment-diagrams-first-"));
  const secondRoot = mkdtempSync(path.join(os.tmpdir(), "assessment-diagrams-second-"));
  try {
    const first = DIAGRAMS.map((diagram) => renderOne(diagram, firstRoot, executable));
    const second = DIAGRAMS.map((diagram) => renderOne(diagram, secondRoot, executable));
    for (const diagram of DIAGRAMS) {
      compareBytes(
        path.join(firstRoot, `${diagram.id}.svg`),
        path.join(secondRoot, `${diagram.id}.svg`),
        `${diagram.id}: consecutive render`,
      );
    }
    const manifest = `${JSON.stringify(buildManifest(first), null, 2)}\n`;
    const temporaryManifest = path.join(firstRoot, "render-manifest.json");
    writeFileSync(temporaryManifest, manifest, "utf8");
    if (mode === "--verify") {
      for (const diagram of DIAGRAMS) {
        compareBytes(
          path.join(firstRoot, `${diagram.id}.svg`),
          path.join(CONTENT_ROOT, `${diagram.id}.svg`),
          diagram.id,
        );
      }
      compareBytes(
        temporaryManifest,
        path.join(CONTENT_ROOT, "render-manifest.json"),
        "render manifest",
      );
      process.stdout.write("assessment-diagrams PASS: 7 deterministic reviewed pairs\n");
      return;
    }
    for (const diagram of DIAGRAMS) {
      atomicReplace(
        path.join(firstRoot, `${diagram.id}.svg`),
        path.join(CONTENT_ROOT, `${diagram.id}.svg`),
      );
    }
    atomicReplace(temporaryManifest, path.join(CONTENT_ROOT, "render-manifest.json"));
    process.stdout.write("assessment-diagrams-update PASS: 7 reviewed pairs updated\n");
  } finally {
    rmSync(firstRoot, { force: true, recursive: true });
    rmSync(secondRoot, { force: true, recursive: true });
  }
}

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  main().catch((error) => {
    process.stderr.write(`${error.stack ?? error}\n`);
    process.exitCode = 1;
  });
}
