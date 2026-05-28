"""HTML parser for mtsamples.com pages.

Extracts medical samples, categories, and abbreviation information
from fetched HTML pages.
"""

from bs4 import BeautifulSoup

from providers.base import ProviderParseError
from providers.data_models import MedicalSample


class MtsamplesParser:
    """Parser for mtsamples.com HTML pages.

    Uses BeautifulSoup for HTML parsing. Handles malformed HTML gracefully
    by returning empty results rather than raising exceptions.
    """

    BASE_URL = "https://www.mtsamples.com"

    def parse_sample_listing(self, html: str) -> list[str]:
        """Extract sample URLs from a category listing page.

        Args:
            html: Raw HTML content from a category page

        Returns:
            List of absolute sample URLs
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
        except Exception:
            return []

        urls = []
        for link in soup.select("table td a"):
            href = link.get("href", "")
            if "sample.asp?sample=" in href:
                full_url = self._make_absolute_url(href)
                if full_url:
                    urls.append(full_url)

        return list(set(urls))  # deduplicate

    def parse_categories(self, html: str) -> list[dict]:
        """Extract category links from the main index page sidebar.

        Args:
            html: Raw HTML content from the main page

        Returns:
            List of dicts with 'name' and 'url' keys
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
        except Exception:
            return []

        categories = []
        for link in soup.select("div.sideBar a"):
            href = link.get("href", "")
            if "type=" in href:
                name = link.text.strip()
                full_url = self._make_absolute_url(href)
                if name and full_url:
                    categories.append({"name": name, "url": full_url})

        return categories

    def parse_sample_page(self, html: str, url: str) -> MedicalSample:
        """Extract a MedicalSample from an individual sample content page.

        Args:
            html: Raw HTML content from a sample page
            url: The URL this page was fetched from

        Returns:
            MedicalSample instance

        Raises:
            ProviderParseError: If the HTML does not contain expected structure
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
        except Exception as exc:
            raise ProviderParseError(f"Failed to parse HTML: {exc}") from exc

        # Find the main content div
        sampletext_div = soup.find("div", id="sampletext")
        if not sampletext_div:
            raise ProviderParseError("Sample page missing 'sampletext' div")

        # Extract title from h1
        title = ""
        h1 = soup.find("h1")
        if h1:
            title = h1.text.strip()

        # Extract content from paragraphs in sampletext
        content_parts = []
        for elem in sampletext_div.find_all(["p", "b"]):
            text = elem.text.strip()
            if text:
                content_parts.append(text)
        content = "\n".join(content_parts)

        # Extract description/keywords from the keywords section
        description = self._extract_keywords(soup)

        # Extract category from URL if possible
        category = self._extract_category_from_url(url)

        # Generate an ID from the URL
        sample_id = self._extract_id_from_url(url)

        return MedicalSample(
            id=sample_id,
            title=title,
            category=category,
            description=description,
            content=content,
            url=url,
        )

    def _make_absolute_url(self, href: str) -> str | None:
        """Convert a relative href to an absolute URL."""
        if href.startswith("http"):
            return href
        if href.startswith("/"):
            return self.BASE_URL + href
        if href.startswith("site/"):
            return f"{self.BASE_URL}/{href}"
        return f"{self.BASE_URL}/site/pages/{href}"

    def _extract_keywords(self, soup: BeautifulSoup) -> str:
        """Extract keywords/description from a sample page."""
        # Look for Keywords: pattern
        keywords_div = soup.find("div", string=lambda t: t and "Keywords" in str(t))
        if keywords_div:
            # Keywords is typically followed by another div with the actual keywords
            next_sibling = keywords_div.find_next_sibling()
            if next_sibling:
                return next_sibling.text.strip()

        # Fallback: look for any description in the page
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            return meta_desc.get("content", "")

        return ""

    def _extract_category_from_url(self, url: str) -> str:
        """Extract category name from URL if possible."""
        # URL pattern: browse.asp?type=10-Cardiovascular%20/%20Pulmonary
        if "type=" in url:
            try:
                type_part = url.split("type=")[1]
                # Extract category name (after the number and dash)
                if "-" in type_part:
                    return type_part.split("-", 1)[1].replace("%20", " ").replace("%2F", "/")
            except Exception:
                pass
        return "Unknown"

    def _extract_id_from_url(self, url: str) -> str:
        """Extract sample ID from URL."""
        # URL pattern: sample.asp?sample=123
        if "sample=" in url:
            try:
                return url.split("sample=")[1].split("&")[0]
            except Exception:
                pass
        # Fallback: use URL hash
        return str(hash(url))[:12]