"""Unit tests for mtsamples HTML Parser (#5).

Note: These tests use mocked HTML fixtures to test parsing logic
without making live HTTP requests to mtsamples.com.
"""

import unittest
from unittest.mock import MagicMock

from providers.data_models import MedicalSample
from providers.base import ProviderParseError


# =============================================================================
# Sample Listing Page Parsing
# =============================================================================

class TestParseSampleListing(unittest.TestCase):
    """parse_sample_listing() extracts sample links from category pages."""

    def test_can_parse_sample_links_from_listing_html(self):
        """Given a sample listing HTML with table of sample links
        When parse_sample_listing is called
        Then it returns a list of sample URLs."""
        from providers.mtsamples._parser import MtsamplesParser

        html = """
        <html><body>
        <table>
            <tr><td><a href="sample.asp?sample=123">Sample 1</a></td></tr>
            <tr><td><a href="sample.asp?sample=456">Sample 2</a></td></tr>
        </table>
        </body></html>
        """
        parser = MtsamplesParser()
        urls = parser.parse_sample_listing(html)
        self.assertEqual(len(urls), 2)

    def test_parse_sample_listing_handles_empty_table(self):
        """Given a sample listing HTML with no sample links
        When parse_sample_listing is called
        Then it returns an empty list."""
        from providers.mtsamples._parser import MtsamplesParser

        html = "<html><body><table></table></body></html>"
        parser = MtsamplesParser()
        urls = parser.parse_sample_listing(html)
        self.assertEqual(urls, [])

    def test_parse_sample_listing_deduplicates_urls(self):
        """Given a sample listing HTML with duplicate links
        When parse_sample_listing is called
        Then it returns unique URLs only."""
        from providers.mtsamples._parser import MtsamplesParser

        html = """
        <html><body>
        <table>
            <tr><td><a href="sample.asp?sample=123">Sample 1</a></td></tr>
            <tr><td><a href="sample.asp?sample=123">Sample 1 Again</a></td></tr>
        </table>
        </body></html>
        """
        parser = MtsamplesParser()
        urls = parser.parse_sample_listing(html)
        self.assertEqual(len(urls), 1)


# =============================================================================
# Category Page Parsing
# =============================================================================

class TestParseCategories(unittest.TestCase):
    """parse_categories() extracts category links from the main index page."""

    def test_can_parse_category_links_from_sidebar(self):
        """Given a main page HTML with sidebar category links
        When parse_categories is called
        Then it returns a list of category dicts with name and url."""
        from providers.mtsamples._parser import MtsamplesParser

        html = """
        <html><body>
        <div class="sideBar">
            <a href="browse.asp?type=10-Cardiovascular">Cardiovascular</a>
            <a href="browse.asp?type=20-Orthopedics">Orthopedics</a>
        </div>
        </body></html>
        """
        parser = MtsamplesParser()
        categories = parser.parse_categories(html)
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0]["name"], "Cardiovascular")

    def test_parse_categories_returns_empty_on_no_sidebar(self):
        """Given a page HTML with no sidebar
        When parse_categories is called
        Then it returns an empty list."""
        from providers.mtsamples._parser import MtsamplesParser

        html = "<html><body><div>No sidebar here</div></body></html>"
        parser = MtsamplesParser()
        categories = parser.parse_categories(html)
        self.assertEqual(categories, [])


# =============================================================================
# Individual Sample Page Parsing
# =============================================================================

