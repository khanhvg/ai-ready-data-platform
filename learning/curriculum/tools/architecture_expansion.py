from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

import yaml

from .content_io import ContentError, ROOT, canonical_bytes, load_json, sha256_bytes, sha256_file


RELEASE_SHA = "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
VIEW_IDS = ("C4-L2-AWS", "DEP-AWS", "DYN-OFFICE", "DYN-PUBLISH", "DYN-RESTORE")
VIEW_KEYS = ("c4_l2_aws", "dep_aws", "dyn_office", "dyn_publish", "dyn_restore")
BASE_IDS = ("C4-L0", "C4-L1", "C4-L2-LOCAL", "C4-L3-RUNNER", "DEP-LOCAL", "DYN-JOURNEY")
TOOL_PATHS = (
    "requirements/architecture/package.json", "requirements/architecture/package-lock.json",
    "scripts/golden/architecture-render.mjs", "scripts/golden/architecture_check.py",
    "scripts/golden/architecture_finalize.py", "scripts/golden/architecture_pipeline.py",
    "scripts/golden/architecture_render.py", "mk/issue-5/i5-01.mk",
)
BASE_PATHS = (
    "architecture/likec4/specification.c4",
    "architecture/likec4/model/people-and-systems.c4",
    "architecture/likec4/model/learning-platform.c4",
    "architecture/likec4/model/data-platform.c4",
    "architecture/likec4/model/local-deployment.c4",
    "architecture/likec4/view-manifest.yaml",
    *(f"architecture/likec4/views/{view_id}.c4" for view_id in BASE_IDS),
    *(f"architecture/rendered/{view_id}.{extension}" for view_id in BASE_IDS for extension in ("svg", "txt")),
    "architecture/rendered/render-manifest.json",
)
PRIVATE_OR_UNSAFE = re.compile(r"(?i)(?:/Users/|/home/|file://|https?://|data:(?:text|image|application)/|<\s*script|<\s*foreignObject|on[a-z]+\s*=)")
NODE_ARCHIVE = "node-v22.22.3-darwin-arm64.tar.xz"
NODE_ARCHIVE_SHA256 = "753c1629e168cc788ccc46ab61e0b35549fce08c07f82fcd3bb0d41f7fb01e7b"


class ArchitectureExpansionError(ValueError):
    """Stable expansion checker/renderer error."""


def _run(command: list[str], cwd: pathlib.Path, env: dict[str, str] | None = None, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    if len(result.stdout.encode()) > 1024 * 1024:
        raise ArchitectureExpansionError("ARCH_OUTPUT_BOUNDS_INVALID")
    if result.returncode:
        excerpt = result.stdout[-16384:]
        raise ArchitectureExpansionError(f"ARCH_RENDER_FAILED:{sha256_bytes(result.stdout.encode())}:{excerpt}")
    return result


def _git_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{RELEASE_SHA}:{path}"], cwd=ROOT)


def _check_protected(root: pathlib.Path) -> None:
    if len(BASE_PATHS) != 25 or len(TOOL_PATHS) != 8:
        raise ArchitectureExpansionError("PROTECTED_BYTES_CHANGED")
    for relative in (*BASE_PATHS, *TOOL_PATHS):
        candidate = root / relative
        if not candidate.exists() and relative in TOOL_PATHS and root != ROOT:
            candidate = ROOT / relative
        try:
            actual = candidate.read_bytes()
        except OSError as exc:
            raise ArchitectureExpansionError("PROTECTED_BYTES_CHANGED") from exc
        expected = _git_bytes(relative)
        if actual != expected:
            raise ArchitectureExpansionError("PROTECTED_BYTES_CHANGED")


def _source_closure(root: pathlib.Path) -> str:
    paths = [
        *(path for path in (root / "architecture/likec4").rglob("*.c4")),
        *(path for path in (root / "architecture/expansions/i5-06/likec4").rglob("*.c4")),
        root / "architecture/expansions/i5-06/likec4/view-manifest.yaml",
        ROOT / "learning/curriculum/tools/architecture-render.mjs",
        ROOT / "requirements/architecture/package-lock.json",
    ]
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.as_posix()):
        if not path.is_file():
            raise ArchitectureExpansionError("ARCH_SOURCE_STALE")
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _compose(root: pathlib.Path, destination: pathlib.Path) -> pathlib.Path:
    source = destination / "source"
    shutil.copytree(root / "architecture/likec4", source)
    extension = root / "architecture/expansions/i5-06/likec4"
    shutil.copyfile(extension / "model/architecture-curriculum.c4", source / "model/architecture-curriculum.c4")
    for view_id in VIEW_IDS:
        shutil.copyfile(extension / f"views/{view_id}.c4", source / f"views/{view_id}.c4")
    return source


