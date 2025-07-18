"""
Story Types and SubTypes Implementation

This module implements the seven classical story types and their subtypes
as described in narrative theory.
"""

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class StorySubType:
    """Represents a specific subtype within a story type."""
    name: str
    description: str
    examples: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


@dataclass
class StoryType:
    """Base class for all story types."""
    name: str
    description: str
    subtypes: List[StorySubType] = field(default_factory=list)
    narrative_elements: Optional[str] = None
    key_theme: Optional[str] = None
    emotional_arc: Optional[str] = None
    common_elements: List[str] = field(default_factory=list)
    
    def add_subtype(self, subtype: StorySubType) -> None:
        """Add a subtype to this story type."""
        self.subtypes.append(subtype)
    
    def get_subtype(self, name: str) -> Optional[StorySubType]:
        """Get a subtype by name."""
        for subtype in self.subtypes:
            if subtype.name.lower() == name.lower():
                return subtype
        return None
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class OvercomingTheMonster(StoryType):
    """Hero faces a great evil or threat."""
    
    def __init__(self):
        super().__init__(
            name="Overcoming the Monster",
            description="Hero faces a great evil or threat",
            narrative_elements="Anticipation → Dream → Frustration → Nightmare → Thrilling Escape"
        )
        
        # Add subtypes
        self.add_subtype(StorySubType(
            name="Predator",
            description="The monster actively hunts or terrorizes",
            examples=["Jaws", "Alien"]
        ))
        
        self.add_subtype(StorySubType(
            name="Holdfast",
            description="The monster guards something precious",
            examples=["The Hobbit's Smaug"]
        ))
        
        self.add_subtype(StorySubType(
            name="Avenger",
            description="The monster retaliates for past wrongs",
            examples=["Dracula"]
        ))


class RagsToRiches(StoryType):
    """Protagonist rises from humble beginnings to greatness."""
    
    def __init__(self):
        super().__init__(
            name="Rags to Riches",
            description="Protagonist rises from humble beginnings to greatness",
            key_theme="Inner transformation is more important than material gain"
        )
        
        # Add subtypes
        self.add_subtype(StorySubType(
            name="Pure Ascent",
            description="The hero rises steadily",
            examples=["Cinderella"]
        ))
        
        self.add_subtype(StorySubType(
            name="Fall and Redemption",
            description="Gains are lost before true growth",
            examples=["The Prince and the Pauper"]
        ))
        
        self.add_subtype(StorySubType(
            name="False Riches",
            description="Superficial success masks inner emptiness",
            examples=["The Great Gatsby"]
        ))


class TheQuest(StoryType):
    """A journey with companions, trials, and a goal."""
    
    def __init__(self):
        super().__init__(
            name="The Quest",
            description="A journey with companions, trials, and a goal",
            common_elements=["Companions", "trials", "temptations", "symbolic landscapes"]
        )
        
        # Add subtypes
        self.add_subtype(StorySubType(
            name="Object Quest",
            description="Seeking a treasure or artifact",
            examples=["Indiana Jones"]
        ))
        
        self.add_subtype(StorySubType(
            name="Person Quest",
            description="Rescuing or finding someone",
            examples=["Finding Nemo"]
        ))
        
        self.add_subtype(StorySubType(
            name="Spiritual Quest",
            description="Seeking enlightenment or truth",
            examples=["The Divine Comedy"]
        ))


class VoyageAndReturn(StoryType):
    """Hero enters a strange world and returns transformed."""
    
    def __init__(self):
        super().__init__(
            name="Voyage and Return",
            description="Hero enters a strange world and returns transformed",
            emotional_arc="Naïveté → Danger → Escape → Wisdom"
        )
        
        # Add subtypes
        self.add_subtype(StorySubType(
            name="Fantasy Realm",
            description="Magical or surreal world",
            examples=["Alice in Wonderland"]
        ))
        
        self.add_subtype(StorySubType(
            name="Time Travel or Sci-Fi",
            description="Unfamiliar future or past",
            examples=["Back to the Future"]
        ))
        
        self.add_subtype(StorySubType(
            name="Psychological Journey",
            description="Internal transformation",
            examples=["Brideshead Revisited"]
        ))


class Comedy(StoryType):
    """Confusion and miscommunication resolved in harmony."""
    
    def __init__(self):
        super().__init__(
            name="Comedy",
            description="Confusion and miscommunication resolved in harmony"
        )
        
        # Add subtypes
        self.add_subtype(StorySubType(
            name="Romantic Comedy",
            description="Misunderstandings resolved in love",
            examples=["Much Ado About Nothing"]
        ))
        
        self.add_subtype(StorySubType(
            name="Social Comedy",
            description="Satire of norms and class",
            examples=["The Importance of Being Earnest"]
        ))
        
        self.add_subtype(StorySubType(
            name="Farce",
            description="Exaggerated chaos and absurdity",
            examples=["The Big Lebowski"]
        ))


class Tragedy(StoryType):
    """A fatal flaw leads to downfall."""
    
    def __init__(self):
        super().__init__(
            name="Tragedy",
            description="A fatal flaw leads to downfall",
            emotional_arc="Rise → Fall → Catharsis"
        )
        
        # Add subtypes
        self.add_subtype(StorySubType(
            name="Fatal Flaw",
            description="Hubris or obsession leads to downfall",
            examples=["Macbeth"]
        ))
        
        self.add_subtype(StorySubType(
            name="Innocent Victim",
            description="External forces destroy the hero",
            examples=["Romeo and Juliet"]
        ))
        
        self.add_subtype(StorySubType(
            name="Corruption Arc",
            description="Moral decay leads to collapse",
            examples=["Citizen Kane"]
        ))


class Rebirth(StoryType):
    """Hero is redeemed or transformed."""
    
    def __init__(self):
        super().__init__(
            name="Rebirth",
            description="Hero is redeemed or transformed",
            key_theme="A symbolic 'death' followed by renewal"
        )
        
        # Add subtypes
        self.add_subtype(StorySubType(
            name="Seasonal Rebirth",
            description="Tied to cycles of nature or holidays",
            examples=["A Christmas Carol"]
        ))
        
        self.add_subtype(StorySubType(
            name="Romantic Rebirth",
            description="Love transforms the character",
            examples=["Beauty and the Beast"]
        ))
        
        self.add_subtype(StorySubType(
            name="Existential Rebirth",
            description="Awakening from despair or nihilism",
            examples=["Groundhog Day"]
        ))


class StoryTypeRegistry:
    """Registry for all story types."""
    
    def __init__(self):
        self._story_types = {
            "overcoming_the_monster": OvercomingTheMonster(),
            "rags_to_riches": RagsToRiches(),
            "the_quest": TheQuest(),
            "voyage_and_return": VoyageAndReturn(),
            "comedy": Comedy(),
            "tragedy": Tragedy(),
            "rebirth": Rebirth()
        }
    
    def get_story_type(self, name: str) -> Optional[StoryType]:
        """Get a story type by name."""
        return self._story_types.get(name.lower().replace(" ", "_"))
    
    def get_all_story_types(self) -> List[StoryType]:
        """Get all story types."""
        return list(self._story_types.values())
    
    def list_story_types(self) -> List[str]:
        """List all story type names."""
        return [story_type.name for story_type in self._story_types.values()]