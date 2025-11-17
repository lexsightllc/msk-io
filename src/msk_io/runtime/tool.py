# SPDX-License-Identifier: MPL-2.0
"""Simple callable wrapper for tools."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Tool:
    name: str
    func: Callable[[Any], Any]

    def __call__(self, data: Any) -> Any:
        return self.func(data)
