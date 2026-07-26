"""Read-only typed resolution of finding-to-action mapping chains."""

from __future__ import annotations

import copy
from importlib import resources
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from yaml.tokens import AliasToken, AnchorToken

from assessment.catalog.models import CatalogBundle, DemoCatalog
from assessment.domain.errors import ContentValidationError
from assessment.frameworks import FrameworkBundle

CRITICAL_FINDING_FAMILIES = (
    "F-OWNERSHIP",
    "F-QUALITY",
    "F-PRIVACY",
    "F-SECURITY",
    "F-GOVERNANCE",
    "F-LINEAGE",
    "F-REPRODUCIBILITY",
    "F-AI-OPERATING",
)
ProvenanceKind = Literal[
    "generated-assessment-fact",
    "architect-judgment",
    "catalog-reference",
    "demo-illustration",
]
NodeKind = Literal[
    "gap",
    "impact",
    "priority",
    "recommendation",
    "architecture",
    "technology-options",
    "demo",
    "action",
]
EdgeKind = Literal[
    "causes",
    "prioritized-as",
    "addressed-by",
    "implemented-through",
    "has-options",
    "illustrated-by",
    "owned-through",
]
ALLOWED_EDGES: set[tuple[NodeKind, NodeKind, EdgeKind]] = {
    ("gap", "impact", "causes"),
    ("impact", "priority", "prioritized-as"),
    ("priority", "recommendation", "addressed-by"),
    ("recommendation", "architecture", "implemented-through"),
    ("architecture", "technology-options", "has-options"),
    ("technology-options", "demo", "illustrated-by"),
    ("technology-options", "action", "owned-through"),
    ("demo", "action", "owned-through"),
}


class MappingModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Provenance(MappingModel):
    kind: ProvenanceKind
    reference: str


class AuthoredEdge(MappingModel):
    source: NodeKind
    target: NodeKind
    kind: EdgeKind


class AuthoredProfileRoleRefs(MappingModel):
    profile_id: Literal["aws-first-profile", "local-demo-evidence"]
    role_ids: list[str] = Field(min_length=1)


class AuthoredChain(MappingModel):
    finding_id: str
    gap: str = Field(min_length=12)
    impact: str = Field(min_length=12)
    priority: str = Field(min_length=1)
    recommendation_id: str
    architecture_id: str
    technology_option_ids: list[str] = Field(min_length=1)
    profile_role_refs: list[AuthoredProfileRoleRefs] = Field(min_length=1)
    demo_reference_id: str | None
    owner_role: str = Field(min_length=1)
    horizon: str = Field(min_length=1)
    success_measure: str = Field(min_length=12)
    edges: list[AuthoredEdge] = Field(min_length=6, max_length=7)


class MappingRegistry(MappingModel):
    schema_version: Literal["1.0.0"]
    catalog_version: Literal["1.0.0"]
    chains: list[AuthoredChain] = Field(min_length=8, max_length=8)


class TextNode(MappingModel):
    text: str
    provenance: Provenance


class PriorityNode(MappingModel):
    label: str
    provenance: Provenance


class ReferenceNode(MappingModel):
    id: str
    title: str
    provenance: Provenance


class TechnologyOption(MappingModel):
    id: str
    role: str
    alternatives: tuple[str, ...]
    constraints: tuple[str, ...]
    vendor_neutral: Literal[True]
    provenance: Provenance


class ProfileTechnologyOption(MappingModel):
    profile_id: str
    role_id: str
    role: str
    selected_tool: str
    content_only: Literal[True]
    executable: Literal[False]
    provenance: Provenance


class DemoLeaf(MappingModel):
    reference_id: str
    stage_ids: tuple[str, ...]
    explanation: str
    status: Literal["available", "unavailable", "mixed"]
    non_scoring: Literal[True]
    provenance: Provenance


class ActionNode(MappingModel):
    owner_role: str
    horizon: str
    success_measure: str
    provenance: Provenance


class FindingActionChain(MappingModel):
    finding_id: str
    gap: TextNode
    impact: TextNode
    priority: PriorityNode
    recommendation: ReferenceNode
    architecture: ReferenceNode
    technology_options: tuple[TechnologyOption, ...]
    profile_options: tuple[ProfileTechnologyOption, ...]
    demo: DemoLeaf | None
    action: ActionNode
    edges: tuple[AuthoredEdge, ...]