def _cache_root() -> pathlib.Path:
    sys.path.insert(0, str(ROOT / "scripts/golden"))
    import workspace

    parent = ROOT / ".artifacts/workspaces/i5-06-render-cache"
    candidates = [] if not parent.exists() else [child for child in parent.iterdir() if child.is_dir() and not child.is_symlink()]
    if not candidates:
        owner = workspace.allocate_family(("workspaces", "i5-06-render-cache"), "i5-06-render-cache")
        path = owner.path
        owner.close()
    elif len(candidates) == 1:
        path = candidates[0]
    else:
        raise ArchitectureExpansionError("ARCH_TOOL_CACHE_INVALID")
    marker = json.loads((path / ".golden-owner.json").read_text())
    if marker.get("purpose") != "i5-06-render-cache" or marker.get("runId") != path.name or path.stat().st_mode & 0o077:
        raise ArchitectureExpansionError("ARCH_TOOL_CACHE_INVALID")
    return path


def _bootstrap_node(stage: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]:
    sys.path.insert(0, str(ROOT / "scripts/golden"))
    from architecture_pipeline import safe_extract

    cache = _cache_root()
    archive = cache / NODE_ARCHIVE
    if not archive.exists():
        temporary = cache / f".{NODE_ARCHIVE}.partial"
        with urllib.request.urlopen(f"https://nodejs.org/download/release/v22.22.3/{NODE_ARCHIVE}", timeout=30) as response, temporary.open("xb") as target:
            shutil.copyfileobj(response, target)
        if sha256_file(temporary) != NODE_ARCHIVE_SHA256:
            temporary.unlink()
            raise ArchitectureExpansionError("ARCH_TOOL_LOCK_MISMATCH")
        os.replace(temporary, archive)
    if sha256_file(archive) != NODE_ARCHIVE_SHA256:
        raise ArchitectureExpansionError("ARCH_TOOL_LOCK_MISMATCH")
    extraction = cache / "node"
    if not extraction.exists():
        extraction.mkdir(mode=0o700)
        safe_extract(archive, extraction)
    node = extraction / "node-v22.22.3-darwin-arm64"
    if not (node / "bin/node").is_file() or not (node / "bin/npm").is_file():
        raise ArchitectureExpansionError("ARCH_TOOL_MISSING")
    npm_cache = cache / "npm-cache"
    npm_cache.mkdir(mode=0o700, exist_ok=True)
    return node, npm_cache


def _tool_environment(tool: pathlib.Path, node: pathlib.Path, npm_cache: pathlib.Path) -> dict[str, str]:
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise ArchitectureExpansionError("ARCH_TOOL_MISSING")
    if subprocess.check_output([str(node / "bin/node"), "--version"], text=True).strip() != "v22.22.3" or subprocess.check_output([str(node / "bin/npm"), "--version"], text=True).strip() != "10.9.8":
        raise ArchitectureExpansionError("ARCH_NODE_VERSION_MISMATCH")
    shutil.copyfile(ROOT / "requirements/architecture/package.json", tool / "package.json")
    shutil.copyfile(ROOT / "requirements/architecture/package-lock.json", tool / "package-lock.json")
    for name in ("home", "tmp"):
        (tool / name).mkdir(mode=0o700)
    env = {
        "PATH": f"{node / 'bin'}:/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(tool / "home"), "TMPDIR": str(tool / "tmp"), "TZ": "UTC",
        "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8", "npm_config_cache": str(npm_cache),
        "npm_config_audit": "false", "npm_config_fund": "false", "npm_config_ignore_scripts": "true",
    }
    _run([str(node / "bin/npm"), "ci", "--ignore-scripts", "--no-audit", "--no-fund"], tool, env, 180)
    return env


