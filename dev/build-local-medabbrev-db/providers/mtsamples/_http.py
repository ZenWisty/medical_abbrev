"""HTTP client for mtsamples.com."""

import requests

from providers.base import ProviderParseError


class MtsamplesHttpClient:
    """HTTP client for fetching pages from mtsamples.com.

    Uses browser-like headers to avoid 403/406 responses.
    """

    BASE_URL = "https://www.mtsamples.com"

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_html(self, url: str) -> str:
        """Fetch an HTML page from mtsamples.com.

        Args:
            url: Full URL to fetch

        Returns:
            Raw HTML content as string

        Raises:
            ProviderParseError: If the HTTP response status is not 200
        """
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code != 200:
                raise ProviderParseError(
                    f"HTTP {response.status_code} for URL: {url}"
                )
            return response.text
        except requests.RequestException as exc:
            raise ProviderParseError(f"Request failed for {url}: {exc}") from exc