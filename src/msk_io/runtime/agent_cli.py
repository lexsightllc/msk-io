# SPDX-License-Identifier: MPL-2.0
"""CLI entry for the lightweight agent runtime."""
from __future__ import annotations

import typer

from msk_io.runtime.agent import Agent
from msk_io.runtime.context import Context
from msk_io.runtime.runner import Runner
from msk_io.runtime.tool import Tool

app = typer.Typer(add_completion=False)


@app.command()
def run() -> None:
    """Run a trivial agent pipeline."""
    tool = Tool("echo", lambda data: "ok")
    agent = Agent("agent1", tool)
    ctx = Context()
    Runner([agent]).run(ctx)
    typer.echo(ctx.data)


if __name__ == "__main__":  # pragma: no cover
    app()