def _semantic_text(external: str, row: dict[str, Any], view: dict[str, Any]) -> bytes:
    lines = [
        f"ID: {external}", f"Title: {view['title']}", f"Type: {row['type']}",
        f"Audience: {row['audienceVi']}", f"Concern: {row['concernId']}", f"Scope: {row['scope']}",
        "Owner: I5-06", "Legend: elements are boxes; labelled arrows are directed relations; numbers preserve dynamic order.", "",
        "Elements:",
    ]
    for node in sorted(view["nodes"], key=lambda item: item["id"]):
        description = (node.get("description") or {}).get("txt", "")
        lines.append(f"- {node['id']} | {node.get('kind', 'element')} | {node['title']} | {description} | parent={node.get('parent') or 'none'}")
    lines.extend(["", "Relations:"])
    dynamic = view.get("_type") == "dynamic"
    relations = view["edges"] if dynamic else sorted(view["edges"], key=lambda edge: (edge["source"], edge["target"], edge.get("label") or ""))
    for ordinal, edge in enumerate(relations, 1):
        prefix = f"{ordinal}. " if dynamic else "- "
        technology = (edge.get("description") or {}).get("txt", "")
        lines.append(f"{prefix}{edge.get('label') or 'relation'}: {edge['source']} -> {edge['target']} | {technology or 'not-specified'}")
    if row["type"] == "deployment":
        lines.extend(["", "Deployment hierarchy:"])
        for node in sorted(view["nodes"], key=lambda item: (item.get("parent") or "", item["id"])):
            lines.append(f"- {node['id']} parent={node.get('parent') or 'environment-root'}")
    lines.extend([
        "", "Limitations: descriptive Stage A architecture only; no portal, executable lab, deployment, account, endpoint, or provider action.",
        "TBCs: hosted identity, tenant isolation, measured capacity, RTO, RPO, and current cost require later owner evidence.",
    ])
    return (unicodedata.normalize("NFC", "\n".join(lines)).rstrip() + "\n").encode()


def _semantic_projection(view: dict[str, Any]) -> dict[str, Any]:
    """Exclude LikeC4's ephemeral export metadata from the content identity."""
    nodes = [
        {
            "id": node["id"],
            "kind": node.get("kind"),
            "title": node["title"],
            "description": (node.get("description") or {}).get("txt", ""),
            "parent": node.get("parent"),
        }
        for node in view["nodes"]
    ]
    edges = [
        {
            "source": edge["source"],
            "target": edge["target"],
            "label": edge.get("label"),
            "description": (edge.get("description") or {}).get("txt", ""),
        }
        for edge in view["edges"]
    ]
    if view.get("_type") != "dynamic":
        edges.sort(key=lambda edge: (edge["source"], edge["target"], edge["label"] or ""))
    return {
        "type": view.get("_type"),
        "title": view["title"],
        "nodes": sorted(nodes, key=lambda node: node["id"]),
        "edges": edges,
    }


def _normalize_svg(raw: str, title: str, description: str) -> bytes:
    sys.path.insert(0, str(ROOT / "scripts/golden"))
    from architecture_render import normalize_svg

    normalized = normalize_svg(raw, title, description).decode()
    match = re.search(r'viewBox="([0-9.-]+) ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)"', normalized)
    if not match:
        raise ArchitectureExpansionError("ARCH_RENDER_FAILED")
    x, y, width, height = (float(item) for item in match.groups())
    if width <= 0 or height <= 0:
        raise ArchitectureExpansionError("ARCH_RENDER_FAILED")
    new_height = height + 32.0
    normalized = normalized.replace(match.group(0), f'viewBox="{x:.2f} {y:.2f} {width:.2f} {new_height:.2f}"', 1)
    normalized = normalized.replace('<g id="graph0"', '<g transform="translate(0 32)"><g id="graph0"', 1)
    legend = '<g id="legend"><text x="8" y="20" font-family="Arial" font-size="12">Legend: boxes are elements; arrows are ordered relations</text></g>'
    normalized = normalized.replace("</svg>", f"</g>{legend}</svg>")
    return (normalized.rstrip() + "\n").encode()


