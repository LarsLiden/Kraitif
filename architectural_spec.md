# Kraitif Architectural Specification

## Overview

Kraitif is built as a Flask web application using a modular, registry-based architecture. The system separates narrative data management, user interface concerns, and business logic into distinct layers for maintainability and extensibility.

**Note**: As of the latest update, all story-related object models and business logic have been reorganized into the `/objects` directory to improve code organization and separation of concerns. This includes story models, character systems, archetypes, genres, styles, and related registries, while keeping UI components (Flask app), AI integration, and utility scripts in the root directory.

## File Structure and Organization

```
Kraitif/
├── app.py                    # Main Flask application and routing
├── prompt.py                 # Prompt generation functions (plot and character prompts)
├── prompt_types.py           # Prompt type enumeration for AI debugging
├── launch.py                 # Simple application launcher
├── demo.py                   # Command-line demo script
├── requirements.txt          # Python dependencies
├── objects/                  # Core story object models and business logic
│   ├── __init__.py          # Objects package initialization
│   ├── story.py             # Core Story model and business logic
│   ├── story_types.py       # Story type definitions and registry
│   ├── archetype.py         # Character archetype registry, models, and ArchetypeEnum
│   ├── emotional_function.py # Emotional function registry, models, and EmotionalFunctionEnum
│   ├── functional_role.py   # Functional role registry, models, and FunctionalRoleEnum
│   ├── narrative_function.py # Narrative function registry, models, and NarrativeFunctionEnum
│   ├── character.py         # Character class combining archetype, functional role, emotional function
│   ├── character_parser.py  # Character and expanded plot line parsing from AI responses
│   ├── chapter.py          # Chapter class for story structure, planning, summary and continuity tracking
│   ├── continuity_character.py # ContinuityCharacter class for tracking character state
│   ├── continuity_object.py # ContinuityObject class for tracking object state
│   ├── continuity_state.py  # ContinuityState class for overall story state tracking
│   ├── plot_thread.py       # PlotThread class for tracking ongoing story threads
│   ├── genre.py             # Genre/sub-genre registry and models  
│   ├── style.py             # Writing style registry and models
│   └── plot_line.py         # PlotLine class for AI-generated plot lines
├── ai/                      # AI integration module
│   └── ai_client.py         # Azure OpenAI client with debugging support
├── data/                    # Narrative data files
│   ├── archetypes.jsonl     # Character archetype definitions
│   ├── emotional_functions.json # Emotional function definitions
│   ├── functional_roles.json # Functional role definitions
│   ├── narrative_functions.json # Narrative function definitions
│   └── [other data files]  # Genre, style data (JSON format)
├── debug/                   # AI prompt debugging files (excluded from git)
│   └── plot_lines.txt       # Latest plot generation prompt and response
├── templates/               # Jinja2 HTML templates
│   ├── base.html           # Base layout with two-panel structure
│   ├── story_types.html    # Story type selection page
│   ├── subtypes.html       # Story subtype selection page
│   ├── key_theme_selection.html
│   ├── core_arc_selection.html
│   ├── genre_selection.html
│   ├── subgenre_selection.html
│   ├── writing_style_selection.html
│   ├── protagonist_archetype_selection.html
│   ├── secondary_archetype_selection.html
│   ├── story_completion.html
│   └── expanded_story.html # Character generation results and expanded plot display
├── static/                  # CSS, JavaScript, images
│   └── style.css           # Main stylesheet (black theme, UI disable states, left panel scrolling)
└── tests/                   # Test suite
    ├── test_story_types.py
    ├── test_emotional_function.py
    ├── test_comprehensive.py
    ├── test_flask_save_load.py
    ├── test_functional_role.py
    ├── test_narrative_function.py  # Narrative function tests
    ├── test_chapter_summary.py     # Chapter continuity and summary functionality tests
    ├── test_prompt_debugging.py  # AI debugging functionality tests
    └── [other test files]
```

## Component Architecture

### Core Components

