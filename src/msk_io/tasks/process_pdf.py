"""Simple task to process a PDF using the internal agent runtime."""
from __future__ import annotations

from pathlib import Path

from msk_io.image_pipeline.pdf_handler import PDFHandler
from msk_io.runtime.agent import Agent
from msk_io.runtime.context import Context
from msk_io.runtime.runner import Runner
from msk_io.runtime.tool import Tool


def process(pdf_path: Path) -> Context:
    """Process a PDF document using the lightweight agent runtime."""
    handler = PDFHandler()
    tool = Tool("read", lambda _: handler.load(pdf_path))
    agent = Agent("reader", tool)
    runner = Runner([agent])
    return runner.run(Context())
