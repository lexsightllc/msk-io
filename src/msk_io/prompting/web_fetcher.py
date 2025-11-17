# SPDX-License-Identifier: MPL-2.0
"""Fetch web pages for prompt enrichment."""
from __future__ import annotations

import urllib.parse
import urllib.request
from typing import Final

# Security: Allowed URL schemes
ALLOWED_SCHEMES: Final[frozenset[str]] = frozenset(["http", "https"])


class WebFetcher:
    """Secure web content fetcher with URL validation.

    Validates URLs to prevent security issues like file:// access or
    other custom scheme exploitation.
    """

    def fetch(self, url: str, timeout: int = 30) -> str:
        """Fetch content from a URL with security validation.

        Parameters
        ----------
        url : str
            The URL to fetch. Must use http or https scheme.
        timeout : int, optional
            Timeout in seconds (default: 30).

        Returns
        -------
        str
            The decoded response content.

        Raises
        ------
        ValueError
            If URL scheme is not allowed.
        urllib.error.URLError
            If the URL cannot be accessed.
        """
        # Security: Validate URL scheme
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ALLOWED_SCHEMES:
            raise ValueError(
                f"Invalid URL scheme '{parsed.scheme}'. "
                f"Only {', '.join(ALLOWED_SCHEMES)} are allowed."
            )

        # Security: Validate URL has a network location
        if not parsed.netloc:
            raise ValueError("Invalid URL: missing network location")

        with urllib.request.urlopen(url, timeout=timeout) as resp:
            content: bytes = resp.read()
            return content.decode()
