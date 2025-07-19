# Kraitif

A Python implementation of the seven classical story types and their subtypes based on narrative theory, plus character archetypes and writing styles.

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

## Writing Styles

The library includes 15 fundamental writing styles with characteristics and examples:

- **Concise** - Minimalist, efficient, no wasted words (Hemingway-esque)
- **Lyrical** - Musical, poetic, flowing rhythm (Toni Morrison, García Márquez)
- **Analytical** - Logical, structured, evidence-based (Orwell, academic writing)
- **Whimsical** - Playful, imaginative, quirky (Roald Dahl, Douglas Adams)
- **Descriptive** - Rich sensory detail, vivid imagery (Virginia Woolf, travel writing)
- **Conversational** - Informal, chatty, direct-to-reader (blog posts, memoirs)
- **Philosophical** - Abstract, reflective, probing big ideas (Camus, Dostoevsky)
- **Satirical** - Ironic, mocking, socially critical (Swift, Vonnegut)
- **Suspenseful** - Tension-building, cliffhangers, pacing (thrillers, horror)
- **Romantic** - Emotionally expressive, idealistic (Brontë sisters, romance novels)
- **Detached** - Objective, clinical, emotionally distant (McCarthy, Kafka)
- **Experimental** - Nonlinear, fragmented, rule-breaking (Joyce, postmodern fiction)
- **Journalistic** - Factual, timely, inverted pyramid structure (news articles)
- **Reflective** - Introspective, personal, meditative (memoirs, essays)
- **Persuasive** - Argument-driven, rhetorical, call-to-action (speeches, op-eds)

## Usage

```python
from story_types import StoryTypeRegistry, ArchetypeRegistry
from style import StyleRegistry

# Create registries
story_registry = StoryTypeRegistry()
archetype_registry = ArchetypeRegistry()
style_registry = StyleRegistry()

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

# Get all writing styles
styles = style_registry.get_all_styles()

# Get a specific writing style
concise = style_registry.get_style("Concise")

# Search for styles
emotional_styles = style_registry.search_styles("emotional")

# Print details
print(f"Story Type: {quest.name}")
print(f"Description: {quest.description}")
print(f"Subtype: {spiritual_quest.name}")
print(f"Examples: {', '.join(spiritual_quest.examples)}")
print(f"Archetype: {chosen_one.name}")
print(f"Archetype Description: {chosen_one.description}")
print(f"Writing Style: {concise.name}")
print(f"Style Description: {concise.description}")
print(f"Style Characteristics: {concise.characteristics}")
```

## Files

## Running the Demo

```bash
python3 demo.py
```

## Running the Flask Web Interface

```bash
python3 launch.py
```

Then open your web browser to [http://localhost:5000](http://localhost:5000)

## Running Tests

```bash
python3 tests/test_story_types.py
```

## Features

- Complete implementation of all 7 story types with 21 subtypes
- 108 character archetypes with descriptions
- 15 writing styles with characteristics and examples
- Narrative elements, themes, and emotional arcs
- Registry pattern for easy access
- Case-insensitive lookups
- Archetype and style search functionality
- Comprehensive test coverage
- Clean, object-oriented design using dataclasses
- **Flask web interface with black background theme**
- **Interactive navigation between story types and subtypes**
- **Responsive design for mobile and desktop**