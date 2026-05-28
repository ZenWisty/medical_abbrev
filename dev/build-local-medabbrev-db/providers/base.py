"""Provider base classes, error types, and metadata."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class ProviderError(RuntimeError):
    """Base error for all provider operations."""
    pass


class ProviderParseError(ProviderError):
    """Error raised when provider fails to parse response content."""
    pass


@dataclass(frozen=True)
class ProviderMetadata:
    """Metadata describing a provider's identity and capabilities."""
    provider_id: str
    display_name: str
    capabilities: tuple[str, ...]


class SignalProvider(ABC):
    """Abstract base class for all information providers."""

    provider_id: str
    display_name: str
    capabilities: tuple[str, ...] = ()

    @abstractmethod
    def search_abbreviation(self, abbrev: str) -> list:
        """Search for an abbreviation. Must be implemented by subclasses."""
        ...

    def describe(self) -> ProviderMetadata:
        """Return metadata describing this provider."""
        return ProviderMetadata(
            provider_id=self.provider_id,
            display_name=self.display_name,
            capabilities=self.capabilities,
        )