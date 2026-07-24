"""All-rule readiness-gate evaluation with operand-level provenance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from assessment.engine.maturity import MaturityResult
from assessment.frameworks import FrameworkBundle


@dataclass(frozen=True)
class GateTrace:
    rule_id: str
    rule_version: int
    operand_id: str
    operand_source: str
    operand_value: int | bool | None
    operand_provenance: tuple[str, ...]
    operator: str
    threshold: int | bool
    evaluated: bool
    triggered: bool
    pre_gate_level: int | None
    applied_cap: int | None
    rule_result: int | None
    final_level: int | None
    explanation: str


@dataclass(frozen=True)
class GateResult:
    pre_gate_level: int | None
    final_level: int | None
    final_label: str
    selected_cap: int | None
    selected_rule_ids: tuple[str, ...]
    traces: tuple[GateTrace, ...]


def _operand(
    operand_id: str,
    maturity: MaturityResult,
    facts: dict[str, Any],
) -> tuple[int | bool | None, tuple[str, ...]]:
    if operand_id.startswith("domain."):
        capability_id = operand_id.removeprefix("domain.")
        capability = next(
            item for item in maturity.capabilities if item.capability_id == capability_id
        )
        return capability.score, capability.source_question_refs
    fact_id = operand_id.removeprefix("fact.")
    value = facts.get(fact_id)
    if type(value) not in {int, bool}:
        value = None
    return value, (f"assessment/quick.json#/diagnostic_facts/{fact_id}",)


def evaluate_gates(
    maturity: MaturityResult,
    diagnostic_facts: dict[str, Any],
    framework: FrameworkBundle,
) -> GateResult:
    provisional: list[dict[str, Any]] = []
    triggered_caps: list[tuple[int, str]] = []
    for rule in framework.gate_rules:
        value, provenance = _operand(
            rule["operand_id"],
            maturity,
            diagnostic_facts,
        )
        evaluated = value is not None
        triggered = False
        if evaluated and rule["operator"] == "le":
            triggered = bool(value <= rule["threshold"])
        elif evaluated and rule["operator"] == "eq":
            triggered = bool(value == rule["threshold"])
        if triggered:
            triggered_caps.append((rule["cap"], rule["id"]))
        rule_result = (
            min(maturity.pre_gate_level, rule["cap"])
            if triggered and maturity.pre_gate_level is not None
            else maturity.pre_gate_level
        )
        provisional.append(
            {
                "rule": rule,
                "value": value,
                "provenance": provenance,
                "evaluated": evaluated,
                "triggered": triggered,
                "rule_result": rule_result,
            }
        )

    selected_cap = min((cap for cap, _ in triggered_caps), default=None)
    final = maturity.pre_gate_level
    if final is not None and selected_cap is not None:
        final = min(final, selected_cap)
    selected_rules = tuple(
        rule_id
        for cap, rule_id in triggered_caps
        if selected_cap is not None and cap == selected_cap
    )
    traces = tuple(
        GateTrace(
            rule_id=item["rule"]["id"],
            rule_version=item["rule"]["version"],
            operand_id=item["rule"]["operand_id"],
            operand_source=item["rule"]["source"],
            operand_value=item["value"],
            operand_provenance=item["provenance"],
            operator=item["rule"]["operator"],
            threshold=item["rule"]["threshold"],
            evaluated=item["evaluated"],
            triggered=item["triggered"],
            pre_gate_level=maturity.pre_gate_level,
            applied_cap=item["rule"]["cap"] if item["triggered"] else None,
            rule_result=item["rule_result"],
            final_level=final,
            explanation=(
                f"{item['rule']['explanation']} Operand "
                f"{item['rule']['operand_id']} was {item['value']!r}; "
                f"the rule {'applied' if item['triggered'] else 'did not apply'}."
                if item["evaluated"]
                else (
                    f"{item['rule']['explanation']} Operand "
                    f"{item['rule']['operand_id']} was not assessed; the rule was not evaluated."
                )
            ),
        )
        for item in provisional
    )
    labels = framework.readiness["levels"]
    return GateResult(
        pre_gate_level=maturity.pre_gate_level,
        final_level=final,
        final_label=labels[final] if final is not None else "Not assessed",
        selected_cap=selected_cap,
        selected_rule_ids=selected_rules,
        traces=traces,
    )
