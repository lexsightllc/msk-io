# SPDX-License-Identifier: MPL-2.0
"""Placeholder image generator."""
from __future__ import annotations

import numpy as np
from PIL import Image


class ImageGenerator:
    def generate(self, size: int = 64) -> Image.Image:
        arr = (np.random.rand(size, size) * 255).astype("uint8")
        return Image.fromarray(arr)
