# SPDX-License-Identifier: MPL-2.0
"""Trivial web search stub."""
from __future__ import annotations


class WebSearch:
    def search(self, query: str) -> str:
        return f"Results for {query}"
