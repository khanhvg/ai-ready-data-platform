from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys
import time
from typing import Any

import jsonschema

from .content_io import ContentError, ROOT, canonical_bytes, emit_evidence, load_json, sha256_file, verify_evidence


INPUT_SHA = "c07c9a080be7be88447aac497bdf0a2b5fddd020"
RELEASE_SHA = "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
MODULE_FILES = ("foundation-v1.json", "junior-v1.json", "data-v1.json", "mid-v1.json")
EXPECTED_IDS = (
    "F01", "F02", "F03", "F04", "J01", "J02", "J03", "J04", "J05", "J06",
    "D01", "D02", "D03", "D04", "D05", "D06", "M01", "M02", "M03", "M04",
)
EXPECTED_PREREQUISITES = {
    "F01": [], "F02": ["F01"], "F03": ["F02"], "F04": ["F03"],
    "J01": ["F03", "F04"], "J02": ["F04"], "J03": ["J02"], "J04": ["J03"],
    "J05": ["J03", "J04"], "J06": ["J03"], "D01": ["F03"], "D02": ["D01"],
    "D03": ["D02", "J04"], "D04": ["D02"], "D05": ["D02", "D03", "D04"],
    "D06": ["D05"], "M01": ["J02", "J03", "J04", "J05", "J06", "D05"],
    "M02": ["M01", "J04"], "M03": ["D04", "D05", "M01"], "M04": ["J05", "M01"],
}
EXPECTED_TEMPLATES = (
    "tpl-stakeholder-concern", "tpl-fr-nfr-asr", "tpl-option-matrix", "tpl-c4-view",
    "tpl-dynamic-sequence", "tpl-deployment", "tpl-adr", "tpl-pattern-admission",
    "tpl-fitness-function", "tpl-capacity-cost", "tpl-dr-recovery", "tpl-security-review",
)
VIETNAMESE = re.compile(r"[ăâđêôơưĂÂĐÊÔƠƯ]|[àáảãạèéẻẽẹìíỉĩịòóỏõọùúủũụỳýỷỹỵ]", re.I)
FORBIDDEN = re.compile(
    r"(?i)(AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|"
    r"https?://|file://|/Users/|/home/|terraform\s+(?:apply|destroy)|"
    r"aws\s+\w+\s+(?:create|delete|put)|<\s*script|<\s*foreignObject|on[a-z]+\s*=|"
    r"data:(?:text|image|application)/|src\s*=|href\s*=)"
)


class CurriculumError(ValueError):
    """Stable public validator error."""


def _schema(root: pathlib.Path, name: str, value: Any, code: str = "CURRICULUM_SCHEMA_INVALID") -> None:
    schema = load_json(root / "learning/curriculum/contracts" / name)
    jsonschema.Draft202012Validator.check_schema(schema)
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(value), key=lambda error: tuple(str(part) for part in error.absolute_path))
    if errors:
        raise CurriculumError(f"{code}:{errors[0].json_path}:{errors[0].message}")


def _expect_keys(value: dict[str, Any], required: set[str], code: str) -> None:
    if set(value) != required:
        raise CurriculumError(code)


def _validate_graph(modules: list[dict[str, Any]]) -> None:
    if tuple(module["id"] for module in modules) != EXPECTED_IDS or len({module["id"] for module in modules}) != 20:
        raise CurriculumError("CURRICULUM_PREREQUISITE_INVALID")
    by_id = {module["id"]: module for module in modules}
    if any(module["sequence"] != ordinal for ordinal, module in enumerate(modules, 1)):
        raise CurriculumError("CURRICULUM_PREREQUISITE_INVALID")
    if any(module["prerequisites"] != EXPECTED_PREREQUISITES[module["id"]] for module in modules):
        raise CurriculumError("CURRICULUM_PREREQUISITE_INVALID")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(module_id: str) -> None:
        if module_id in visiting:
            raise CurriculumError("CURRICULUM_PREREQUISITE_INVALID")
        if module_id in visited:
            return
        visiting.add(module_id)
        for prerequisite in by_id[module_id]["prerequisites"]:
            if prerequisite not in by_id or prerequisite == module_id:
                raise CurriculumError("CURRICULUM_PREREQUISITE_INVALID")
            visit(prerequisite)
        visiting.remove(module_id)
        visited.add(module_id)

    for module_id in by_id:
        visit(module_id)
    if visited != set(EXPECTED_IDS) or any(module_id != "F01" and "F01" not in _ancestors(module_id, by_id) for module_id in EXPECTED_IDS):
        raise CurriculumError("CURRICULUM_PREREQUISITE_INVALID")


