# Kraitif Design Specification

## Application Purpose and Domain

Kraitif is a narrative theory application that helps writers systematically create story configurations based on established literary principles. The application implements Christopher Booker's seven basic plot types from narrative theory, combined with character archetypes, writing styles, and genre classifications to provide comprehensive story guidance.

**Core Domain**: Narrative theory and story structure analysis  
**Target Users**: Writers, storytellers, content creators, and narrative designers  
**Primary Goal**: Generate detailed story configurations that can guide creative writing processes

## Narrative Theory Foundation

The application is built on these literary concepts:

### Seven Classical Story Types
Each story type represents a fundamental narrative pattern with specific emotional arcs, key moments, and thematic elements:

1. **Overcoming the Monster** - Hero faces a great evil or threat
2. **Rags to Riches** - Protagonist rises from humble beginnings to greatness  
3. **The Quest** - A journey with companions, trials, and a goal
4. **Voyage and Return** - Hero enters a strange world and returns transformed
5. **Comedy** - Confusion and miscommunication resolved in harmony
6. **Tragedy** - A fatal flaw leads to downfall
7. **Rebirth** - Hero is redeemed or transformed

Each story type contains 3 subtypes (21 total), narrative rhythm patterns, emotional arcs, key themes, and common structural elements.

### Character Archetypes
108 character archetypes representing universal character patterns found across literature and media. Each archetype includes a name and descriptive explanation of the character's role and motivations.

### Writing Styles  
15 fundamental writing styles (Concise, Lyrical, Analytical, Whimsical, etc.) with characteristics, examples, and application guidance.

### Genres and Sub-genres
Comprehensive genre system covering Fantasy, Science Fiction, Mystery, Horror, Romance, and others, each with multiple sub-genres that contain typical archetype associations.

## Data Model Relationships

### Core Entity: Story Object
The `Story` class serves as the central data container tracking user selections:

```python
class Story:
    # Story Type selections
    story_type_name: Optional[str]      # e.g., "The Quest"
    subtype_name: Optional[str]         # e.g., "Spiritual Quest"  
    key_theme: Optional[str]            # User-selected theme
    core_arc: Optional[str]             # User-selected arc
    
    # Genre selections
    genre: Optional[Genre]              # Genre object with sub-genres
    sub_genre: Optional[SubGenre]       # Contains archetype associations
    
    # Style and Character selections
    writing_style: Optional[Style]      # Writing style object
    protagonist_archetype: Optional[str] # Single protagonist choice
    secondary_archetypes: List[str]     # Multiple secondary characters
```

### Registry Pattern
All narrative elements use a registry pattern for centralized access:
- `StoryTypeRegistry` - Manages story types and subtypes
- `ArchetypeRegistry` - Manages character archetypes  
- `GenreRegistry` - Manages genres and sub-genres
- `StyleRegistry` - Manages writing styles

### Data Flow Dependencies
1. **Genre → Sub-genre**: Sub-genres belong to specific genres
2. **Sub-genre → Archetypes**: Each sub-genre has typical archetype associations
3. **Story Type → Themes/Arcs**: Each story type defines available themes and arcs
4. **All selections → Prompt Generation**: Complete story configuration generates structured text output

## User Experience Flow

The user will step through the following interfaces:

1) Select story type
2) Select story sub-type  
3) Select key theme (auto-proceeds to next step)
4) Select core arc (auto-proceeds to next step)
5) Select genre (auto-proceeds to next step)
6) Select sub-genre (auto-proceeds to next step)
7) Select writing style (manual proceed to next step)
8) Select protagonist archetype (manual proceed to secondary characters)
9) Select secondary character archetypes (manual proceed to completion)

## User Experience Flow

The UI provides a streamlined selection experience where users automatically proceed to the next step upon making their selection, eliminating the need for manual "continue" buttons.

## Business Rules and Logic

### Auto-progression Rules
- **Theme/Arc/Genre Selections**: Automatically proceed to next step upon selection (no manual "continue" button)
- **Style/Archetype Selections**: Require manual progression to allow multiple selections or careful consideration

