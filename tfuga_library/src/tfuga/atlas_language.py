from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageSpec:
    code: str
    name: str
    greeting: str
    direction: str = "ltr"


@dataclass(frozen=True)
class AtlasConcept:
    key: str
    canonical: str
    definition: str
    status: str = "prototype"


@dataclass(frozen=True)
class AtlasCard:
    language: LanguageSpec
    concept: AtlasConcept
    title: str
    prompt: str


class AITAtlasLanguage:
    def languages(self) -> tuple[LanguageSpec, ...]:
        return (
            LanguageSpec("fr", "Francais", "Bonjour"),
            LanguageSpec("en", "English", "Hello"),
            LanguageSpec("es", "Espanol", "Hola"),
            LanguageSpec("de", "Deutsch", "Hallo"),
            LanguageSpec("pt", "Portugues", "Ola"),
            LanguageSpec("ar", "Arabic", "Marhaba", "rtl"),
            LanguageSpec("zh", "Chinese", "Ni hao"),
            LanguageSpec("ja", "Japanese", "Konnichiwa"),
        )

    def concepts(self) -> tuple[AtlasConcept, ...]:
        return (
            AtlasConcept("tfuga", "TFUGA", "generative architecture for theories and artifacts"),
            AtlasConcept("oak", "OAK", "readiness and validation gate", "operational"),
            AtlasConcept("ait", "AIT", "agentic module in the TFUGA ecosystem", "operational"),
            AtlasConcept("omniall", "AIT-OmniAll", "recursive composition over AIT modules"),
            AtlasConcept("hyperbest", "TFUGAHyperBest", "ranking kernel for next best moves"),
        )

    def card(self, language: LanguageSpec, concept: AtlasConcept) -> AtlasCard:
        title = f"{concept.canonical} / {language.code}"
        prompt = f"Explain {concept.canonical} clearly in {language.name}; keep TFUGA/OAK terms stable."
        return AtlasCard(language, concept, title, prompt)

    def cards(self) -> tuple[AtlasCard, ...]:
        return tuple(self.card(lang, concept) for lang in self.languages() for concept in self.concepts())

    def coverage(self) -> dict[str, int]:
        return {lang.code: len(self.concepts()) for lang in self.languages()}

    def markdown(self) -> str:
        lines = ["# AIT Atlas Language", "", "mode: language_pack_seed", ""]
        for code, count in sorted(self.coverage().items()):
            lines.append(f"- `{code}`: `{count}` cards")
        return "\n".join(lines).strip() + "\n"
