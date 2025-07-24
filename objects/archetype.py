"""
Archetypes Implementation

This module implements character archetypes loaded from JSONL data.
"""

from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import json
import os


class ArchetypeEnum(Enum):
    """Enum for archetype names."""
    CHOSEN_ONE = "Chosen One"
    WISE_MENTOR = "Wise Mentor"
    LOYAL_COMPANION = "Loyal Companion"
    HIDDEN_MAGE = "Hidden Mage"
    SKEPTIC_DETECTIVE = "Skeptic Detective"
    FAE_TRICKSTER = "Fae Trickster"
    ANTI_HERO = "Anti-Hero"
    CURSED_WARRIOR = "Cursed Warrior"
    SINISTER_ADVISOR = "Sinister Advisor"
    DEMI_GOD = "Demi-God"
    SACRED_GUARDIAN = "Sacred Guardian"
    MORTAL_PROPHET = "Mortal Prophet"
    REIMAGINED_PRINCESS = "Reimagined Princess"
    WICKED_STEPMOTHER = "Wicked Stepmother"
    ORDINARY_YOUTH = "Ordinary Youth"
    SENTIENT_REALM = "Sentient Realm"
    GATEKEEPER = "Gatekeeper"
    BRASH_HERO = "Brash Hero"
    TOWER_WIZARD = "Tower Wizard"
    SEDUCTIVE_ROGUE = "Seductive Rogue"
    RATIONAL_SCIENTIST = "Rational Scientist"
    AI_COMPANION = "AI Companion"
    HACKER_REBEL = "Hacker Rebel"
    STREETWISE_MERCENARY = "Streetwise Mercenary"
    STARSHIP_CAPTAIN = "Starship Captain"
    GALACTIC_TYRANT = "Galactic Tyrant"
    TIME_WANDERER = "Time Wanderer"
    TIMELINE_ENFORCER = "Timeline Enforcer"
    ENHANCED_HUMAN = "Enhanced Human"
    ROGUE_AI = "Rogue AI"
    RESISTANCE_LEADER = "Resistance Leader"
    MONITORED_CITIZEN = "Monitored Citizen"
    GUNSLINGER = "Gunslinger"
    OUTLAW = "Outlaw"
    TOWN_SHERIFF = "Town Sheriff"
    FLAWED_HERO = "Flawed Hero"
    DISILLUSIONED_WAR_VET = "Disillusioned War Vet"
    RANCHER = "Rancher"
    URBAN_COP = "Urban Cop"
    LONE_AVENGER = "Lone Avenger"
    MECH_WRANGLER = "Mech Wrangler"
    SPACE_SHERIFF = "Space Sheriff"
    QUIRKY_SLEUTH = "Quirky Sleuth"
    NOSY_NEIGHBOR = "Nosy Neighbor"
    CYNICAL_PI = "Cynical PI"
    FEMME_FATALE = "Femme Fatale"
    FORENSICS_EXPERT = "Forensics Expert"
    ROOKIE_COP = "Rookie Cop"
    ISOLATED_GUESTS = "Isolated Guests"
    SILENT_WITNESS = "Silent Witness"
    UNSTABLE_PROTAGONIST = "Unstable Protagonist"
    MANIPULATIVE_PARTNER = "Manipulative Partner"
    FUGITIVE = "Fugitive"
    FRAMED_INNOCENT = "Framed Innocent"
    WHISTLEBLOWER = "Whistleblower"
    CORRUPT_OFFICIAL = "Corrupt Official"
    HACKER_HERO = "Hacker Hero"
    SYSTEM_ARCHITECT = "System Architect"
    FINAL_GIRL = "Final Girl"
    PARANORMAL_EXPERT = "Paranormal Expert"
    DOOMED_CARETAKER = "Doomed Caretaker"
    SINISTER_CHILD = "Sinister Child"
    ELDRITCH_ENTITY = "Eldritch Entity"
    SKEPTIC_TURNED_BELIEVER = "Skeptic Turned Believer"
    BROODING_LOVE_INTEREST = "Brooding Love Interest"
    OPTIMIST = "Optimist"
    MATCHMAKER = "Matchmaker"
    REBOUND = "Rebound"
    FORBIDDEN_FLAME = "Forbidden Flame"
    LOVABLE_FOOL = "Lovable Fool"
    OVERCONFIDENT_UNDERDOG = "Overconfident Underdog"
    NAIVE_GENIUS = "Naive Genius"
    DEADPAN_OBSERVER = "Deadpan Observer"
    SOCIAL_CLIMBER = "Social Climber"
    DISAPPOINTED_PARENT = "Disappointed Parent"
    IDEALISTIC_YOUTH = "Idealistic Youth"
    DISILLUSIONED_PROFESSIONAL = "Disillusioned Professional"
    QUIET_SUFFERER = "Quiet Sufferer"
    SPIRALING_GENIUS = "Spiraling Genius"
    RELUCTANT_EXPLORER = "Reluctant Explorer"
    SEASONED_GUIDE = "Seasoned Guide"
    BURDENED_SCHOLAR = "Burdened Scholar"
    RIVAL_ADVENTURER = "Rival Adventurer"
    CURIOUS_CHILD = "Curious Child"
    ENLIGHTENED_REVOLUTIONARY = "Enlightened Revolutionary"
    NOBLE_PEASANT = "Noble Peasant"
    WAR_WEARY_SOLDIER = "War-weary Soldier"
    SCHEMING_ARISTOCRAT = "Scheming Aristocrat"
    DOOMED_MONARCH = "Doomed Monarch"
    MASTERMIND = "Mastermind"
    COP_WITH_A_PAST = "Cop with a Past"
    UNDERCOVER_MOLE = "Undercover Mole"
    MANIPULATED_VICTIM = "Manipulated Victim"
    LAW_ABIDING_CITIZEN_TURNED_ROGUE = "Law-Abiding Citizen Turned Rogue"
    STOIC_WARRIOR = "Stoic Warrior"
    SIDEKICK_WITH_HEART = "Sidekick with Heart"
    GENIUS_STRATEGIST = "Genius Strategist"
    RELUCTANT_HERO = "Reluctant Hero"
    FALLEN_LEADER = "Fallen Leader"
    TRUTH_SEEKER = "Truth-Seeker"
    SUBJECT_MATTER_EXPERT = "Subject Matter Expert"
    RELUCTANT_WITNESS = "Reluctant Witness"
    CULTURAL_NARRATOR = "Cultural Narrator"
    ASPIRING_PERFORMER = "Aspiring Performer"
    MENTOR_MUSICIAN = "Mentor Musician"
    RIVAL_SINGER = "Rival Singer"
    HAUNTED_ARTIST = "Haunted Artist"
    HOPEFUL_YOUTH = "Hopeful Youth"


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
        data_file = os.path.join(os.path.dirname(__file__), "..", "data", "archetypes.jsonl")
        
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