### Data Validation Rules
- **Sub-genre Dependency**: Sub-genre must belong to selected genre; changing genre clears sub-genre
- **Archetype Validation**: All selected archetypes must exist in the registry
- **Story Type Consistency**: Key themes and core arcs must be available for the selected story type

### Selection Clearing Logic
When navigating back to edit a previous step:
- Clear the edited step AND all subsequent steps
- Preserve all steps before the edited step
- Redirect user to appropriate selection page

### Archetype Organization Rules
- **Typical vs Other**: Sub-genres define "typical" archetypes; all others are "other"
- **Protagonist Constraint**: Exactly one protagonist required; cannot be changed in secondary selection
- **Secondary Optional**: Secondary character selection is completely optional

## User Interface Patterns

### Two-Panel Layout Architecture
**Left Panel**: 
- Save and load controls at top
- "Your Story Selections" section showing completed choices
- Each selection includes edit button (✏️) for navigation back to that step
- Expandable details panels for story type and subtype with rich information
- All edit buttons implement smart clearing logic

**Right Panel**: 
- Current step content and selection options
- Progress flows from top to bottom through the selection process
- Card-based selection UI with hover effects and visual feedback

### Navigation System Principles
- **No Breadcrumb Navigation**: Eliminated in favor of left panel edit buttons
- **Icon-Based Edit Controls**: Clean ✏️ pencil icons rather than text buttons
- **Smart State Management**: Edit buttons clear dependent selections automatically
- **Progressive Disclosure**: Show only current step content in right panel

### UI Component Patterns
- **Selection Cards**: Consistent card-based interface for themes, arcs, genres, sub-genres
- **Radio Button Groups**: Single-selection elements (genre, sub-genre, protagonist)
- **Checkbox Groups**: Multi-selection elements (secondary characters)
- **Expandable Panels**: Rich information display for story type and subtype details
- **Auto-submit Forms**: Theme, arc, and genre selections automatically submit on click

### Visual Design Principles
- **Black Background Theme**: Dark theme for comfortable extended use
- **Responsive Design**: Works on mobile and desktop
- **Hover Effects**: Interactive feedback on all selectable elements  
- **Progressive Enhancement**: Core functionality works without JavaScript

## Data Persistence and State Management

### Session State
Flask sessions maintain story state during user interaction:
- All selections stored in `session['story_data']` dictionary
- Session persists across page navigation and refreshes
- Session cleared on fresh visits from external sources

### Save/Load Functionality
- **Save**: Exports complete story configuration as JSON file download
- **Load**: Imports JSON file, validates data, updates session, redirects to appropriate step
- **Validation**: Ensures all loaded data references exist in current registries

### Story Completion Output
Generate structured prompt text containing:
- Story type and subtype details with examples
- Selected themes and arcs  
- Genre and sub-genre information
- Writing style with characteristics and examples
- Character archetypes with detailed descriptions:
  - Selected protagonist archetype
  - Selected secondary character archetypes (if any)
  - Suggested secondary character archetypes typical for the genre (when no secondary characters are explicitly selected)
- Formatted for use with AI writing assistants

## Technical Integration Points

### Flask Route Structure
- RESTful route naming following `/noun-verb` pattern
- GET routes display selection forms
- POST routes process form submissions and redirect
- Navigation routes handle edit button functionality
- Utility routes handle save/load operations

### Template Inheritance
- `base.html` provides core two-panel layout and session-aware left panel
- Individual step templates extend base and focus on right panel content
- Consistent data passing includes story object and all registry objects

### Error Handling Patterns
- Flash messages for user feedback on validation errors
- Graceful fallbacks for missing data or invalid selections
- Redirect chains ensure users cannot access steps without prerequisites

### Data Loading Strategy
- Registries load from JSON/JSONL files in `/data` directory at startup
- Immutable data structures for thread safety
- Case-insensitive lookups with exact name matching

### Navigation System

The application uses a **left panel navigation system** with edit buttons instead of traditional breadcrumb navigation:

