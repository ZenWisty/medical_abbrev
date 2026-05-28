"""Unit tests for MedAbbrev Data Models (#2)."""

import unittest
from dataclasses import FrozenInstanceError

from providers.data_models import AbbreviationResult, MedicalSample


# =============================================================================
# MedicalSample
# =============================================================================

class TestMedicalSampleCreation(unittest.TestCase):
    """MedicalSample is a frozen dataclass representing a medical text sample."""

    def test_can_be_created_with_all_fields(self):
        """Given valid field values
        When MedicalSample is created with all required fields
        Then all fields are accessible."""
        sample = MedicalSample(
            id="1",
            title="Heart Surgery Case",
            category="Cardiology",
            description="A case of triple bypass surgery",
            content="Patient presented with...",
            url="https://mtsamples.com/sample/1",
        )
        self.assertEqual(sample.id, "1")
        self.assertEqual(sample.title, "Heart Surgery Case")
        self.assertEqual(sample.category, "Cardiology")
        self.assertEqual(sample.description, "A case of triple bypass surgery")
        self.assertEqual(sample.content, "Patient presented with...")
        self.assertEqual(sample.url, "https://mtsamples.com/sample/1")

    def test_is_frozen(self):
        """Given a MedicalSample instance
        When attempting to modify any field
        Then a FrozenInstanceError is raised."""
        sample = MedicalSample(
            id="1", title="Test", category="Cat",
            description="Desc", content="Content", url="http://x.com"
        )
        with self.assertRaises(FrozenInstanceError):
            sample.id = "2"

    def test_fields_are_correctly_typed(self):
        """Given a MedicalSample instance
        Then fields have correct types: id=str, title=str, category=str,
        description=str, content=str, url=str."""
        sample = MedicalSample(
            id="1", title="T", category="C",
            description="D", content="Co", url="http://x.com"
        )
        self.assertIsInstance(sample.id, str)
        self.assertIsInstance(sample.title, str)
        self.assertIsInstance(sample.category, str)
        self.assertIsInstance(sample.description, str)
        self.assertIsInstance(sample.content, str)
        self.assertIsInstance(sample.url, str)


class TestMedicalSampleEquality(unittest.TestCase):
    """MedicalSample instances with same field values are equal."""

    def test_two_instances_with_same_values_are_equal(self):
        """Given two MedicalSample instances with identical field values
        When compared with ==
        Then they are considered equal."""
        s1 = MedicalSample("1", "T", "C", "D", "Co", "http://x.com")
        s2 = MedicalSample("1", "T", "C", "D", "Co", "http://x.com")
        self.assertEqual(s1, s2)

    def test_two_instances_with_different_values_are_not_equal(self):
        """Given two MedicalSample instances with different field values
        When compared with ==
        Then they are considered not equal."""
        s1 = MedicalSample("1", "T", "C", "D", "Co", "http://x.com")
        s2 = MedicalSample("2", "T", "C", "D", "Co", "http://x.com")
        self.assertNotEqual(s1, s2)


# =============================================================================
# AbbreviationResult
# =============================================================================

class TestAbbreviationResultCreation(unittest.TestCase):
    """AbbreviationResult holds abbreviation search results."""

    def test_can_be_created_with_all_fields(self):
        """Given valid field values
        When AbbreviationResult is created
        Then all fields are accessible."""
        sample = MedicalSample("1", "T", "C", "D", "Co", "http://x.com")
        result = AbbreviationResult(
            abbrev="ACL",
            expansions=["Anterior Cruciate Ligament"],
            samples=[sample],
        )
        self.assertEqual(result.abbrev, "ACL")
        self.assertEqual(result.expansions, ["Anterior Cruciate Ligament"])
        self.assertEqual(result.samples, [sample])

    def test_is_frozen(self):
        """Given an AbbreviationResult instance
        When attempting to modify any field
        Then a FrozenInstanceError is raised."""
        result = AbbreviationResult("ACL", [], [])
        with self.assertRaises(FrozenInstanceError):
            result.abbrev = "X"

    def test_fields_have_correct_types(self):
        """Given an AbbreviationResult instance
        Then fields have correct types: abbrev=str, expansions=list[str],
        samples=list[MedicalSample]."""
        result = AbbreviationResult("ACL", ["exp"], [])
        self.assertIsInstance(result.abbrev, str)
        self.assertIsInstance(result.expansions, list)
        self.assertIsInstance(result.samples, list)


class TestAbbreviationResultEquality(unittest.TestCase):
    """AbbreviationResult instances with same field values are equal."""

    def test_two_instances_with_same_values_are_equal(self):
        """Given two AbbreviationResult instances with identical field values
        When compared with ==
        Then they are considered equal."""
        r1 = AbbreviationResult("ACL", ["exp"], [])
        r2 = AbbreviationResult("ACL", ["exp"], [])
        self.assertEqual(r1, r2)


# =============================================================================
# Data Models Export
# =============================================================================

class TestDataModelsExport(unittest.TestCase):
    """Data models are properly exported from providers package."""

    def test_can_import_medical_sample(self):
        """Given the providers package is installed
        When importing MedicalSample from providers
        Then MedicalSample class is available."""
        from providers import MedicalSample
        self.assertTrue(callable(MedicalSample))

    def test_can_import_abbreviation_result(self):
        """Given the providers package is installed
        When importing AbbreviationResult from providers
        Then AbbreviationResult class is available."""
        from providers import AbbreviationResult
        self.assertTrue(callable(AbbreviationResult))


if __name__ == "__main__":
    unittest.main()