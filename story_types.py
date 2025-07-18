"""
Story Types and SubTypes Implementation

This module implements the seven classical story types and their subtypes
as described in narrative theory.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import os


class StoryTypeEnum(Enum):
    """Enum for story type names."""
    OVERCOMING_THE_MONSTER = "Overcoming the Monster"
    RAGS_TO_RICHES = "Rags to Riches"
    THE_QUEST = "The Quest"
    VOYAGE_AND_RETURN = "Voyage and Return"
    COMEDY = "Comedy"
    TRAGEDY = "Tragedy"
    REBIRTH = "Rebirth"


class GenreEnum(Enum):
    """Enum for genre names."""
    FANTASY = "Fantasy"
    SCIENCE_FICTION = "Science Fiction"
    WESTERN = "Western"
    MYSTERY = "Mystery"
    THRILLER = "Thriller"
    HORROR = "Horror"
    ROMANCE = "Romance"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    ADVENTURE = "Adventure"
    HISTORICAL = "Historical"
    CRIME = "Crime"
    ACTION = "Action"
    DOCUMENTARY = "Documentary"
    MUSICAL = "Musical"


class SubGenreEnum(Enum):
    """Enum for sub-genre names."""
    # Fantasy subgenres
    HIGH_FANTASY = "High Fantasy"
    URBAN_FANTASY = "Urban Fantasy"
    DARK_FANTASY = "Dark Fantasy"
    MYTHIC_FANTASY = "Mythic Fantasy"
    FAIRY_TALE_RETELLING = "Fairy Tale Retelling"
    PORTAL_FANTASY = "Portal Fantasy"
    SWORD_AND_SORCERY = "Sword & Sorcery"
    
    # Science Fiction subgenres
    HARD_SCI_FI = "Hard Sci-Fi"
    CYBERPUNK = "Cyberpunk"
    SPACE_OPERA = "Space Opera"
    TIME_TRAVEL = "Time Travel"
    GENETIC_AI_SCI_FI = "Genetic/AI Sci-Fi"
    TECHNO_DYSTOPIA = "Techno-Dystopia"
    
    # Western subgenres
    CLASSIC_WESTERN = "Classic Western"
    REVISIONIST = "Revisionist"
    NEO_WESTERN = "Neo-Western"
    SCI_FI_WESTERN = "Sci-Fi Western"
    
    # Mystery subgenres
    COZY_MYSTERY = "Cozy Mystery"
    NOIR_DETECTIVE = "Noir Detective"
    PROCEDURAL = "Procedural"
    LOCKED_ROOM = "Locked Room"
    
    # Thriller subgenres
    PSYCHOLOGICAL = "Psychological"
    CRIME_THRILLER = "Crime Thriller"
    POLITICAL = "Political"
    TECH_CYBER = "Tech/Cyber"
    
    # Horror subgenres
    PSYCHOLOGICAL_HORROR = "Psychological Horror"
    SUPERNATURAL_HORROR = "Supernatural Horror"
    SLASHER = "Slasher"
    BODY_HORROR = "Body Horror"
    COSMIC_HORROR = "Cosmic Horror"
    
    # Romance subgenres
    HISTORICAL_ROMANCE = "Historical Romance"
    ROMANTIC_COMEDY = "Romantic Comedy"
    FANTASY_ROMANCE = "Fantasy Romance"
    TRAGIC_ROMANCE = "Tragic Romance"
    ENEMIES_TO_LOVERS = "Enemies to Lovers"
    
    # Comedy subgenres
    SLAPSTICK = "Slapstick"
    SATIRE = "Satire"
    DARK_COMEDY = "Dark Comedy"
    ROMANTIC_COMEDY_GENRE = "Romantic Comedy"  # Different from Romance's Romantic Comedy
    
    # Drama subgenres
    FAMILY_DRAMA = "Family Drama"
    LEGAL_DRAMA = "Legal Drama"
    COMING_OF_AGE = "Coming-of-Age"
    TRAGEDY = "Tragedy"
    
    # Adventure subgenres
    SURVIVAL = "Survival"
    TREASURE_HUNT = "Treasure Hunt"
    EXPEDITION = "Expedition"
    SWASHBUCKLING = "Swashbuckling"
    
    # Historical subgenres
    WAR_TIME = "War-Time"
    BIOGRAPHICAL = "Biographical"
    PERIOD_PIECE = "Period Piece"
    ALT_HISTORY = "Alt-History"
    
    # Crime subgenres
    HEIST = "Heist"
    MOB_DRAMA = "Mob Drama"
    SERIAL_CRIMES = "Serial Crimes"
    COURTROOM = "Courtroom"
    
    # Action subgenres
    SPY_THRILLER = "Spy Thriller"
    MARTIAL_ARTS = "Martial Arts"
    SUPERHERO = "Superhero"
    DISASTER = "Disaster"
    MILITARY_OPS = "Military Ops"
    
    # Documentary subgenres
    NATURE_AND_SCIENCE = "Nature & Science"
    SOCIAL_ISSUES = "Social Issues"
    BIOGRAPHY = "Biography"
    EXPLORATION = "Exploration"
    
    # Musical subgenres
    CLASSIC_BROADWAY_STYLE = "Classic Broadway Style"
    MODERN_POP_MUSICAL = "Modern Pop Musical"
    ANIMATED_MUSICAL = "Animated Musical"
    HISTORICAL_MUSICAL = "Historical Musical"


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
    examples: List[str] = field(default_factory=list)
    subtypes: List[StorySubType] = field(default_factory=list)
    characteristics: Dict[str, Any] = field(default_factory=dict)
    
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
    
    @property
    def narrative_elements(self) -> Optional[str]:
        """Get narrative elements from characteristics."""
        return self.characteristics.get("narrative_elements")
    
    @property
    def key_theme(self) -> Optional[str]:
        """Get key theme from characteristics."""
        return self.characteristics.get("key_theme")
    
    @property
    def emotional_arc(self) -> Optional[str]:
        """Get emotional arc from characteristics."""
        return self.characteristics.get("emotional_arc")
    
    @property
    def common_elements(self) -> List[str]:
        """Get common elements from characteristics."""
        return self.characteristics.get("common_elements", [])


@dataclass
class SubGenre:
    """Represents a specific sub-genre within a genre."""
    name: str
    archetypes: List[str] = field(default_factory=list)
    plot: str = ""
    examples: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"{self.name}: {self.plot}"


@dataclass
class Genre:
    """Base class for all genres."""
    name: str
    subgenres: List[SubGenre] = field(default_factory=list)
    
    def add_subgenre(self, subgenre: SubGenre) -> None:
        """Add a sub-genre to this genre."""
        self.subgenres.append(subgenre)
    
    def get_subgenre(self, name: str) -> Optional[SubGenre]:
        """Get a sub-genre by name."""
        for subgenre in self.subgenres:
            if subgenre.name.lower() == name.lower():
                return subgenre
        return None
    
    def __str__(self) -> str:
        return f"{self.name} ({len(self.subgenres)} sub-genres)"


@dataclass
class Archetype:
    """Represents a character archetype."""
    name: str
    description: str
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class ArchetypeRegistry:
    """Registry for all character archetypes."""
    
    def __init__(self):
        """Initialize registry with archetypes from JSONL data."""
        # Use default data file in the data directory
        data_file = os.path.join(os.path.dirname(__file__), "data", "archetypes.jsonl")
        
        self._archetypes = {}
        self._load_from_jsonl(data_file)
    
    def _load_from_jsonl(self, file_path: str) -> None:
        """Load archetypes from JSONL file."""
        import json
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('//'):  # Skip empty lines and comments
                    # Remove trailing comma if present
                    if line.endswith(','):
                        line = line[:-1]
                    
                    try:
                        archetype_data = json.loads(line)
                        archetype = Archetype(
                            name=archetype_data['name'],
                            description=archetype_data['description']
                        )
                        # Store with normalized key
                        key = archetype_data['name'].lower().replace(" ", "_")
                        self._archetypes[key] = archetype
                    except json.JSONDecodeError:
                        # Skip malformed lines
                        continue
    
    def get_archetype(self, name: str) -> Optional[Archetype]:
        """Get an archetype by name."""
        return self._archetypes.get(name.lower().replace(" ", "_"))
    
    def get_all_archetypes(self) -> List[Archetype]:
        """Get all archetypes."""
        return list(self._archetypes.values())
    
    def list_archetype_names(self) -> List[str]:
        """List all archetype names."""
        return [archetype.name for archetype in self._archetypes.values()]
    
    def search_archetypes(self, search_term: str) -> List[Archetype]:
        """Search for archetypes by name or description."""
        search_term = search_term.lower()
        results = []
        
        for archetype in self._archetypes.values():
            if (search_term in archetype.name.lower() or 
                search_term in archetype.description.lower()):
                results.append(archetype)
        
        return results


class StoryTypeRegistry:
    """Registry for all story types."""
    
    def __init__(self):
        """Initialize registry with story types from JSON data."""
        # Use default data file in the data directory
        data_file = os.path.join(os.path.dirname(__file__), "data", "story_types_data.json")
        
        self._story_types = {}
        self._load_from_json(data_file)
    
    def _load_from_json(self, file_path: str) -> None:
        """Load story types from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for story_type_data in data['story_types']:
            # Create subtypes
            subtypes = []
            for subtype_data in story_type_data.get('subtypes', []):
                subtype = StorySubType(
                    name=subtype_data['name'],
                    description=subtype_data['description'],
                    examples=subtype_data.get('examples', [])
                )
                subtypes.append(subtype)
            
            # Create story type
            story_type = StoryType(
                name=story_type_data['name'],
                description=story_type_data['description'],
                examples=story_type_data.get('examples', []),
                subtypes=subtypes,
                characteristics=story_type_data.get('characteristics', {})
            )
            
            # Store with normalized key
            key = story_type_data['name'].lower().replace(" ", "_")
            self._story_types[key] = story_type
    
    def get_story_type(self, name: str) -> Optional[StoryType]:
        """Get a story type by name."""
        return self._story_types.get(name.lower().replace(" ", "_"))
    
    def get_all_story_types(self) -> List[StoryType]:
        """Get all story types."""
        return list(self._story_types.values())
    
    def list_story_types(self) -> List[str]:
        """List all story type names."""
        return [story_type.name for story_type in self._story_types.values()]