- **No Breadcrumb Navigation**: All breadcrumb trails (e.g., "Story Types > Rags to Riches > Pure Ascent > Key Theme Selection") have been removed from all pages
- **Left Panel Edit Buttons**: Each completed selection in the "Your Story Selections" panel includes an edit button (✏️ icon) that allows users to return to that selection step
- **Smart Clearing Logic**: When a user clicks an edit button to return to a previous step:
  - That selection and all subsequent selections are cleared from the story object
  - The user is redirected to the appropriate selection page for that step
  - All selections made before that step are preserved
- **Icon-Based Design**: Edit buttons use a clean pencil emoji (✏️) for an aesthetic, icon-based approach rather than text buttons
- **Hover Effects**: Edit buttons include hover effects and tooltips for better user experience

This navigation system provides a more intuitive way for users to modify their story selections without losing progress on earlier decisions, while maintaining a clean interface without cluttered breadcrumb navigation.

### UI Cleanup
The following pages have been streamlined to show only essential elements:

- **Key Theme Selection**: Shows only the title, theme selection cards, and back button (removed story type description and section titles)
- **Core Arc Selection**: Shows only the title, arc selection cards, and back button (removed step description and "Your Story So Far" section)  
- **Genre Selection**: Shows only the title, genre selection cards, and back button (removed step description and "Your Story So Far" section). Genre cards now display actual sub-genre names instead of counts.
- **Sub-Genre Selection**: Shows only the title, sub-genre selection cards, and back button (removed step indicator and "Your Story So Far" section)

## UI Layout

The UI has a left and right panel

**Left Panel**: 
- Shows save and load buttons at the top
- Displays the choices that the user has made so far (choices are stored in the story class)

- Contains separate expandable details panels inside the "Your Story Selections" section:
  - **Story Type Panel**: Shows story type name with expandable details including description, examples, emotional arc, key moments, and common elements. Includes edit button to return to story type selection.
  - **Story Sub-Type Panel**: Shows story sub-type name with expandable details specific to the sub-type including description and examples. Includes edit button to return to subtype selection.
  - **Selection Items**: Key Theme, Core Arc, Genre, Sub-Genre, Writing Style, Protagonist, and Secondary Characters all display with edit buttons that allow navigation back to their respective selection pages.
  - Both expandable panels persist across all pages once selections are made and can be expanded/collapsed independently
- All edit buttons use icon-based design (✏️) and implement smart clearing logic when clicked

**Right Panel**: 
- Shows the options that the user can choose from
- Displays current step content and selections

## Save/Load Functionality

At the top of the left panel is a load and save button:
- **Save button**: Saves the story object to disk in JSON format
- **Load button**: 
    - Loads the JSON and converts it to the story object
    - Updates the UI to show the current state of the story  
    - If the story is incomplete, user is taken to selection page for step with next missing information

## Archetype Selection

The archetype selection has been separated into two distinct steps to differentiate between protagonist and secondary characters:

### Protagonist Archetype Selection (Step 7)
- **Single Selection**: Users select one archetype for the story protagonist using radio buttons
- **Two-Section Layout**: 
  - **Typical Protagonist Archetypes**: Shows archetypes commonly associated with the selected sub-genre
  - **Other Available Protagonist Archetypes**: Shows all remaining archetypes with descriptions
- **Navigation**: "Continue to Secondary Characters" button proceeds to the next step

### Secondary Character Archetype Selection (Step 8)
- **Optional Multiple Selection**: Users can select multiple archetypes for secondary characters using checkboxes
- **Clearly Marked as Optional**: Both the heading and description indicate that secondary character selection is optional
- **Disabled Protagonist**: The previously selected protagonist archetype is displayed but disabled (greyed out text, not selectable) with "(Protagonist)" label to show context
- **Two-Section Layout**:
  - **Typical Secondary Character Archetypes**: Shows all typical archetypes for the sub-genre, with protagonist disabled
  - **Other Available Secondary Character Archetypes**: Shows all other archetypes, with protagonist disabled if present
- **Complete Button at Top**: "Complete Story Selection" button is positioned above the fold for easy access
- **Navigation**: Users can go back to protagonist selection or complete the story

### Left Panel Display
The selected archetypes are displayed as separate sections in the left panel:
- **Protagonist**: Shows the single selected protagonist archetype with edit button
- **Secondary Characters**: Shows comma-separated list of selected secondary archetypes with edit button (only appears if any are selected)