def _ancestors(module_id: str, by_id: dict[str, dict[str, Any]]) -> set[str]:
    result: set[str] = set()
    pending = list(by_id[module_id]["prerequisites"])
    while pending:
        current = pending.pop()
        if current in result:
            continue
        result.add(current)
        pending.extend(by_id[current]["prerequisites"])
    return result


def _validate_templates(value: dict[str, Any]) -> None:
    templates = value["templates"]
    if tuple(template["id"] for template in templates) != EXPECTED_TEMPLATES:
        raise CurriculumError("CURRICULUM_TEMPLATE_INVALID")
    seen: set[tuple[str, str]] = set()
    for template in templates:
        identity = (template["id"], template["version"])
        if identity in seen:
            raise CurriculumError("CURRICULUM_TEMPLATE_INVALID")
        seen.add(identity)
        hashed = {key: item for key, item in template.items() if key != "contentSha256"}
        if hashlib.sha256(canonical_bytes(hashed)).hexdigest() != template["contentSha256"]:
            raise CurriculumError("CURRICULUM_TEMPLATE_INVALID")
        if template["supersession"]["status"] != "active" or template["supersession"]["supersedes"] is not None:
            raise CurriculumError("CURRICULUM_TEMPLATE_INVALID")


def _validate_patterns(value: dict[str, Any]) -> None:
    _expect_keys(value, {"schemaVersion", "patterns"}, "CURRICULUM_PATTERN_INVALID")
    if value["schemaVersion"] != "architecture-pattern-registry-v1" or not value["patterns"]:
        raise CurriculumError("CURRICULUM_PATTERN_INVALID")
    expected = {"id", "nameVi", "forceIds", "failureModes", "qualityAttributeIds", "boundaryId", "verifierIds", "tradeOffsVi", "removalRuleVi", "moduleIds"}
    identifiers: set[str] = set()
    for pattern in value["patterns"]:
        _expect_keys(pattern, expected, "CURRICULUM_PATTERN_INVALID")
        if pattern["id"] in identifiers or not all(pattern[key] for key in ("forceIds", "failureModes", "qualityAttributeIds", "verifierIds", "tradeOffsVi", "removalRuleVi")):
            raise CurriculumError("CURRICULUM_PATTERN_INVALID")
        identifiers.add(pattern["id"])


def _validate_assessment(value: dict[str, Any], module_ids: set[str]) -> None:
    _expect_keys(value, {"schemaVersion", "authority", "rubrics", "reflectionPolicy"}, "CURRICULUM_AUTHORITY_INVALID")
    _expect_keys(value["authority"], {"runtimeStatus", "authoritative", "completionMutation", "learnerEvidenceEmission"}, "CURRICULUM_AUTHORITY_INVALID")
    authority = value["authority"]
    if authority != {"runtimeStatus": "not-executed-static-only", "authoritative": False, "completionMutation": False, "learnerEvidenceEmission": False}:
        raise CurriculumError("CURRICULUM_AUTHORITY_INVALID")
    if {rubric["moduleId"] for rubric in value["rubrics"]} != module_ids:
        raise CurriculumError("CURRICULUM_REFERENCE_INVALID")


def _validate_activation(root: pathlib.Path, value: dict[str, Any]) -> None:
    schema = load_json(root / "learning/contracts/command-owner-activation-v1.schema.json")
    jsonschema.Draft202012Validator(schema).validate(value)
    if value["owner"] != "I5-06" or [row["commandId"] for row in value["commands"]] != ["curriculum-check", "traceability-check"]:
        raise CurriculumError("CURRICULUM_AUTHORITY_INVALID")
    if value["baseRegistrySha256"] != sha256_file(root / value["baseRegistryPath"]):
        raise CurriculumError("CURRICULUM_REFERENCE_INVALID")
    if value["fragment"]["sha256"] != sha256_file(root / value["fragment"]["path"]):
        raise CurriculumError("CURRICULUM_REFERENCE_INVALID")


