# Build Local MedAbbrev DB Provider — PRD

## 1. Overview

**Project:** medical_abbrev
**Type:** Local scraping provider system
**Goal:** Build a provider architecture for fetching and storing medical abbreviation data from mtsamples.com. The system should support multiple information sources, starting with a single provider for mtsamples.com.

---

## 2. Reference Architecture

Based on `digital_oracle/providers/`:

```
providers/
├── __init__.py          # All provider exports
├── base.py              # Base class, error types, metadata
├── _coerce.py           # Type coercion helpers
├── mtsamples.py         # mtsamples.com provider (initial)
└── [future providers]   # Additional sources
```

### Base Provider Interface

```python
class ProviderError(RuntimeError): pass
class ProviderParseError(ProviderError): pass

@dataclass(frozen=True)
class ProviderMetadata:
    provider_id: str
    display_name: str
    capabilities: tuple[str, ...]

class SignalProvider(ABC):
    provider_id: str
    display_name: str
    capabilities: tuple[str, ...] = ()

    def describe(self) -> ProviderMetadata: ...
```

---

## 3. Provider Structure

### 3.1 MedAbbrevProvider (SignalProvider)

- `provider_id = "mtsamples"`
- `display_name = "mtsamples.com"`
- `capabilities = ("abbreviation_search", "sample_listing")`

### 3.2 Data Models

```python
@dataclass
class MedicalSample:
    id: str
    title: str
    category: str
    description: str
    content: str          # transcript/notes
    url: str

@dataclass
class AbbreviationResult:
    abbrev: str
    expansions: list[str]
    samples: list[MedicalSample]
```

### 3.3 Interface

```python
class MedAbbrevProvider(SignalProvider):
    def search_abbreviation(self, abbrev: str) -> list[AbbreviationResult]: ...

    def get_samples(self, category: str | None = None, limit: int = 20) -> list[MedicalSample]: ...

    def get_categories(self) -> list[str]: ...
```

---

## 4. Implementation Phases

### Phase 1: Foundation
- [ ] Create `providers/base.py` — base class, errors, metadata
- [ ] Create `providers/_coerce.py` — coercion helpers
- [ ] Create `providers/__init__.py` — exports
- [ ] Create `providers/mtsamples.py` — initial provider stub

### Phase 2: mtsamples Provider
- [ ] Implement HTTP client with proper headers
- [ ] Implement `search_abbreviation()`
- [ ] Implement `get_samples()`
- [ ] Implement `get_categories()`
- [ ] Write BDD tests (Given-When-Then)

### Phase 3: Storage
- [ ] Local DB model (SQLite)
- [ ] Provider data persistence

### Phase 4: Future Providers
- [ ] Additional information sources
- [ ] Unified search interface across providers

---

## 5. Dependencies

- Python 3.10+
- `.venv` (per project instructions)
- `requests` or `urllib` for HTTP
- `sqlite3` for local storage
- `scrapy` (already in project) for scraping

---

## 6. File Structure

```
medical_abbrev/
├── providers/
│   ├── __init__.py
│   ├── base.py
│   ├── _coerce.py
│   └── mtsamples.py
├── storage/
│   └── db.py
├── plan/
│   └── build-local-medabbrev-db-provider.md
└── .venv/
```