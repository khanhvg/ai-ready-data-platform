import { constants as fsConstants } from "node:fs";
import { access, lstat, mkdir, open, realpath, rename } from "node:fs/promises";
import { dirname, isAbsolute, relative, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const MAX_INPUT_BYTES = 2 * 1024 * 1024;
export const STAGE_A_VIEW_IDS = Object.freeze([
  "C4-L2-AWS",
  "DEP-AWS",
  "DYN-OFFICE",
  "DYN-PUBLISH",
  "DYN-RESTORE",
]);

export function visibleSemanticLines(source) {
  return source
    .split(/\r?\n/u)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("relation ") || line.startsWith("deployment ") || line.startsWith("boundary "));
}

export async function readBoundedText(inputPath) {
  if (!isAbsolute(inputPath)) throw new Error("input path must be absolute");
  const metadata = await lstat(inputPath);
  if (!metadata.isFile() || metadata.isSymbolicLink()) throw new Error("input must be regular");
  if (metadata.size > MAX_INPUT_BYTES) throw new Error("input exceeds byte limit");
  const handle = await open(inputPath, fsConstants.O_RDONLY);
  try {
    return await handle.readFile({ encoding: "utf8" });
  } finally {
    await handle.close();
  }
}

export async function writeOwnedText(outputRoot, outputPath, value) {
  if (!isAbsolute(outputRoot) || !isAbsolute(outputPath)) {
    throw new Error("output paths must be absolute");
  }
  const canonicalRoot = await realpath(outputRoot);
  const target = resolve(outputPath);
  const targetRelative = relative(canonicalRoot, target);
  if (targetRelative.startsWith("..") || isAbsolute(targetRelative)) {
    throw new Error("output escaped its root");
  }
  if (Buffer.byteLength(value, "utf8") > MAX_INPUT_BYTES) {
    throw new Error("output exceeds byte limit");
  }
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

export async function main(argv = process.argv.slice(2)) {
  if (argv.length !== 3 || argv[0] !== "copy-bounded") {
    throw new Error("expected: copy-bounded <absolute-input> <absolute-output>");
  }
  const input = resolve(argv[1]);
  const output = resolve(argv[2]);
  const sourceRoot = await realpath(process.cwd());
  const runtimeValue = process.env.I11_RUNTIME;
  if (!runtimeValue || !isAbsolute(runtimeValue)) throw new Error("admitted runtime is required");
  const outputRoot = await realpath(runtimeValue);
  const runtimeMetadata = await lstat(outputRoot);
  if (!runtimeMetadata.isDirectory() || (runtimeMetadata.mode & 0o777) !== 0o700) {
    throw new Error("admitted runtime must be a private directory");
  }
  const inputRelative = relative(sourceRoot, input);
  if (inputRelative.startsWith("..") || isAbsolute(inputRelative)) {
    throw new Error("input escaped the repository");
  }
  const value = await readBoundedText(input);
  await writeOwnedText(outputRoot, output, value);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  await main();
}