def validate_security_and_bounds(root: pathlib.Path) -> dict[str, int]:
    curriculum = root / "learning/curriculum"
    expansion = root / "architecture/expansions/i5-06"
    files = sorted(item for base in (curriculum, expansion) if base.exists() for item in base.rglob("*") if item.is_file())
    curriculum_bytes = sum(item.stat().st_size for item in files if curriculum in item.parents)
    rendered_bytes = sum(item.stat().st_size for item in files if "rendered" in item.parts)
    if curriculum_bytes > 2 * 1024 * 1024 or rendered_bytes > 2 * 1024 * 1024:
        raise CurriculumError("CURRICULUM_BOUNDS_INVALID")
    for path in files:
        info = path.lstat()
        if path.is_symlink() or not path.is_file() or info.st_nlink != 1:
            raise CurriculumError("CURRICULUM_SECURITY_INVALID")
        if path.suffix in {".svg", ".txt", ".json", ".c4", ".yaml"}:
            raw = path.read_bytes()
            if b"\r" in raw or not raw.endswith(b"\n"):
                raise CurriculumError("CURRICULUM_SECURITY_INVALID")
            text = raw.decode("utf-8")
            sanitized = text.replace("https://json-schema.org/draft/2020-12/schema", "approved-schema-meta")
            sanitized = sanitized.replace("http://www.w3.org/2000/svg", "approved-svg-namespace")
            sanitized = sanitized.replace("http://www.w3.org/1999/xlink", "approved-xlink-namespace")
            if FORBIDDEN.search(sanitized):
                raise CurriculumError("CURRICULUM_SECURITY_INVALID")
        if path.suffix == ".svg" and path.stat().st_size > 256 * 1024:
            raise CurriculumError("CURRICULUM_BOUNDS_INVALID")
        if path.suffix == ".txt" and path.stat().st_size > 64 * 1024:
            raise CurriculumError("CURRICULUM_BOUNDS_INVALID")
    return {"curriculumBytes": curriculum_bytes, "renderedBytes": rendered_bytes, "unsafeCount": 0, "specialFileCount": 0}