class TestParseSamplePage(unittest.TestCase):
    """parse_sample_page() extracts MedicalSample from a sample content page."""

    def test_can_extract_title_from_h1(self):
        """Given a sample page HTML with an h1 title
        When parse_sample_page is called
        Then the returned MedicalSample has the correct title."""
        from providers.mtsamples._parser import MtsamplesParser

        html = """
        <html><body>
        <h1>Knee Arthroscopy Case</h1>
        <div id="sampletext">
            <p>Patient scheduled for arthroscopic surgery...</p>
        </div>
        </body></html>
        """
        parser = MtsamplesParser()
        sample = parser.parse_sample_page(html, "https://www.mtsamples.com/sample.asp?sample=456")
        self.assertEqual(sample.title, "Knee Arthroscopy Case")

    def test_can_extract_content_from_sampletext_div(self):
        """Given a sample page HTML with a sampletext div
        When parse_sample_page is called
        Then the returned MedicalSample has content from that div."""
        from providers.mtsamples._parser import MtsamplesParser

        html = """
        <html><body>
        <h1>Heart Surgery</h1>
        <div id="sampletext">
            <p>Patient presented with chest pain and shortness of breath.</p>
            <p>ECG showed abnormal readings.</p>
        </div>
        </body></html>
        """
        parser = MtsamplesParser()
        sample = parser.parse_sample_page(html, "https://www.mtsamples.com/sample.asp?sample=123")
        self.assertIn("chest pain", sample.content)

    def test_parse_sample_page_returns_medical_sample(self):
        """Given a valid sample page HTML
        When parse_sample_page is called
        Then it returns a MedicalSample instance."""
        from providers.mtsamples._parser import MtsamplesParser

        html = """
        <html><body>
        <h1>Sample Title</h1>
        <div id="sampletext"><p>Content here</p></div>
        </body></html>
        """
        parser = MtsamplesParser()
        sample = parser.parse_sample_page(html, "https://www.mtsamples.com/sample")
        self.assertIsInstance(sample, MedicalSample)

    def test_parse_sample_page_raises_error_on_missing_sampletext(self):
        """Given a sample page HTML without sampletext div
        When parse_sample_page is called
        Then ProviderParseError is raised."""
        from providers.mtsamples._parser import MtsamplesParser

        html = "<html><body><h1>No Content</h1></body></html>"
        parser = MtsamplesParser()
        with self.assertRaises(ProviderParseError):
            parser.parse_sample_page(html, "https://www.mtsamples.com/sample")

    def test_parse_sample_page_extracts_keywords(self):
        """Given a sample page HTML with keywords section
        When parse_sample_page is called
        Then the returned MedicalSample has description from keywords."""
        from providers.mtsamples._parser import MtsamplesParser

        html = """
        <html><body>
        <h1>Heart Surgery</h1>
        <div id="sampletext">
            <p>Patient presented with chest pain...</p>
        </div>
        <div>Keywords:</div>
        <div>cardiac, surgery, ECG, chest pain</div>
        </body></html>
        """
        parser = MtsamplesParser()
        sample = parser.parse_sample_page(html, "https://www.mtsamples.com/sample")
        self.assertIn("cardiac", sample.description)

    def test_parse_sample_page_extracts_category_from_url(self):
        """Given a sample page HTML and the category is inferable
        When parse_sample_page is called
        Then the returned MedicalSample has category field."""
        from providers.mtsamples._parser import MtsamplesParser

        html = """
        <html><body>
        <h1>Cardiac Case</h1>
        <div id="sampletext"><p>Content</p></div>
        </body></html>
        """
        parser = MtsamplesParser()
        sample = parser.parse_sample_page(html, "https://www.mtsamples.com/sample")
        self.assertIsInstance(sample.category, str)


# =============================================================================
# Error Handling
# =============================================================================

class TestParserErrorHandling(unittest.TestCase):
    """Parser handles malformed HTML gracefully."""

    def test_parse_sample_listing_handles_invalid_html(self):
        """Given malformed HTML input
        When parse_sample_listing is called
        Then it returns an empty list rather than raising."""
        from providers.mtsamples._parser import MtsamplesParser

        html = "not valid html at all <>"
        parser = MtsamplesParser()
        urls = parser.parse_sample_listing(html)
        self.assertEqual(urls, [])

    def test_parse_categories_handles_invalid_html(self):
        """Given malformed HTML input
        When parse_categories is called
        Then it returns an empty list rather than raising."""
        from providers.mtsamples._parser import MtsamplesParser

        html = "not valid html at all <>"
        parser = MtsamplesParser()
        categories = parser.parse_categories(html)
        self.assertEqual(categories, [])


if __name__ == "__main__":
    unittest.main()