def _produce(root: pathlib.Path, stage: pathlib.Path) -> pathlib.Path:
    source = _compose(root, stage)
    node, npm_cache = _bootstrap_node(stage)
    tool = stage / "tool"
    tool.mkdir(mode=0o700)
    env = _tool_environment(tool, node, npm_cache)
    likec4 = tool / "node_modules/.bin/likec4"
    _run([str(likec4), "format", "--check", str(source)], ROOT, env)
    validation = _run([str(likec4), "validate", "--json", str(source)], ROOT, env)
    if '"valid": true' not in validation.stdout:
        raise ArchitectureExpansionError("ARCH_SOURCE_INVALID")
    model = stage / "model.json"
    dot = stage / "dot"
    dot.mkdir(mode=0o700)
    _run([str(likec4), "export", "json", "--skip-layout", "--pretty", "-o", str(model), str(source)], ROOT, env)
    _run([str(likec4), "gen", "dot", "-o", str(dot), str(source)], ROOT, env)
    renderer = tool / "architecture-render.mjs"
    shutil.copyfile(ROOT / "learning/curriculum/tools/architecture-render.mjs", renderer)
    raw_svg = stage / "raw-svg"
    _run([str(node / "bin/node"), str(renderer), str(dot), str(raw_svg)], tool, env)

    manifest = load_json(root / "architecture/expansions/i5-06/likec4/view-manifest.yaml")
    model_value = json.loads(model.read_text())
    if not set(VIEW_KEYS) <= set(model_value["views"]):
        raise ArchitectureExpansionError("ARCH_VIEW_SET_MISMATCH")
    output = stage / "final"
    output.mkdir(mode=0o700)
    rows = []
    closure = _source_closure(root)
    for row in manifest["views"]:
        external = row["id"]
        view = model_value["views"][row["key"]]
        text = _semantic_text(external, row, view)
        semantic_sha = sha256_bytes(canonical_bytes({"view": _semantic_projection(view), "manifest": row}))
        svg = _normalize_svg((raw_svg / f"{external}.raw.svg").read_text(), view["title"], f"{row['type']} view for {row['audienceVi']}: {row['concernId']}")
        (output / f"{external}.txt").write_bytes(text)
        (output / f"{external}.svg").write_bytes(svg)
        rows.append({"id": external, "key": row["key"], "type": row["type"], "semanticSha256": semantic_sha, "svgBytes": len(svg), "svgSha256": sha256_bytes(svg), "txtBytes": len(text), "txtSha256": sha256_bytes(text)})
    result = {
        "schemaVersion": "architecture-expansion-render-manifest-v1",
        "leaseId": "i5-06-stage-a-architecture-expansion-v1",
        "toolchain": {"node": "22.22.3", "npm": "10.9.8", "likec4": "1.59.1", "wasmGraphviz": "1.22.2", "graphviz": "15.0.0"},
        "sourceClosureSha256": closure,
        "rendererSha256": sha256_file(ROOT / "learning/curriculum/tools/architecture-render.mjs"),
        "packageLockSha256": sha256_file(ROOT / "requirements/architecture/package-lock.json"),
        "views": rows,
        "claim": "deterministic-static-stage-a-only",
    }
    (output / "render-manifest.json").write_bytes(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True).encode() + b"\n")
    for item in output.iterdir():
        os.chmod(item, 0o644)
    return output


def _tree_hash(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.iterdir()):
        digest.update(item.name.encode())
        digest.update(b"\0")
        digest.update(item.read_bytes())
    return digest.hexdigest()


def render(root: pathlib.Path = ROOT, output: pathlib.Path | None = None) -> dict[str, Any]:
    _check_protected(root)
    with tempfile.TemporaryDirectory(prefix="i11-expansion-") as temporary:
        final = _produce(root, pathlib.Path(temporary))
        destination = output or root / "architecture/expansions/i5-06/rendered"
        if destination.exists():
            if destination.is_symlink() or not destination.is_dir():
                raise ArchitectureExpansionError("ARCH_OUTPUT_UNSAFE")
            if any(destination.iterdir()):
                expected_names = {*(f"{view_id}.{extension}" for view_id in VIEW_IDS for extension in ("svg", "txt")), "render-manifest.json"}
                if {item.name for item in destination.iterdir()} != expected_names:
                    raise ArchitectureExpansionError("ARCH_OUTPUT_UNSAFE")
                for item in final.iterdir():
                    if (destination / item.name).read_bytes() != item.read_bytes():
                        shutil.copyfile(item, destination / item.name)
                        os.chmod(destination / item.name, 0o644)
            else:
                for item in final.iterdir():
                    shutil.copyfile(item, destination / item.name)
                    os.chmod(destination / item.name, 0o644)
        else:
            destination.mkdir(parents=True, mode=0o755)
            for item in final.iterdir():
                shutil.copyfile(item, destination / item.name)
                os.chmod(destination / item.name, 0o644)
        return {"viewCount": 5, "treeSha256": _tree_hash(destination), "output": destination}


