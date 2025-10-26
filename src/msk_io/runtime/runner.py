# SPDX-License-Identifier: MPL-2.0
"""Minimal multi-agent runner."""
from __future__ import annotations

from typing import Iterable

from msk_io.runtime.agent import Agent
from msk_io.runtime.context import Context


class Runner:
    """Execute a list of agents sequentially."""

    def __init__(self, agents: Iterable[Agent]):
        self.agents = list(agents)

    def run(self, ctx: Context) -> Context:
        for agent in self.agents:
            ctx.data[agent.name] = agent.run(ctx.data)
        return ctx
