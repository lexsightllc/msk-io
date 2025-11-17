# SPDX-License-Identifier: MPL-2.0
"""Simplified agent abstraction used by the Varkiel framework."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Agent:
    name: str
    tool: Callable[[Any], Any]

    def run(self, data: Any) -> Any:
        return self.tool(data)