#### 1. Flask Application (`app.py`)
**Purpose**: Web interface, routing, session management, request handling
**Key Features**:
- Route definitions following RESTful patterns
- Session-based state persistence
- Template rendering with context data
- Form processing and validation
- File upload/download for save/load functionality
- Asynchronous plot line generation with UI state management
- AI integration with prompt type categorization for debugging
- **Imports**: Uses `from objects.*` imports to access story models and registries

**Key Functions**:
- `get_story_from_session()` - Reconstruct Story object from session data
- `save_story_to_session()` - Persist Story object to session
- `get_next_incomplete_step()` - Determine the next incomplete step in story creation process for smart post-load navigation. Logic checks in order: story type → subtype → key theme → core arc → genre → sub-genre → writing style → protagonist archetype → plot line selection → character generation → **chapter plan (if chapters exist)** → complete story
- Route handlers for each step in the user flow including individual chapter generation
- `/generate-chapter/<int:chapter_number>` POST route for individual chapter generation with chapter_text
- Navigation handler for edit button functionality

#### 2. Story Model (`objects/story.py`)
**Purpose**: Central business object managing user selections and data validation
**Key Features**:
- Tracks all user selections (story type, genre, archetypes using ArchetypeEnum, etc.)
- Maintains separate archetype fields (`protagonist_archetype: Optional[ArchetypeEnum]`, `secondary_archetypes: List[ArchetypeEnum]`) and Character system (`characters`)
- Includes chapter structure functionality (`chapters: List[Chapter]`) for detailed story planning
- Includes expanded plot line functionality (`expanded_plot_line: Optional[str]`) for AI-generated enhanced narratives
- Validates data consistency across selections including archetype enum validation
- Provides business logic for typical vs other archetype classification
- Generates structured prompt text for AI writing assistants **including plot line information when available**
- Provides specialized prompt text generation for chapter outlines that excludes specific fields (protagonist_archetype, secondary_archetypes, selected_plot_line)
- Provides specialized prompt text generation for individual chapters that excludes archetype/plot fields and filters chapters to n-1
- JSON serialization/deserialization for persistence with automatic enum to string conversion
- **Imports**: Uses relative imports (`.`) to access other objects within the package

**Key Methods**:
- `set_*()` methods with validation and dependency management including archetype enum conversion
- `get_available_*()` methods for filtered selection options
- Chapter management methods (`add_chapter()`, `remove_chapter()`, `get_chapter()`, `update_chapter()`)
- `to_prompt_text()` - Generate structured output for external use, including suggested secondary character archetypes when none are explicitly selected **and plot line details when a plot line is selected** **and chapter structure when chapters are defined**
- `to_prompt_text_for_chapter_outline()` - Generate filtered story configuration for chapter outline prompts
- `to_prompt_text_for_chapter(n: int)` - Generate filtered story configuration for individual chapter generation with previous chapters only

- `to_json()` / `from_json()` - Persistence functionality with automatic enum to string conversion and string to enum parsing

#### 3. Prompt Generation (`prompt.py`)
**Purpose**: Generates specialized LLM prompts by combining template files with story configuration
**Key Features**:
- **Plot Prompt Generation**: `generate_plot_prompt()` function for creating plot line generation prompts
- **Character Prompt Generation**: `generate_character_prompt()` function for creating character development prompts
- **Chapter Outline Prompt Generation**: `generate_chapter_outline_prompt()` function for creating chapter outline prompts with modified story configuration
- **Chapter Prompt Generation**: `generate_chapter_prompt(story: Story, n: int)` function for creating individual chapter prompts with filtered story configuration and previous chapters only
- Template file integration from `prompts/` directory for all prompt types
- Character generation based on selected plot line and complete story configuration
- Chapter outline generation with excluded fields (protagonist_archetype, secondary_archetypes, selected_plot_line)
- Chapter generation with filtered chapters (only 1 to n-1) and excluded archetype/plot fields
- Structured JSON response parsing for expanded plot lines and character data
- Consistent prompt structure combining pre-text, story configuration, and post-text
- Whitespace handling and error resilience
- **Imports**: Uses `from objects.story import Story` to access story models

