# Kraitif

A Python implementation of the seven classical story types and their subtypes based on narrative theory, plus character archetypes.

## Story Types

This library implements the seven fundamental story types identified in narrative theory:

1. **Overcoming the Monster** - Hero faces a great evil or threat
2. **Rags to Riches** - Protagonist rises from humble beginnings to greatness
3. **The Quest** - A journey with companions, trials, and a goal
4. **Voyage and Return** - Hero enters a strange world and returns transformed
5. **Comedy** - Confusion and miscommunication resolved in harmony
6. **Tragedy** - A fatal flaw leads to downfall
7. **Rebirth** - Hero is redeemed or transformed

Each story type includes 3 subtypes with descriptions and examples.

## Character Archetypes

The library also includes 108 character archetypes that represent common character types found in literature and media, such as:

- **Chosen One** - A protagonist destined for greatness, often tied to prophecy or legacy
- **Wise Mentor** - An experienced guide who provides wisdom and training to the hero
- **Anti-Hero** - A morally ambiguous lead who seeks redemption or power through flawed means
- **Femme Fatale** - A seductive, manipulative figure hiding dangerous secrets
- And many more...

## Usage

```python
from story_types import StoryTypeRegistry, ArchetypeRegistry

# Create registries
story_registry = StoryTypeRegistry()
archetype_registry = ArchetypeRegistry()

# Get all story types
story_types = story_registry.get_all_story_types()

# Get a specific story type
quest = story_registry.get_story_type("The Quest")

# Get a specific subtype
spiritual_quest = quest.get_subtype("Spiritual Quest")

# Get all archetypes
archetypes = archetype_registry.get_all_archetypes()

# Get a specific archetype
chosen_one = archetype_registry.get_archetype("Chosen One")

# Search for archetypes
hero_archetypes = archetype_registry.search_archetypes("hero")

# Print details
print(f"Story Type: {quest.name}")
print(f"Description: {quest.description}")
print(f"Subtype: {spiritual_quest.name}")
print(f"Examples: {', '.join(spiritual_quest.examples)}")
print(f"Archetype: {chosen_one.name}")
print(f"Archetype Description: {chosen_one.description}")
```

## Files

- `story_types.py` - Main implementation of story types, subtypes, and archetypes
- `demo.py` - Demonstration script showing all story types and archetypes
- `tests/test_story_types.py` - Comprehensive tests for the implementation
- `data/` - Folder containing data files:
  - `story_types_data.json` - Story types and subtypes data
  - `archetypes.jsonl` - Character archetypes data

## Running the Demo

```bash
python3 demo.py
```

## Running Tests

```bash
python3 tests/test_story_types.py
```

## Features

- Complete implementation of all 7 story types with 21 subtypes
- 108 character archetypes with descriptions
- Narrative elements, themes, and emotional arcs
- Registry pattern for easy access
- Case-insensitive lookups
- Archetype search functionality
- Comprehensive test coverage
- Clean, object-oriented design using dataclasses