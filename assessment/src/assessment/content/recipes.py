"""Public additive recipe-extension loader used by inert test fixtures."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from assessment.content.loader import load_yaml
from assessment.content.schemas import validate_document
from assessment.domain.errors import ContentValidationError
from assessment.domain.models import Recipe

RECIPE_FILES = {
    "recipe.yaml",
    "vocabulary.yaml",
    "questions.yaml",
    "mappings.yaml",
    "demo.yaml",
    "inertness-proof.json",
}


class RecipeExtensionModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class RecipeVocabulary(RecipeExtensionModel):
    terms: dict[str, str] = Field(min_length=1)


class RecipeQuestion(RecipeExtensionModel):
    id: str
    capability_id: str
    text: str = Field(min_length=12)
    advisory_only: Literal[True]


class RecipeMapping(RecipeExtensionModel):
    question_id: str
    recommendation_id: str
    architecture_id: str


class AbsentRecipeDemo(RecipeExtensionModel):
    status: Literal["absent"]
    reason: str = Field(min_length=12)
    non_scoring: Literal[True]
    executable: Literal[False]


class RecipeExtension(RecipeExtensionModel):
    manifest: Recipe
    vocabulary: RecipeVocabulary
    questions: tuple[RecipeQuestion, ...]
    mappings: tuple[RecipeMapping, ...]
    demo: AbsentRecipeDemo
    production_supported: Literal[False]
    pipeline_routes: tuple[()]


def load_recipe_extension(root: Path) -> RecipeExtension:
    """Load an additive content bundle without changing framework or engine state."""
    if not root.is_absolute() or root.is_symlink() or not root.is_dir():
        raise ContentValidationError("recipe extension root must be a real absolute directory")
    names = {path.name for path in root.iterdir() if path.is_file()}
    if names != RECIPE_FILES:
        raise ContentValidationError("recipe extension contains an unexpected file inventory")
    try:
        raw_manifest = load_yaml(root / "recipe.yaml")
        validate_document(
            raw_manifest,
            resources.files("assessment.public_schemas").joinpath(
                "recipe-v1.schema.json"
            ),
        )
        manifest = Recipe.model_validate(raw_manifest)
        vocabulary = RecipeVocabulary.model_validate(load_yaml(root / "vocabulary.yaml"))
        question_document = load_yaml(root / "questions.yaml")
        mapping_document = load_yaml(root / "mappings.yaml")
        demo = AbsentRecipeDemo.model_validate(load_yaml(root / "demo.yaml"))
        questions = tuple(
            RecipeQuestion.model_validate(item)
            for item in question_document.get("questions", [])
        )
        mappings = tuple(
            RecipeMapping.model_validate(item)
            for item in mapping_document.get("mappings", [])
        )
    except (ValidationError, ValueError) as error:
        raise ContentValidationError(f"recipe extension: {error}") from error
    question_ids = [question.id for question in questions]
    if (
        manifest.question_ids != question_ids
        or len(question_ids) != len(set(question_ids))
    ):
        raise ContentValidationError("recipe extension question inventory is inconsistent")
    if not {question.capability_id for question in questions} <= set(
        manifest.capability_ids
    ):
        raise ContentValidationError("recipe extension capability reference is unresolved")
    if {mapping.question_id for mapping in mappings} != set(question_ids):
        raise ContentValidationError("recipe extension mapping coverage is incomplete")
    return RecipeExtension(
        manifest=manifest,
        vocabulary=vocabulary,
        questions=questions,
        mappings=mappings,
        demo=demo,
        production_supported=False,
        pipeline_routes=(),
    )