**Template Files**:
- `plot_lines_pre.txt` / `plot_lines_post.txt` - For plot generation prompts
- `characters_pre.txt` / `characters_post.txt` - For character development prompts
- `chapter_outline_pre.txt` / `chapter_outline_post.txt` - For chapter outline generation prompts
- `chapter_pre.txt` / `chapter_post.txt` - For individual chapter generation prompts

#### 4. Character Parser (`objects/character_parser.py`)
**Purpose**: Parses AI responses to extract characters and expanded plot lines
**Key Features**:
- **Character Data Extraction**: Parses structured JSON from AI responses
- **Expanded Plot Line Extraction**: Extracts enhanced plot narratives 
- **Character Object Creation**: Creates Character instances with complete archetype, role, and development data
- **Enum Conversion**: Converts string values to appropriate enum types (ArchetypeEnum, FunctionalRoleEnum, EmotionalFunctionEnum)
- **Error Handling**: Graceful handling of malformed AI responses
- **Imports**: Uses relative imports to access character and enum models

**Key Functions**:
- `parse_characters_from_ai_response()` - Main parsing function returning expanded plot line and character list
- `_create_character_from_dict()` - Character object creation with validation
- `_find_*_enum()` - Helper functions for enum string-to-value conversion

#### 5. Registry Components
**Purpose**: Centralized access to narrative data with consistent interfaces

**StoryTypeRegistry** (`story_types.py`):
- Manages 7 story types with 3 subtypes each
- Provides lookup by name with case-insensitive matching
- Includes rich metadata (descriptions, examples, emotional arcs, themes)

**ArchetypeRegistry** (`archetype.py`):
- Manages 108 character archetypes loaded from JSONL
- Provides search functionality across archetype names
- Supports both exact lookup and partial text search

**GenreRegistry** (`genre.py`):
- Manages hierarchical genre/sub-genre relationships
- Links sub-genres to typical character archetypes
- Supports genre-based filtering of story options

**StyleRegistry** (`style.py`):
- Manages 15 writing styles with characteristics and examples
- Provides search across style descriptions and characteristics
- Supports style-based guidance for writing approach

**EmotionalFunctionRegistry** (`emotional_function.py`):
- Manages 8 emotional functions that define character emotional roles
- Provides lookup and search functionality for emotional functions
- Supports emotional characterization in story development

**FunctionalRoleRegistry** (`functional_role.py`):
- Manages 20 functional roles defining narrative character functions
- Provides case-insensitive lookup with name normalization
- Supports search across role names and descriptions

**NarrativeFunctionRegistry** (`narrative_function.py`):
- Manages 23 narrative functions defining structural roles of scenes or chapters
- Provides case-insensitive lookup with name normalization
- Supports search across function names and descriptions

### Data Models

#### Story Type Hierarchy
```python
StoryType:
    - name: str
    - description: str  
    - examples: List[str]
    - narrative_rhythm: str
    - emotional_arc: List[str]
    - key_themes: List[str]
    - core_arcs: List[str]
    - subtypes: List[SubType]

SubType:
    - name: str
    - description: str
    - examples: List[str]
```

#### Character Archetype Model
```python
ArchetypeEnum:
    - CHOSEN_ONE = "Chosen One"
    - WISE_MENTOR = "Wise Mentor"
    - ... (108 total archetypes)

Archetype:
    - name: str          # e.g., "Chosen One"
    - description: str   # Detailed character description
```

#### Character Model
```python
Character:
    - name: str                         # Character's name
    - archetype: ArchetypeEnum          # Character's archetypal role
    - functional_role: FunctionalRoleEnum  # Character's narrative function
    - emotional_function: EmotionalFunctionEnum  # Character's emotional purpose
    - backstory: str                    # Character's background
    - character_arc: str                # Character's development arc
```