class GenreRegistry:
    """Registry for all genres."""
    
    def __init__(self):
        """Initialize registry with genres from JSON data."""
        # Use default data file in the data directory
        data_file = os.path.join(os.path.dirname(__file__), "data", "genres.json")
        
        self._genres = {}
        self._load_from_json(data_file)
    
    def _load_from_json(self, file_path: str) -> None:
        """Load genres from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for genre_data in data['genres']:
            # Create sub-genres
            subgenres = []
            for subgenre_data in genre_data.get('subgenres', []):
                subgenre = SubGenre(
                    name=subgenre_data['name'],
                    archetypes=subgenre_data.get('archetypes', []),
                    plot=subgenre_data.get('plot', ''),
                    examples=subgenre_data.get('examples', [])
                )
                subgenres.append(subgenre)
            
            # Create genre
            genre = Genre(
                name=genre_data['name'],
                subgenres=subgenres
            )
            
            # Store with normalized key
            key = genre_data['name'].lower().replace(" ", "_")
            self._genres[key] = genre
    
    def get_genre(self, name: str) -> Optional[Genre]:
        """Get a genre by name."""
        return self._genres.get(name.lower().replace(" ", "_"))
    
    def get_all_genres(self) -> List[Genre]:
        """Get all genres."""
        return list(self._genres.values())
    
    def list_genres(self) -> List[str]:
        """List all genre names."""
        return [genre.name for genre in self._genres.values()]