def check(root: pathlib.Path = ROOT, rendered: pathlib.Path | None = None) -> dict[str, Any]:
    _check_protected(root)
    manifest = load_json(root / "architecture/expansions/i5-06/likec4/view-manifest.yaml")
    if tuple(row["id"] for row in manifest["views"]) != VIEW_IDS or tuple(row["key"] for row in manifest["views"]) != VIEW_KEYS:
        raise ArchitectureExpansionError("ARCH_VIEW_INVALID")
    if any(not row["concernId"] or not row["audienceVi"] or not row["traceIds"] for row in manifest["views"]):
        raise ArchitectureExpansionError("ARCH_VIEW_INVALID")
    try:
        base_manifest = yaml.safe_load((root / "architecture/likec4/view-manifest.yaml").read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ArchitectureExpansionError("ARCH_VIEW_INVALID") from exc
    if not isinstance(base_manifest, dict) or not isinstance(base_manifest.get("views"), list):
        raise ArchitectureExpansionError("ARCH_VIEW_INVALID")
    if set(VIEW_IDS) & {row["id"] for row in base_manifest["views"]} or set(VIEW_KEYS) & {row["key"] for row in base_manifest["views"]}:
        raise ArchitectureExpansionError("ARCH_VIEW_INVALID")
    output = rendered or root / "architecture/expansions/i5-06/rendered"
    result = load_json(output / "render-manifest.json")
    if tuple(row["id"] for row in result["views"]) != VIEW_IDS:
        raise ArchitectureExpansionError("ARCH_VIEW_SET_MISMATCH")
    if result["sourceClosureSha256"] != _source_closure(root) or result["rendererSha256"] != sha256_file(ROOT / "learning/curriculum/tools/architecture-render.mjs") or result["packageLockSha256"] != sha256_file(ROOT / "requirements/architecture/package-lock.json"):
        raise ArchitectureExpansionError("ARCH_OUTPUT_STALE")
    total = 0
    for row in result["views"]:
        for extension in ("svg", "txt"):
            path = output / f"{row['id']}.{extension}"
            raw = path.read_bytes()
            total += len(raw)
            if len(raw) != row[f"{extension}Bytes"] or sha256_bytes(raw) != row[f"{extension}Sha256"]:
                raise ArchitectureExpansionError("ARCH_OUTPUT_STALE")
            text = raw.decode("utf-8")
            inspected_text = text
            if extension == "svg":
                inspected_text = inspected_text.replace("http://www.w3.org/2000/svg", "").replace("http://www.w3.org/1999/xlink", "")
            if b"\r" in raw or not raw.endswith(b"\n") or unicodedata.normalize("NFC", text) != text or PRIVATE_OR_UNSAFE.search(inspected_text):
                raise ArchitectureExpansionError("ARCH_OUTPUT_UNSAFE")
            if extension == "txt" and not all(label in text for label in ("Audience:", "Concern:", "Scope:", "Elements:", "Relations:", "Limitations:", "TBCs:")):
                raise ArchitectureExpansionError("ARCH_ACCESSIBILITY_INVALID")
            if extension == "svg":
                xml = ET.fromstring(raw)
                local = lambda tag: tag.rsplit("}", 1)[-1]
                if xml.get("role") != "img" or not any(local(child.tag) == "title" for child in xml) or not any(local(child.tag) == "desc" for child in xml):
                    raise ArchitectureExpansionError("ARCH_ACCESSIBILITY_INVALID")
                if not any(local(node.tag) == "text" and "Legend:" in "".join(node.itertext()) for node in xml.iter()):
                    raise ArchitectureExpansionError("ARCH_ACCESSIBILITY_INVALID")
                for node in xml.iter():
                    if local(node.tag) in {"script", "foreignObject", "image"} or any(name.lower().startswith("on") or name.lower().endswith("href") or name.lower() == "src" for name in node.attrib):
                        raise ArchitectureExpansionError("ARCH_OUTPUT_UNSAFE")
    if total > 2 * 1024 * 1024:
        raise ArchitectureExpansionError("ARCH_OUTPUT_BOUNDS_INVALID")
    return {"viewCount": 5, "protectedCount": 33, "accessible": True, "fresh": True, "renderMode": "isolated-likec4-wasm", "renderedBytes": total, "treeSha256": _tree_hash(output)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("command", nargs="?", choices=("check", "render"), default="check")
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--rendered", type=pathlib.Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        summary = render(root, args.output) if args.command == "render" else check(root, args.rendered)
        if args.command == "render" and args.output is None:
            summary = check(root)
        print(json.dumps({key: value.as_posix() if isinstance(value, pathlib.Path) else value for key, value in summary.items()}, sort_keys=True) if args.json else f"architecture-expansion-{args.command}: pass views=5 tree={summary['treeSha256']}")
        return 0
    except (ArchitectureExpansionError, ContentError, OSError, subprocess.SubprocessError, ValueError, ET.ParseError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
