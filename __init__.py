"""
Kraitif - Story Types and SubTypes Library

A Python implementation of the seven classical story types and their subtypes.
"""

from .story_types import (
    StoryType,
    StorySubType,
    StoryTypeRegistry,
    OvercomingTheMonster,
    RagsToRiches,
    TheQuest,
    VoyageAndReturn,
    Comedy,
    Tragedy,
    Rebirth
)

__version__ = "1.0.0"
__all__ = [
    "StoryType",
    "StorySubType", 
    "StoryTypeRegistry",
    "OvercomingTheMonster",
    "RagsToRiches",
    "TheQuest",
    "VoyageAndReturn",
    "Comedy",
    "Tragedy",
    "Rebirth"
]