"""
VENOM Λ-Genesis (Lambda-Genesis) Package
Digital Organism Organ System

This package implements the Λ-Genesis layer of the VENOM system,
providing the core organs and biological-inspired computational framework.
"""

__version__ = "1.0.0"
__author__ = "VENOM Team"

from . import arbiter_core
from . import organs
from . import pulse
from . import mesh
from . import core

__all__ = [
    "arbiter_core",
    "organs",
    "pulse",
    "mesh",
    "core",
]
