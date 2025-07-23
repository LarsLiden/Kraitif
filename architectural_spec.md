# Kraitif Architectural Specification

## Overview

Kraitif is built as a Flask web application using a modular, registry-based architecture. The system separates narrative data management, user interface concerns, and business logic into distinct layers for maintainability and extensibility.

## File Structure and Organization

```
Kraitif/
├── app.py                    # Main Flask application and routing
├── story.py                  # Core Story model and business logic
├── story_types.py           # Story type definitions and registry
├── archetype.py             # Character archetype registry and models
├── emotional_function.py    # Emotional function registry and models
├── functional_role.py       # Functional role registry and models
├── genre.py                 # Genre/sub-genre registry and models  
├── style.py                 # Writing style registry and models
├── launch.py                # Simple application launcher
├── demo.py                  # Command-line demo script
├── requirements.txt         # Python dependencies
├── data/                    # Narrative data files
│   ├── archetypes.jsonl     # Character archetype definitions
│   ├── emotional_functions.json # Emotional function definitions
│   ├── functional_roles.json # Functional role definitions
│   └── [other data files]  # Genre, style data (JSON format)
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

**Key Functions**:
- `get_story_from_session()` - Reconstruct Story object from session data
- `save_story_to_session()` - Persist Story object to session
- Route handlers for each step in the user flow
- Navigation handler for edit button functionality

#### 2. Story Model (`story.py`)
**Purpose**: Central business object managing user selections and data validation
**Key Features**:
- Tracks all user selections (story type, genre, archetypes, etc.)
- Validates data consistency across selections
- Provides business logic for typical vs other archetype classification
- Generates structured prompt text for AI writing assistants
- JSON serialization/deserialization for persistence

**Key Methods**:
- `set_*()` methods with validation and dependency management
- `get_available_*()` methods for filtered selection options
- `to_prompt_text()` - Generate structured output for external use, including suggested secondary character archetypes when none are explicitly selected
- `to_json()` / `from_json()` - Persistence functionality

#### 3. Registry Components
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
Archetype:
    - name: str          # e.g., "Chosen One"
    - description: str   # Detailed character description
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

#### Emotional Function Model
EmotionalFunction:
    - name: str          # e.g., "Catalyst"
    - description: str   # Emotional role description

#### Functional Role Model
FunctionalRole:
    - name: str          # e.g., "Protagonist"
    - description: str   # Detailed role description

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

### Template Integration
- **Jinja2 Filters**: Custom filters for data formatting (e.g., arrow_format)
- **Context Processors**: Automatic story state injection into templates
- **Static Assets**: CSS and JavaScript for UI interactions
- **UI State Management**: JavaScript-based enabling/disabling of interface elements during async operations

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