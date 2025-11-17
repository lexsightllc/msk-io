# SPDX-License-Identifier: MPL-2.0
"""Context object passed between agents."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Context:
    data: dict[str, Any] = field(default_factory=dict)
