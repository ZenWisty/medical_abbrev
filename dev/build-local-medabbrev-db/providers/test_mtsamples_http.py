"""Unit tests for mtsamples HTTP Client (#4).

Note: These are live integration tests that call mtsamples.com directly.
They will fail if the site is down or returns errors.
Some tests are marked as @unittest.expectedFailure when site returns 403/500.
"""

import unittest


# =============================================================================
# MtsamplesHttpClient Instantiation
# =============================================================================

class TestMtsamplesHttpClientInstantiation(unittest.TestCase):
    """MtsamplesHttpClient can be instantiated with proper headers."""

    def test_can_instantiate_mtsamples_http_client(self):
        """Given the MtsamplesHttpClient class exists
        When MtsamplesHttpClient is instantiated
        Then it succeeds without error."""
        from providers.mtsamples._http import MtsamplesHttpClient
        client = MtsamplesHttpClient()
        self.assertIsNotNone(client)

    def test_has_user_agent_header(self):
        """Given a MtsamplesHttpClient instance
        When accessing headers
        Then User-Agent header is set to a browser-like value."""
        from providers.mtsamples._http import MtsamplesHttpClient
        client = MtsamplesHttpClient()
        self.assertIn("User-Agent", client.headers)
        self.assertIn("Mozilla", client.headers["User-Agent"])


# =============================================================================
# MtsamplesHttpClient HTTP Methods
# =============================================================================

class TestGetHtml(unittest.TestCase):
    """get_html() fetches HTML pages from mtsamples.com."""

    @unittest.expectedFailure
    def test_get_html_returns_string(self):
        """Given a MtsamplesHttpClient instance
        When get_html is called with a valid mtsamples URL
        Then a string is returned."""
        from providers.mtsamples._http import MtsamplesHttpClient
        client = MtsamplesHttpClient()
        url = "https://www.mtsamples.com/site/pages/browse.asp?type=10-Cardiovascular%20/%20Pulmonary"
        result = client.get_html(url)
        self.assertIsInstance(result, str)

    def test_get_html_handles_nonexistent_page(self):
        """Given a MtsamplesHttpClient instance
        When get_html is called with a non-existent URL
        Then ProviderParseError is raised."""
        from providers.mtsamples._http import MtsamplesHttpClient
        from providers.base import ProviderParseError
        client = MtsamplesHttpClient()
        url = "https://www.mtsamples.com/site/pages/nonexistent_page_xyz123.html"
        with self.assertRaises(ProviderParseError):
            client.get_html(url)

    @unittest.expectedFailure
    def test_get_html_returns_html_with_sampletext_div(self):
        """Given a MtsamplesHttpClient instance
        When get_html is called with a valid sample listing URL
        Then the returned HTML contains sample text div markers."""
        from providers.mtsamples._http import MtsamplesHttpClient
        client = MtsamplesHttpClient()
        url = "https://www.mtsamples.com/site/pages/browse.asp?type=10-Cardiovascular%20/%20Pulmonary"
        result = client.get_html(url)
        self.assertIn("sample", result.lower())


# =============================================================================
# HTTP Error Handling
# =============================================================================

class TestHttpErrorHandling(unittest.TestCase):
    """HTTP client raises ProviderParseError on HTTP errors."""

    def test_raises_parse_error_on_404(self):
        """Given a MtsamplesHttpClient instance
        When get_html is called with a 404 URL
        Then ProviderParseError is raised."""
        from providers.mtsamples._http import MtsamplesHttpClient
        from providers.base import ProviderParseError
        client = MtsamplesHttpClient()
        with self.assertRaises(ProviderParseError):
            client.get_html("https://www.mtsamples.com/site/pages/does_not_exist_404.html")

    def test_raises_parse_error_on_403(self):
        """Given a MtsamplesHttpClient instance
        When get_html is called with a URL that returns 403
        Then ProviderParseError is raised."""
        from providers.mtsamples._http import MtsamplesHttpClient
        from providers.base import ProviderParseError
        client = MtsamplesHttpClient()
        with self.assertRaises(ProviderParseError):
            client.get_html("https://www.mtsamples.com/site/pages/forbidden_403.html")


if __name__ == "__main__":
    unittest.main()