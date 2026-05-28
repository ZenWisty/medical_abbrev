"""Core data models for the MedAbbrev provider system."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MedicalSample:
    """A medical text sample from a provider source.

    Represents a single medical document or case description
    retrieved from sources like mtsamples.com.
    """
    id: str
    title: str
    category: str
    description: str
    content: str
    url: str


@dataclass(frozen=True)
class AbbreviationResult:
    """Results from an abbreviation search operation.

    Contains an abbreviation and its possible expansions,
    along with sample medical contexts where it appears.
    """
    abbrev: str
    expansions: list[str]
    samples: list["MedicalSample"]