def validate_all(root: pathlib.Path = ROOT) -> dict[str, Any]:
    base = root / "learning/curriculum"
    manifest = load_json(base / "architecture-curriculum-v1.json")
    _schema(root, "architecture-curriculum-v1.schema.json", manifest)
    if manifest["inputSha"] != INPUT_SHA or manifest["releasedStageASha"] != RELEASE_SHA:
        raise CurriculumError("CURRICULUM_REFERENCE_INVALID")

    modules: list[dict[str, Any]] = []
    expected_levels = ("foundation", "junior", "data", "mid")
    for filename, level in zip(MODULE_FILES, expected_levels, strict=True):
        collection = load_json(base / "modules" / filename)
        _schema(root, "architecture-module-collection-v1.schema.json", collection)
        if collection["level"] != level or any(module["level"] != level for module in collection["modules"]):
            raise CurriculumError("CURRICULUM_SCHEMA_INVALID")
        modules.extend(collection["modules"])
    _validate_graph(modules)
    for module in modules:
        vietnamese_fields = [module["title"]["vi"], module["remediation"]["textVi"], module["reflection"]["promptVi"], module["exercise"]["taskVi"], module["consequences"]["detailsVi"]]
        vietnamese_fields.extend(row["textVi"] for row in module["instructions"])
        if any(not VIETNAMESE.search(value) for value in vietnamese_fields):
            raise CurriculumError("CURRICULUM_LOCALE_INVALID")
        if module["traceId"] != f"trace-{module['id']}":
            raise CurriculumError("CURRICULUM_REFERENCE_INVALID")
        if module["evidence"]["learnerEvidence"] is not False or module["assessment"]["completionMutation"] is not False:
            raise CurriculumError("CURRICULUM_AUTHORITY_INVALID")

    templates = load_json(base / "templates/architecture-templates-v1.json")
    _schema(root, "architecture-template-registry-v1.schema.json", templates, "CURRICULUM_TEMPLATE_INVALID")
    _validate_templates(templates)

    trace = load_json(base / "traces/architecture-trace-v1.json")
    _schema(root, "architecture-trace-v1.schema.json", trace, "TRACEABILITY_INVALID")
    if {module["traceId"] for module in modules} != {row["id"] for row in trace["traces"]}:
        raise CurriculumError("CURRICULUM_REFERENCE_INVALID")

    patterns = load_json(base / "patterns/system-design-patterns-v1.json")
    _validate_patterns(patterns)
    pattern_ids = {pattern["id"] for pattern in patterns["patterns"]}
    if any(not set(module["decision"]["patternIds"]) <= pattern_ids for module in modules):
        raise CurriculumError("CURRICULUM_REFERENCE_INVALID")

    assessments = load_json(base / "assessments/architecture-assessment-v1.json")
    _validate_assessment(assessments, set(EXPECTED_IDS))

    mapping = load_json(base / "mappings/local-aws-conceptual-v1.json")
    _expect_keys(mapping, {"schemaVersion", "claim", "mappings", "limitations"}, "CURRICULUM_SCHEMA_INVALID")
    if mapping["claim"] != "conceptual-static-only-no-deployment" or len(mapping["mappings"]) != 6:
        raise CurriculumError("CURRICULUM_AUTHORITY_INVALID")

    example = load_json(base / "examples/promotion-publication-architecture-v1.json")
    _expect_keys(example, {"schemaVersion", "runtimeStatus", "decision", "reasonVi", "grainIds", "traceIds", "operationIds"}, "CURRICULUM_SCHEMA_INVALID")
    if example["runtimeStatus"] != "not-executed-static-only" or example["grainIds"] != ["region", "category", "dq", "overall"]:
        raise CurriculumError("CURRICULUM_AUTHORITY_INVALID")

    release_binding = load_json(base / "release-binding-i5-06-stage-a-v1.json")
    _schema(root, "architecture-release-binding-v1.schema.json", release_binding)
    if release_binding["inputSha"] != INPUT_SHA or release_binding["releasedStageASha"] != RELEASE_SHA or release_binding["stageB"]["status"] != "blocked-on-issue10":
        raise CurriculumError("CURRICULUM_REFERENCE_INVALID")

    view_manifest = load_json(root / "architecture/expansions/i5-06/likec4/view-manifest.yaml")
    _schema(root, "architecture-view-extension-v1.schema.json", view_manifest, "ARCH_VIEW_INVALID")

    activation = load_json(base / "command-owner-activation-i5-06-stage-a-v1.json")
    _validate_activation(root, activation)

    matrix = load_json(root / "learning/contracts/operation-matrix-v1.json")
    operation_ids = {row["operationId"] for row in matrix["operations"]}
    if len(operation_ids) != 16 or set(manifest["openApiOperationIds"]) != operation_ids:
        raise CurriculumError("CURRICULUM_API_INVALID")
    if manifest["asyncApiAdmission"] != {"status": "not-admitted", "reason": "no-released-channel", "channelIds": []}:
        raise CurriculumError("CURRICULUM_API_INVALID")

    bounds = validate_security_and_bounds(root)
    expected_json = {
        "architecture-curriculum-v1.json", "command-owner-activation-i5-06-stage-a-v1.json",
        "release-binding-i5-06-stage-a-v1.json", "architecture-assessment-v1.json",
        "architecture-curriculum-v1.schema.json", "architecture-module-collection-v1.schema.json",
        "architecture-release-binding-v1.schema.json", "architecture-template-registry-v1.schema.json",
        "architecture-trace-v1.schema.json", "architecture-view-extension-v1.schema.json",
        "promotion-publication-architecture-v1.json", "local-aws-conceptual-v1.json",
        *MODULE_FILES, "system-design-patterns-v1.json", "architecture-templates-v1.json", "architecture-trace-v1.json",
    }
    actual_json = {path.name for path in base.rglob("*.json")}
    if actual_json != expected_json or len(actual_json) != 19:
        raise CurriculumError("CURRICULUM_FILE_SET_INVALID")
    return {
        "schemaVersion": "architecture-curriculum-validation-v1",
        "moduleCount": len(modules),
        "templateCount": len(templates["templates"]),
        "validatedFileCount": 18,
        "activationValidated": True,
        "acyclic": True,
        "allReachable": True,
        "operationCount": len(operation_ids),
        "cloudActions": 0,
        "learnerEvidenceRecords": 0,
        "stageBPaths": 0,
        **bounds,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--no-evidence", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--verify-evidence", type=pathlib.Path)
    args = parser.parse_args(argv)
    try:
        if args.verify_evidence:
            summary = verify_evidence(args.verify_evidence)
            print(json.dumps(summary, sort_keys=True) if args.json else f"evidence-verify: pass entries={summary['entryCount']}")
            return 0
        started_wall = datetime.datetime.now(datetime.timezone.utc)
        started = time.monotonic()
        summary = validate_all(args.root.resolve())
        if args.json:
            print(json.dumps(summary, sort_keys=True))
        elif args.no_evidence or args.root.resolve() != ROOT:
            print(f"curriculum-check: pass modules={summary['moduleCount']} templates={summary['templateCount']}")
        else:
            locator = emit_evidence("curriculum-check", summary, started_wall, started)
            print(f"EVIDENCE_LOCATOR={locator.as_posix()}")
            print(f"curriculum-check: pass modules={summary['moduleCount']} templates={summary['templateCount']}")
        return 0
    except (ContentError, CurriculumError, jsonschema.ValidationError, jsonschema.SchemaError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
