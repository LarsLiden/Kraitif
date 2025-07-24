# Kraitif Architectural Specification

## Overview

Kraitif is built as a Flask web application using a modular, registry-based architecture. The system separates narrative data management, user interface concerns, and business logic into distinct layers for maintainability and extensibility.

## File Structure and Organization

```
Kraitif/
├── app.py                    # Main Flask application and routing
├── story.py                  # Core Story model and business logic
├── story_types.py           # Story type definitions and registry
├── archetype.py             # Character archetype registry, models, and ArchetypeEnum
├── emotional_function.py    # Emotional function registry, models, and EmotionalFunctionEnum
├── functional_role.py       # Functional role registry, models, and FunctionalRoleEnum
├── character.py             # Character class combining archetype, functional role, emotional function
├── genre.py                 # Genre/sub-genre registry and models  
├── style.py                 # Writing style registry and models
├── prompt.py                  # Prompt generation functions (plot and character prompts)
├── prompt_types.py          # Prompt type enumeration for AI debugging
├── launch.py                # Simple application launcher
├── demo.py                  # Command-line demo script
├── requirements.txt         # Python dependencies
├── ai/                      # AI integration module
│   └── ai_client.py         # Azure OpenAI client with debugging support
├── data/                    # Narrative data files
│   ├── archetypes.jsonl     # Character archetype definitions
│   ├── emotional_functions.json # Emotional function definitions
│   ├── functional_roles.json # Functional role definitions
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
│   └── story_completion.html
├── static/                  # CSS, JavaScript, images
│   └── style.css           # Main stylesheet (black theme, UI disable states)
└── tests/                   # Test suite
    ├── test_story_types.py
    ├── test_emotional_function.py
    ├── test_comprehensive.py
    ├── test_flask_save_load.py
    ├── test_functional_role.py
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

**Key Functions**:
- `get_story_from_session()` - Reconstruct Story object from session data
- `save_story_to_session()` - Persist Story object to session
- Route handlers for each step in the user flow
- Navigation handler for edit button functionality

#### 2. Story Model (`story.py`)
**Purpose**: Central business object managing user selections and data validation
**Key Features**:
- Tracks all user selections (story type, genre, archetypes using ArchetypeEnum, etc.)
- Maintains separate archetype fields (`protagonist_archetype: Optional[ArchetypeEnum]`, `secondary_archetypes: List[ArchetypeEnum]`) and Character system (`characters`)
- Validates data consistency across selections including archetype enum validation
- Provides business logic for typical vs other archetype classification
- Generates structured prompt text for AI writing assistants **including plot line information when available**
- JSON serialization/deserialization for persistence with automatic enum to string conversion

**Key Methods**:
- `set_*()` methods with validation and dependency management including archetype enum conversion
- `get_available_*()` methods for filtered selection options
- `to_prompt_text()` - Generate structured output for external use, including suggested secondary character archetypes when none are explicitly selected **and plot line details when a plot line is selected**
- `to_json()` / `from_json()` - Persistence functionality with automatic enum to string conversion and string to enum parsing

#### 3. Prompt Generation (`prompt.py`)
**Purpose**: Generates specialized LLM prompts by combining template files with story configuration
**Key Features**:
- **Plot Prompt Generation**: `generate_plot_prompt()` function for creating plot line generation prompts
- **Character Prompt Generation**: `generate_character_prompt()` function for creating character development prompts  
- Template file integration from `prompts/` directory
- Consistent prompt structure combining pre-text, story configuration, and post-text
- Whitespace handling and error resilience

**Template Files**:
- `plot_lines_pre.txt` / `plot_lines_post.txt` - For plot generation prompts
- `characters_pre.txt` / `characters_post.txt` - For character development prompts

#### 4. Registry Components
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
    # Additional types can be added as needed
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
- **Prompt Categorization**: `PromptType` enum for categorizing different AI prompts
- **Debug File Management**: Automatic saving of prompts and responses to categorized files
- **Error Handling**: Graceful handling of AI service failures with debug logging
- **File Organization**: Debug files named by prompt type for easy identification

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