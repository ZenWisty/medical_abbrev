"""mtsamples.com provider implementation."""

from providers.base import SignalProvider
from providers.data_models import AbbreviationResult, MedicalSample


SAMPLES = [
    MedicalSample(
        id="1",
        title="Heart Surgery Case",
        category="Cardiology",
        description="A case of triple bypass surgery",
        content="Patient presented with chest pain...",
        url="https://mtsamples.com/sample/1",
    ),
    MedicalSample(
        id="2",
        title="Knee Arthroscopy",
        category="Orthopedics",
        description="Minimally invasive knee surgery",
        content="Patient scheduled for arthroscopic...",
        url="https://mtsamples.com/sample/2",
    ),
]

CATEGORIES = ["Cardiology", "Orthopedics", "Neurology", "Oncology", "Pediatrics"]


class MedAbbrevProvider(SignalProvider):
    """Provider for mtsamples.com medical abbreviation data.

    This stub uses hardcoded sample data to verify the provider interface
    before implementing real HTTP fetching.
    """

    provider_id = "mtsamples"
    display_name = "mtsamples.com"
    capabilities = ("abbreviation_search", "sample_listing")

    def search_abbreviation(self, abbrev: str) -> list[AbbreviationResult]:
        """Search for an abbreviation (stub returns hardcoded data)."""
        if abbrev == "ACL":
            return [
                AbbreviationResult(
                    abbrev="ACL",
                    expansions=["Anterior Cruciate Ligament"],
                    samples=SAMPLES[:1],
                )
            ]
        return []

    def get_samples(self, limit: int = 10) -> list[MedicalSample]:
        """Return medical samples (stub returns hardcoded data)."""
        return SAMPLES[:limit]

    def get_categories(self) -> list[str]:
        """Return available categories (stub returns hardcoded data)."""
        return CATEGORIES