#### Chapter Model
```python
Chapter:
    - chapter_number: int               # Sequential chapter number
    - title: str                        # Short chapter title
    - overview: str                     # Brief summary of chapter events
    - character_impact: List[Dict[str, str]]  # Character impact entries
    - point_of_view: Optional[str]      # POV character name
    - narrative_function: Optional[NarrativeFunctionEnum]  # Narrative function tag
    - foreshadow_or_echo: Optional[str] # Setup or payoff description
    - scene_highlights: Optional[str]   # Notable imagery, dialogue, emotion, tension
    - summary: Optional[str]            # Recap of what happened in the chapter
    - continuity_state: ContinuityState # Detailed state tracking for story elements
    - chapter_text: Optional[str]       # Full prose text of the chapter (~1000 words)
```

#### Continuity Tracking Models
```python
# Note: Each class below is implemented in its own file within the objects/ directory

ContinuityState:
    - characters: List[ContinuityCharacter]  # Character states and positions
    - objects: List[ContinuityObject]        # Object locations and ownership
    - locations_visited: List[str]           # Places that have been visited
    - open_plot_threads: List[PlotThread]    # Active story threads

ContinuityCharacter:
    - name: str                         # Character's name
    - current_location: str             # Where the character currently is
    - status: str                       # Character's current emotional/physical state
    - inventory: List[str]              # Items the character possesses

ContinuityObject:
    - name: str                         # Object's name
    - holder: Optional[str]             # Who currently possesses the object
    - location: str                     # Where the object is located

PlotThread:
    - id: str                           # Unique identifier for the plot thread
    - description: str                  # Description of the ongoing plot element
    - status: str                       # Current status (e.g., "pending", "in progress")
```

#### Genre Hierarchy
```python
Genre:
    - name: str                    # e.g., "Fantasy"
    - subgenres: List[SubGenre]    # Associated sub-genres

SubGenre:
    - name: str              # e.g., "High Fantasy"
    - plot: str             # Plot type description
    - examples: List[str]   # Example works
    - archetypes: List[str] # Typical character archetypes
```

#### Writing Style Model
```python
Style:
    - name: str                    # e.g., "Concise"
    - description: str             # Style overview
    - characteristics: List[str]   # Specific traits
    - examples: List[str]         # Example authors/works
```

#### Prompt Type Model
```python
PromptType(Enum):
    - PLOT_LINES = "plot_lines"
    - CHARACTERS = "characters"
    - CHAPTER_OUTLINE = "chapter_outline"
    - CHAPTER = "chapter"
```

#### Emotional Function Model
```python
EmotionalFunctionEnum:
    - SYMPATHETIC_CHARACTER = "Sympathetic Character"
    - UNSYMPATHETIC_CHARACTER = "Unsympathetic Character"
    - CATALYST = "Catalyst"
    - OBSERVER = "Observer"
    - INSTIGATOR = "Instigator"
    - VICTIM = "Victim"
    - AGGRESSOR = "Aggressor"
    - MEDIATOR = "Mediator"

EmotionalFunction:
    - name: str          # e.g., "Catalyst"
    - description: str   # Emotional role description
```

#### Functional Role Model
```python
FunctionalRoleEnum:
    - PROTAGONIST = "Protagonist"
    - ANTAGONIST = "Antagonist"
    - MENTOR = "Mentor"
    - ... (20 total functional roles)

FunctionalRole:
    - name: str          # e.g., "Protagonist"
    - description: str   # Detailed role description
```

#### Narrative Function Model
```python
NarrativeFunctionEnum:
    - SETTING_INTRODUCTION = "Setting Introduction"
    - CHARACTER_INTRODUCTION = "Character Introduction"
    - INCITING_INCIDENT = "Inciting Incident"
    - CLIMAX = "Climax"
    - DENOUEMENT = "Denouement"
    - ... (23 total narrative functions)

NarrativeFunction:
    - name: str          # e.g., "Setting Introduction"
    - description: str   # Detailed function description
```

## Data Flow Architecture

### Request/Response Flow
1. **User Request** → Flask route handler
2. **Session Retrieval** → `get_story_from_session()`
3. **Data Preparation** → Registry lookups for template context
4. **Template Rendering** → Jinja2 with story state and options
5. **Form Submission** → POST handler with validation
6. **State Update** → Story object modification + session save
7. **Redirect** → Next step in user flow

