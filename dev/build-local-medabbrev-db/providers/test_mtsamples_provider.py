"""Unit tests for mtsamples Provider Stub (#3)."""

import unittest


# =============================================================================
# MedAbbrevProvider Instantiation
# =============================================================================

class TestMedAbbrevProviderInstantiation(unittest.TestCase):
    """MedAbbrevProvider can be instantiated and inherits from SignalProvider."""

    def test_can_instantiate_med_abbrev_provider(self):
        """Given the MedAbbrevProvider class exists
        When MedAbbrevProvider is instantiated
        Then it succeeds without error."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        self.assertIsNotNone(provider)

    def test_is_subclass_of_signal_provider(self):
        """Given MedAbbrevProvider class
        When checking its inheritance
        Then it is a subclass of SignalProvider."""
        from providers import MedAbbrevProvider, SignalProvider
        self.assertTrue(issubclass(MedAbbrevProvider, SignalProvider))

    def test_has_correct_provider_id(self):
        """Given a MedAbbrevProvider instance
        When accessing provider_id
        Then it equals "mtsamples"."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        self.assertEqual(provider.provider_id, "mtsamples")

    def test_has_correct_display_name(self):
        """Given a MedAbbrevProvider instance
        When accessing display_name
        Then it equals "mtsamples.com"."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        self.assertEqual(provider.display_name, "mtsamples.com")

    def test_has_correct_capabilities(self):
        """Given a MedAbbrevProvider instance
        When accessing capabilities
        Then it includes "abbreviation_search" and "sample_listing"."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        caps = provider.capabilities
        self.assertIn("abbreviation_search", caps)
        self.assertIn("sample_listing", caps)


# =============================================================================
# MedAbbrevProvider Methods
# =============================================================================

class TestSearchAbbreviation(unittest.TestCase):
    """search_abbreviation() returns hardcoded list of AbbreviationResult."""

    def test_returns_list(self):
        """Given a MedAbbrevProvider instance
        When search_abbreviation is called with "ACL"
        Then a list is returned."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        result = provider.search_abbreviation("ACL")
        self.assertIsInstance(result, list)

    def test_returns_non_empty_for_known_abbreviation(self):
        """Given a MedAbbrevProvider instance
        When search_abbreviation is called with "ACL"
        Then the list is non-empty."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        result = provider.search_abbreviation("ACL")
        self.assertGreater(len(result), 0)

    def test_returns_empty_for_unknown_abbreviation(self):
        """Given a MedAbbrevProvider instance
        When search_abbreviation is called with "XYZNOTFOUND"
        Then an empty list is returned."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        result = provider.search_abbreviation("XYZNOTFOUND")
        self.assertEqual(len(result), 0)


class TestGetSamples(unittest.TestCase):
    """get_samples() returns hardcoded list of MedicalSample."""

    def test_returns_list(self):
        """Given a MedAbbrevProvider instance
        When get_samples is called
        Then a list is returned."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        result = provider.get_samples()
        self.assertIsInstance(result, list)

    def test_returns_list_with_limit(self):
        """Given a MedAbbrevProvider instance
        When get_samples is called with limit=5
        Then at most 5 samples are returned."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        result = provider.get_samples(limit=5)
        self.assertLessEqual(len(result), 5)


class TestGetCategories(unittest.TestCase):
    """get_categories() returns hardcoded list of category strings."""

    def test_returns_list(self):
        """Given a MedAbbrevProvider instance
        When get_categories is called
        Then a list is returned."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        result = provider.get_categories()
        self.assertIsInstance(result, list)

    def test_returns_non_empty_list(self):
        """Given a MedAbbrevProvider instance
        When get_categories is called
        Then the list is non-empty."""
        from providers import MedAbbrevProvider
        provider = MedAbbrevProvider()
        result = provider.get_categories()
        self.assertGreater(len(result), 0)


# =============================================================================
# Provider Export
# =============================================================================

class TestProviderExport(unittest.TestCase):
    """MedAbbrevProvider is properly exported from providers package."""

    def test_can_import_med_abbrev_provider(self):
        """Given the providers package is installed
        When importing MedAbbrevProvider from providers
        Then MedAbbrevProvider class is available."""
        from providers import MedAbbrevProvider
        self.assertIsNotNone(MedAbbrevProvider)


if __name__ == "__main__":
    unittest.main()