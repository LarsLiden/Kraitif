# Kraitif

A Python implementation of the seven classical story types and their subtypes based on narrative theory.

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

## Usage

```python
from story_types import StoryTypeRegistry

# Create a registry
registry = StoryTypeRegistry()

# Get all story types
story_types = registry.get_all_story_types()

# Get a specific story type
quest = registry.get_story_type("The Quest")

# Get a specific subtype
spiritual_quest = quest.get_subtype("Spiritual Quest")

# Print details
print(f"Story Type: {quest.name}")
print(f"Description: {quest.description}")
print(f"Subtype: {spiritual_quest.name}")
print(f"Examples: {', '.join(spiritual_quest.examples)}")
```

## Files

- `story_types.py` - Main implementation of story types and subtypes
- `demo.py` - Demonstration script showing all story types
- `app.py` - Flask web application providing a web interface
- `launch.py` - Launch script for the Flask application
- `templates/` - HTML templates for the web interface
- `static/` - CSS and static files for the web interface
- `tests/test_story_types.py` - Basic tests for the implementation

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

- Complete implementation of all 7 story types
- 21 subtypes with descriptions and examples
- Narrative elements, themes, and emotional arcs
- Registry pattern for easy access
- Case-insensitive lookups
- Comprehensive test coverage
- Clean, object-oriented design using dataclasses
- **Flask web interface with black background theme**
- **Interactive navigation between story types and subtypes**
- **Responsive design for mobile and desktop**