### State Management Flow
```
User Input → Form Validation → Story Object Update → Session Persistence → Database Queries → Template Context → UI Update
```

### Navigation Flow
```
Edit Button Click → Clear Dependent Selections → Update Story State → Route to Selection Page → Display Current Options
```

## Design Patterns

### Registry Pattern
All narrative data uses centralized registries:
- Consistent lookup interfaces across data types
- Case-insensitive name-based access
- Search functionality where appropriate
- Immutable data after initialization

### Template Inheritance Pattern
```
base.html (layout + session state)
    ├── story_types.html (step-specific content)
    ├── genre_selection.html (step-specific content)
    └── [other step templates]
```

### Session State Pattern
- Story object serialized to session dictionary
- Automatic reconstruction on each request
- Smart clearing logic for dependent selections
- Persistence across browser sessions

### Form Processing Pattern
All step forms follow consistent pattern:
1. GET: Display selection options with current state
2. POST: Validate input, update story state, redirect to next step
3. Navigation: Handle edit requests with state clearing

## Integration Points

### External Data Sources
- **JSON/JSONL Files**: Narrative data loaded at application startup
- **File System**: Save/load functionality for story configurations
- **Session Storage**: Flask session for temporary state persistence
- **Azure OpenAI**: AI service integration for plot generation with debugging
- **Debug Files**: Local file system storage for AI prompt/response debugging

### Template Integration
- **Jinja2 Filters**: Custom filters for data formatting (e.g., arrow_format)
- **Context Processors**: Automatic story state injection into templates
- **Static Assets**: CSS and JavaScript for UI interactions
- **UI State Management**: JavaScript-based content replacement for intermediate states during async operations

### AI Integration and Debugging
- **Prompt Categorization**: `PromptType` enum for categorizing different AI prompts (PLOT_LINES, CHARACTERS)
- **Debug File Management**: Automatic saving of prompts and responses to categorized files
- **Error Handling**: Graceful handling of AI service failures with debug logging
- **File Organization**: Debug files named by prompt type for easy identification (plot_lines.txt, characters.txt)

### Testing Integration
- **Unit Tests**: Individual component validation
- **Integration Tests**: Full user flow testing
- **Flask Test Client**: Web request simulation
- **Fixture Data**: Consistent test data setup

## Extension Points

### Adding New Narrative Elements
1. Create new registry class following existing pattern
2. Add data loading from JSON/JSONL files
3. Integrate into Story object with validation
4. Create template for selection interface
5. Add route handlers for GET/POST processing

### Adding New UI Steps
1. Add new properties to Story model
2. Create template extending base.html
3. Add route handlers in app.py
4. Update navigation logic for edit functionality
5. Update session serialization/deserialization

### Adding New Data Sources
1. Implement registry interface
2. Add data loading logic
3. Update Story object dependencies
4. Ensure consistent validation patterns

## Performance Considerations

### Data Loading Strategy
- All registries loaded once at application startup
- Immutable data structures prevent thread safety issues
- In-memory lookups for fast access during requests

### Session Management
- Minimal session data (selections only, not full objects)
- Lazy object reconstruction from registries
- Session cleanup on fresh application visits

### Template Rendering
- Consistent context preparation across routes
- Minimal template logic (business logic in models)
- Static asset caching for improved performance

## Development Workflow

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `python3 launch.py` or `python3 app.py`
3. Access at `http://localhost:5000` or `http://localhost:5001`
4. Run tests: `python3 -m pytest tests/`

### Testing Strategy
- **Unit Tests**: Individual registry and model functionality
- **Integration Tests**: Full user workflow simulation
- **Flask Tests**: Route handler and session management testing
- **Data Validation Tests**: Ensure data consistency and completeness

### Code Organization Principles
- **Separation of Concerns**: Clear boundaries between data, business logic, and presentation
- **Consistent Patterns**: Registry pattern, template inheritance, route naming
- **Validation Centralization**: Business rules enforced in model layer
- **Error Handling**: Graceful degradation with user feedback