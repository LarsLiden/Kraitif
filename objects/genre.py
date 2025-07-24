"""
Genre and Sub-Genre Implementation

This module implements genres and sub-genres loaded from JSON data.
"""

from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import os


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


class GenreRegistry:
    """Registry for all genres."""
    
    def __init__(self):
        """Initialize registry with genres from JSON data."""
        # Use default data file in the data directory
        data_file = os.path.join(os.path.dirname(__file__), "..", "data", "genres.json")
        
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