def load_mapping_registry() -> MappingRegistry:
    raw = (
        resources.files("assessment")
        .joinpath(
            "content",
            "catalog",
            "1.0.0",
            "mappings",
            "finding-action-chains.yaml",
        )
        .read_text(encoding="utf-8")
    )
    try:
        if any(isinstance(token, AliasToken | AnchorToken) for token in yaml.scan(raw)):
            raise ContentValidationError(
                "finding action mappings: YAML anchors and aliases are not allowed"
            )
        document = yaml.safe_load(raw)
        return MappingRegistry.model_validate(document)
    except (yaml.YAMLError, ValidationError) as error:
        raise ContentValidationError(f"finding action mappings: {error}") from error


class MappingResolver:
    """Resolve validated references without writing inputs or invoking the engine."""

    def __init__(
        self,
        framework: FrameworkBundle,
        catalog: CatalogBundle,
        demo: DemoCatalog,
        registry: MappingRegistry,
    ) -> None:
        self._framework = copy.deepcopy(framework)
        self._catalog = catalog.model_copy(deep=True)
        self._demo = demo.model_copy(deep=True)
        self._registry = registry.model_copy(deep=True)
        self._validate()

    def _validate(self) -> None:
        finding_ids = {str(item["id"]) for item in self._framework.finding_rules}
        recommendation_ids = {
            str(item["id"]) for item in self._framework.recommendations
        }
        architecture_ids = {item.id for item in self._catalog.architectures}
        demo_ids = {item.id for item in self._demo.evidence_links}
        profiles = {item.id: item for item in self._catalog.technology_profiles}
        alternatives = profiles["deferred-alternatives"]
        alternative_roles = {item.id: item for item in alternatives.roles}
        ordered = tuple(item.finding_id for item in self._registry.chains)
        if ordered != CRITICAL_FINDING_FAMILIES or set(ordered) != finding_ids:
            raise ContentValidationError(
                "finding action mappings must cover every critical finding family in order"
            )
        for chain in self._registry.chains:
            if chain.recommendation_id not in recommendation_ids:
                raise ContentValidationError(
                    f"{chain.finding_id}: unresolved recommendation reference"
                )
            if chain.architecture_id not in architecture_ids:
                raise ContentValidationError(
                    f"{chain.finding_id}: unresolved architecture reference"
                )
            if (
                chain.demo_reference_id is not None
                and chain.demo_reference_id not in demo_ids
            ):
                raise ContentValidationError(
                    f"{chain.finding_id}: unresolved demo reference"
                )
            if len(chain.technology_option_ids) != len(
                set(chain.technology_option_ids)
            ):
                raise ContentValidationError(
                    f"{chain.finding_id}: duplicate technology references"
                )
            for role_id in chain.technology_option_ids:
                role = alternative_roles.get(role_id)
                if role is None or chain.architecture_id not in role.architecture_ids:
                    raise ContentValidationError(
                        f"{chain.finding_id}: unresolved technology option reference"
                    )
            seen_profile_roles: set[tuple[str, str]] = set()
            for profile_refs in chain.profile_role_refs:
                profile = profiles[profile_refs.profile_id]
                profile_roles = {item.id: item for item in profile.roles}
                for role_id in profile_refs.role_ids:
                    reference = (profile.id, role_id)
                    role = profile_roles.get(role_id)
                    if (
                        reference in seen_profile_roles
                        or role is None
                        or role.selected_tool is None
                        or chain.architecture_id not in role.architecture_ids
                    ):
                        raise ContentValidationError(
                            f"{chain.finding_id}: unresolved technology profile reference"
                        )
                    seen_profile_roles.add(reference)
            self._validate_edges(chain)

    @staticmethod
    def _validate_edges(chain: AuthoredChain) -> None:
        triples = {(edge.source, edge.target, edge.kind) for edge in chain.edges}
        if len(triples) != len(chain.edges) or not triples <= ALLOWED_EDGES:
            raise ContentValidationError(f"{chain.finding_id}: invalid mapping edge")
        expected = {
            ("gap", "impact", "causes"),
            ("impact", "priority", "prioritized-as"),
            ("priority", "recommendation", "addressed-by"),
            ("recommendation", "architecture", "implemented-through"),
            ("architecture", "technology-options", "has-options"),
        }
        expected.add(
            (
                "technology-options",
                "demo" if chain.demo_reference_id else "action",
                "illustrated-by" if chain.demo_reference_id else "owned-through",
            )
        )
        if chain.demo_reference_id:
            expected.add(("demo", "action", "owned-through"))
        if triples != expected:
            raise ContentValidationError(
                f"{chain.finding_id}: edge graph is incomplete or cyclic"
            )

    def resolve_all(self) -> tuple[FindingActionChain, ...]:
        return tuple(self._resolve(item) for item in self._registry.chains)

    def by_finding_id(self, finding_id: str) -> FindingActionChain:
        for chain in self.resolve_all():
            if chain.finding_id == finding_id:
                return chain
        raise ContentValidationError(f"mapping for finding {finding_id!r}: not found")

    def _resolve(self, authored: AuthoredChain) -> FindingActionChain:
        recommendation = next(
            item
            for item in self._framework.recommendations
            if item["id"] == authored.recommendation_id
        )
        architecture = self._catalog.architecture(authored.architecture_id)
        profiles = {
            item.id: item for item in self._catalog.technology_profiles
        }
        alternatives = {
            item.id: item for item in profiles["deferred-alternatives"].roles
        }
        demo_leaf: DemoLeaf | None = None
        if authored.demo_reference_id is not None:
            link = self._demo.evidence_link(authored.demo_reference_id)
            statuses = {
                artifact.status
                for stage in self._demo.stages
                if stage.id in link.stage_ids
                for artifact in stage.artifacts
            }
            status: Literal["available", "unavailable", "mixed"]
            status = (
                "mixed"
                if len(statuses) > 1
                else ("available" if statuses == {"available"} else "unavailable")
            )
            demo_leaf = DemoLeaf(
                reference_id=link.id,
                stage_ids=tuple(link.stage_ids),
                explanation=link.explanation,
                status=status,
                non_scoring=True,
                provenance=Provenance(
                    kind="demo-illustration",
                    reference=f"demo:{link.id}",
                ),
            )
        return FindingActionChain(
            finding_id=authored.finding_id,
            gap=TextNode(
                text=authored.gap,
                provenance=Provenance(
                    kind="generated-assessment-fact",
                    reference=f"finding:{authored.finding_id}",
                ),
            ),
            impact=TextNode(
                text=authored.impact,
                provenance=Provenance(
                    kind="catalog-reference",
                    reference=f"recommendation:{authored.recommendation_id}",
                ),
            ),
            priority=PriorityNode(
                label=authored.priority,
                provenance=Provenance(
                    kind="generated-assessment-fact",
                    reference=f"finding:{authored.finding_id}:priority",
                ),
            ),
            recommendation=ReferenceNode(
                id=authored.recommendation_id,
                title=str(recommendation["action"]),
                provenance=Provenance(
                    kind="catalog-reference",
                    reference=f"recommendation:{authored.recommendation_id}",
                ),
            ),
            architecture=ReferenceNode(
                id=architecture.id,
                title=architecture.title,
                provenance=Provenance(
                    kind="catalog-reference",
                    reference=f"architecture:{architecture.id}",
                ),
            ),
            technology_options=tuple(
                TechnologyOption(
                    id=alternatives[role_id].id,
                    role=alternatives[role_id].role,
                    alternatives=tuple(alternatives[role_id].alternatives),
                    constraints=tuple(alternatives[role_id].constraints),
                    vendor_neutral=True,
                    provenance=Provenance(
                        kind="catalog-reference",
                        reference=(
                            "technology-profile:deferred-alternatives:"
                            f"{role_id}"
                        ),
                    ),
                )
                for role_id in authored.technology_option_ids
            ),
            profile_options=tuple(
                ProfileTechnologyOption(
                    profile_id=profile_refs.profile_id,
                    role_id=role.id,
                    role=role.role,
                    selected_tool=str(role.selected_tool),
                    content_only=profiles[profile_refs.profile_id].content_only,
                    executable=profiles[profile_refs.profile_id].executable,
                    provenance=Provenance(
                        kind="catalog-reference",
                        reference=(
                            f"technology-profile:{profile_refs.profile_id}:"
                            f"{role.id}"
                        ),
                    ),
                )
                for profile_refs in authored.profile_role_refs
                for role in profiles[profile_refs.profile_id].roles
                if role.id in profile_refs.role_ids
            ),
            demo=demo_leaf,
            action=ActionNode(
                owner_role=authored.owner_role,
                horizon=authored.horizon,
                success_measure=authored.success_measure,
                provenance=Provenance(
                    kind="catalog-reference",
                    reference=f"mapping:{authored.finding_id}:accountable-action",
                ),
            ),
            edges=tuple(authored.edges),
        )
