# SPDX-License-Identifier: MPL-2.0
"""Handle PDF loading and page extraction.

SECURITY WARNING: This module uses pdfminer.six which has known vulnerabilities
related to pickle deserialization (CVE-502). Only process PDF files from trusted
sources. Never process PDFs from untrusted or user-uploaded sources without
additional sandboxing and security measures.
"""
from __future__ import annotations

from pathlib import Path

from pdfminer.high_level import extract_text


class PDFHandler:
    """Handle PDF text extraction with security considerations.

    WARNING: Only use with PDFs from trusted sources due to pdfminer.six
    vulnerabilities. Validate file paths and ensure proper access controls.
    """

    def load(self, path: Path) -> str:
        """Extract text from a PDF file.

        Parameters
        ----------
        path : Path
            Path to the PDF file. Must be from a trusted source.

        Returns
        -------
        str
            Extracted text from the PDF.

        Raises
        ------
        FileNotFoundError
            If the PDF file doesn't exist.
        ValueError
            If the path is invalid or potentially unsafe.
        """
        # Security: Validate path
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")

        # Security: Ensure path is absolute and normalized
        resolved_path = path.resolve()

        # Security: Check file size to prevent DoS
        max_size = 100 * 1024 * 1024  # 100MB
        if resolved_path.stat().st_size > max_size:
            raise ValueError(f"PDF file too large (max {max_size} bytes)")

        return extract_text(str(resolved_path))

    def split_pages(self, text: str) -> list[str]:
        """Split extracted text by page breaks.

        Parameters
        ----------
        text : str
            The extracted PDF text.

        Returns
        -------
        list[str]
            List of text content per page.
        """
        return text.split("\f")
