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

### Character Archetypes and Character System
The application uses a comprehensive character system built around:

#### Character Archetypes
108 character archetypes representing universal character patterns found across literature and media. Each archetype includes a name and descriptive explanation of the character's role and motivations. These are defined as an `ArchetypeEnum` for type safety.

#### Character Objects
The `Character` class represents a complete character with:
- **name** (str): The character's name
- **archetype** (ArchetypeEnum): The character's archetypal role
- **functional_role** (FunctionalRoleEnum): The character's narrative function
- **emotional_function** (EmotionalFunctionEnum): The character's emotional purpose
- **backstory** (str): The character's background story
- **character_arc** (str): The character's development throughout the story

#### Functional Roles
20 fundamental functional roles that define how characters function within a narrative structure (Protagonist, Antagonist, Mentor, etc.). Each functional role includes a name and description of the character's narrative purpose and relationship to the plot and other characters. These are defined as a `FunctionalRoleEnum`.

#### Emotional Functions
8 emotional functions that define the emotional role a character serves in the story:
- **Sympathetic Character**: Evokes empathy; often deeply vulnerable
- **Unsympathetic Character**: Hard to like but may still compel or challenge the protagonist
- **Catalyst**: Pushes others to change without changing much themselves
- **Observer**: Exists at the margins, often revealing truths unnoticed
- **Instigator**: Creates disruptions that force growth or conflict
- **Victim**: Suffers due to external forces, evoking sorrow or motivation
- **Aggressor**: Causes harm, either directly or through manipulation
- **Mediator**: Resolves conflicts between other characters

Each emotional function includes a name and descriptive explanation of the emotional role the character serves. These are defined as an `EmotionalFunctionEnum`.

#### Narrative Functions
23 narrative functions that define the structural roles of scenes or chapters within a story:
- **Setting Introduction**: Establishes location, mood, tone
- **Character Introduction**: Introduces key characters
- **Inciting Incident**: First major disruption to the status quo
- **First Reversal**: Unexpected shift in direction or stakes
- **Rising Tension**: Builds suspense, stakes, and pressure
- **Subplot Activation**: Launches secondary threads
- **Moral Challenge**: Characters face ethical or emotional conflict
- **Midpoint Turn**: Major twist or truth changes the trajectory
- **Relationship Reversal**: Shift in character dynamics (betrayal, alliance)
- **Moment of Weakness**: Hero falters emotionally or physically
- **Setback**: External failure or complication
- **Truth Revelation**: Important secret or mystery unveiled
- **Confrontation**: Major clash between protagonist and antagonist
- **Climax**: Emotional or physical peak of tension
- **Transformation**: Character internal shift or rebirth
- **Denouement**: Loose ends resolved, consequences shown
- **Final Image**: Last scene or symbolic moment
- **Foreshadowing**: Seeds planted for future tension
- **Echo**: Payoff for earlier scene or dialogue
- **Reflection**: Characters contemplate past actions, change
- **Theme Reinforcement**: Underscores core message or motif
- **Catalyst Event**: Minor event with disproportionate future impact
- **Unexpected Reunion**: Characters reconnect in surprising ways

Each narrative function includes a name and descriptive explanation of the structural role it serves. These are defined as a `NarrativeFunctionEnum`.

### Chapter System
The application includes a comprehensive chapter structure system that allows writers to plan and organize their stories at the chapter level:

#### Chapter Objects
The `Chapter` class represents a complete chapter with:
- **chapter_number** (int): The sequential number of the chapter
- **title** (str): Short chapter title
- **overview** (str): Brief summary of what happens in this chapter
- **character_impact** (List[Dict[str, str]]): Array of character impact entries with character names and effect descriptions
- **point_of_view** (str, optional): Name of POV character for the chapter
- **narrative_function** (NarrativeFunctionEnum, optional): Narrative function tag that must match NarrativeFunctionEnum
- **foreshadow_or_echo** (str, optional): Description of setup or payoff elements
- **scene_highlights** (str, optional): Notable imagery, dialogue, emotion, or tension

Each chapter provides methods for managing character impact entries, setting narrative functions, and serialization support.

### Chapter Summary System
The application includes a comprehensive chapter summary system that tracks story continuity and state:

#### Chapter Summary Objects
The `ChapterSummary` class represents a complete chapter summary with:
- **summary** (str): Recap of what happened in the chapter
- **continuity_state** (ContinuityState): Detailed state tracking for story elements

#### Continuity State Components
The `ContinuityState` class tracks the ongoing state of story elements:
- **characters** (List[ContinuityCharacter]): Character states and positions
- **objects** (List[ContinuityObject]): Object locations and ownership
- **locations_visited** (List[str]): Places that have been visited
- **open_plot_threads** (List[PlotThread]): Active story threads

#### Continuity Character Tracking
The `ContinuityCharacter` class tracks character state:
- **name** (str): Character's name
- **current_location** (str): Where the character currently is
- **status** (str): Character's current emotional/physical state
- **inventory** (List[str]): Items the character possesses

#### Continuity Object Tracking
The `ContinuityObject` class tracks important story objects:
- **name** (str): Object's name
- **holder** (Optional[str]): Who currently possesses the object
- **location** (str): Where the object is located

#### Plot Thread Tracking
The `PlotThread` class tracks ongoing story elements:
- **id** (str): Unique identifier for the plot thread
- **description** (str): Description of the ongoing plot element
- **status** (str): Current status (e.g., "pending", "in progress", "resolved")

The chapter summary system provides comprehensive JSON serialization/deserialization, validation, and management methods for maintaining story continuity across chapters.

### Writing Styles

15 fundamental writing styles (Concise, Lyrical, Analytical, Whimsical, etc.) with characteristics, examples, and application guidance.
### Genres and Sub-genres

Comprehensive genre system covering Fantasy, Science Fiction, Mystery, Horror, Romance, and others, each with multiple sub-genres that contain typical archetype associations.

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
    
    # Writing style selection
    writing_style: Optional[Style]      # Writing style object
    
    # Archetype selections - separate protagonist and secondary characters
    protagonist_archetype: Optional[ArchetypeEnum]  # e.g., "Chosen One"
    secondary_archetypes: List[ArchetypeEnum]       # e.g., ["Wise Mentor", "Loyal Companion"]
    
    # Character selections
    characters: List[Character]         # List of Character objects containing
                                       # archetype, functional_role, emotional_function,
                                       # backstory, and character_arc
    
    # Chapter structure
    chapters: List[Chapter]             # List of Chapter objects containing
                                       # chapter_number, title, overview, character_impact,
                                       # point_of_view, narrative_function, foreshadow_or_echo,
                                       # and scene_highlights
```

**Note**: The `protagonist_archetype` and `secondary_archetypes` fields are separate from and unrelated to the `characters` list. The archetype fields are used by the current web UI, while the `characters` list is for future UI implementation. The `chapters` list provides detailed chapter-level story structure planning.

### Registry Pattern
All narrative elements use a registry pattern for centralized access:
- `StoryTypeRegistry` - Manages story types and subtypes
- `ArchetypeRegistry` - Manages character archetypes with `ArchetypeEnum` support
- `GenreRegistry` - Manages genres and sub-genres
- `StyleRegistry` - Manages writing styles
- `EmotionalFunctionRegistry` - Manages emotional functions with `EmotionalFunctionEnum` support
- `FunctionalRoleRegistry` - Manages functional roles with `FunctionalRoleEnum` support
- `NarrativeFunctionRegistry` - Manages narrative functions with `NarrativeFunctionEnum` support

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

## Prompt Generation System

The application includes a comprehensive prompt generation system for AI integration:

### Plot Prompt Generation
- `generate_plot_prompt()` function combines plot-specific templates with story configuration
- Uses `plot_lines_pre.txt` and `plot_lines_post.txt` template files
- Includes complete story configuration for plot line generation

### Character Prompt Generation  
- `generate_character_prompt()` function combines character-specific templates with story configuration
- Uses `characters_pre.txt` and `characters_post.txt` template files
- Includes complete story configuration for character development prompts
- Template files contain detailed instructions for AI character creation including archetype, functional role, and emotional function specifications
- **Character Generation Flow**: Plot line selection → AI character generation → expanded plot line and character creation

### Chapter Outline Prompt Generation
- `generate_chapter_outline_prompt()` function combines chapter outline templates with modified story configuration
- Uses `chapter_outline_pre.txt` and `chapter_outline_post.txt` template files
- Uses `to_prompt_text_for_chapter_outline()` method which excludes specific fields from the story configuration:
  - Excludes `protagonist_archetype` field
  - Excludes `secondary_archetypes` field  
  - Excludes `selected_plot_line` field
- Includes `expanded_plot_line` when available
- Includes full Character objects when they exist
- Template files contain detailed instructions for AI chapter outline creation with structured metadata

### Character Generation System
The application includes a comprehensive character generation system that builds upon the selected plot line:

#### AI Character Generation Process
1. **Prerequisites**: User must have selected a plot line from AI-generated options
2. **Character Generation Trigger**: "Generate characters" button appears in left panel when plot line is selected
3. **AI Integration**: Uses `generate_character_prompt()` to create character-specific prompts based on story configuration and selected plot line
4. **Structured Response**: AI returns JSON containing expanded plot line and 5-8 character profiles
5. **Character Parsing**: `parse_characters_from_ai_response()` extracts character data and expanded plot line
6. **Character Objects**: Creates Character instances with complete archetype, role, and development information
7. **Story Integration**: Updates story object with expanded plot line and character data
8. **Results Display**: Shows expanded story page with detailed plot line and character profiles

#### Character Data Structure
Each AI-generated character includes:
- **Name**: Character's given name
- **Archetype**: Selected from ArchetypeEnum (108 available archetypes)
- **Functional Role**: Selected from FunctionalRoleEnum (20 narrative functions)
- **Emotional Function**: Selected from EmotionalFunctionEnum (8 emotional purposes)
- **Backstory**: Character's background and history
- **Character Arc**: Character's development and transformation throughout the story

#### Expanded Plot Line
- **Enhanced Narrative**: More detailed version of the selected plot line that incorporates all generated characters
- **Character Integration**: Plot expanded to show character roles, relationships, and interactions
- **Story Depth**: Provides comprehensive foundation for story writing with character-driven narrative

### Story Configuration Output
The `to_prompt_text()` method generates comprehensive story configuration that includes:
- Story type and subtype details with examples and emotional arcs
- Selected themes and core arcs
- Genre and sub-genre information with typical archetype associations
- Writing style characteristics and examples
- Character archetype details with descriptions
- **Plot line information when available** - includes selected plot line name and description
- **Character generation capabilities** - generates expanded plot lines and detailed character profiles
- **Expanded plot line integration** - enhanced story details that incorporate all generated characters
- Suggested secondary character archetypes for the genre when none are explicitly selected

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
- Each selection includes edit button (🗑️) for navigation back to that step
- Expandable details panels for story type and subtype with rich information
- All edit buttons implement smart clearing logic

**Right Panel**: 
- Current step content and selection options
- Progress flows from top to bottom through the selection process
- Card-based selection UI with hover effects and visual feedback

### UI Component Patterns
- **Selection Cards**: Consistent card-based interface for themes, arcs, genres, sub-genres
- **Radio Button Groups**: Single-selection elements (genre, sub-genre, protagonist)
- **Checkbox Groups**: Multi-selection elements (secondary characters)
- **Expandable Panels**: Rich information display for story type and subtype details
- **Auto-submit Forms**: Theme, arc, and genre selections automatically submit on click
- **Intermediate Page States**: Right panel content is replaced with intermediate "generating plot lines" or "generating characters" pages during AI processing, while preserving access to Save/Load/New buttons in the left panel
- **Character Generation Flow**: Generate characters button appears in left panel when plot line is selected, leading to character generation and expanded story display

### Visual Design Principles
- **Black Background Theme**: Dark theme for comfortable extended use
- **Responsive Design**: Works on mobile and desktop
- **Hover Effects**: Interactive feedback on all selectable elements  
- **Progressive Enhancement**: Core functionality works without JavaScript
- **Loading States**: Intermediate page replaces right panel content during asynchronous operations like plot line generation, providing visual feedback without disabling UI controls

### Page Title and Subtitle System
- **Consistent Title Structure**: All selection pages use consistent titles starting with "Select" (e.g., "Select Story Type", "Select a Genre")
- **Blue Subtitles**: Each page includes a blue subtitle using the `.page-subtitle` CSS class that provides context about available options
- **Dynamic Content**: Subtitles include dynamic content like story type or genre names (e.g., "Available Fantasy Sub-Genres", "Available Overcoming the Monster Themes")
- **Shared Styling**: The `.page-subtitle` class ensures consistent blue color (#64B5F6), typography, and spacing across all pages

## Data Persistence and State Management

### Session State
Flask sessions maintain story state during user interaction:
- All selections stored in `session['story_data']` dictionary with archetype fields as enum values converted to strings for session storage
- Session persists across page navigation and refreshes
- Session cleared on fresh visits from external sources

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
- **Plot line information when a plot line is selected** - includes plot line name and detailed description
- Formatted for use with AI writing assistants

### Prompt Generation Functions
The application provides three specialized prompt generation functions:
- **`generate_plot_prompt()`** - For plot line generation using plot-specific templates
- **`generate_character_prompt()`** - For character development using character-specific templates
- **`generate_chapter_outline_prompt()`** - For chapter outline generation using chapter outline templates and a modified story configuration that excludes protagonist_archetype, secondary_archetypes, and selected_plot_line fields
- Both functions combine pre/post template files with complete story configuration via `to_prompt_text()`

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

### AI Integration and Debugging
- AI prompts are categorized using `PromptType` enum for debugging purposes
- All AI interactions are logged to debug files in `/debug` folder
- Debug files are named using the prompt type (e.g., `plot_lines.txt`, `characters.txt`, `chapter_outline.txt`)
- Each debug file contains timestamp, prompt type, original prompt, and AI response
- Debug files are overwritten on each request to maintain only the latest interaction
- The `/debug` folder is excluded from version control

### Error Handling Patterns
- Flash messages for user feedback on validation errors
- Graceful fallbacks for missing data or invalid selections
- Redirect chains ensure users cannot access steps without prerequisites
- UI state restoration after failed asynchronous operations (e.g., plot line generation failures)
- Debug file creation errors are handled gracefully without breaking main application flow

### Data Loading Strategy
- Registries load from JSON/JSONL files in `/data` directory at startup
- Immutable data structures for thread safety
- Case-insensitive lookups with exact name matching

### Navigation System

The application uses a **left panel navigation system** with edit buttons instead of traditional breadcrumb navigation:

- **No Breadcrumb Navigation**: All breadcrumb trails (e.g., "Story Types > Rags to Riches > Pure Ascent > Key Theme Selection") have been completely removed from all pages. **Breadcrumb navigation must never be added to any page in this application.**
- **Left Panel Edit Buttons**: Each completed selection in the "Your Story Selections" panel includes an edit button (🗑️ icon) that allows users to return to that selection step
- **Smart Clearing Logic**: When a user clicks an edit button to return to a previous step:
  - That selection and all subsequent selections are cleared from the story object
  - The user is redirected to the appropriate selection page for that step
  - All selections made before that step are preserved
- **Icon-Based Design**: Edit buttons use a clean trash emoji (🗑️) for an aesthetic, icon-based approach rather than text buttons
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
- All edit buttons use icon-based design (🗑️) and implement smart clearing logic when clicked

**Right Panel**: 
- Shows the options that the user can choose from
- Displays current step content and selections

## Save/Load Functionality

At the top of the left panel is a load and save button:
- **Save button**: Saves the story object to disk in JSON format
- **Load button**: 
    - Loads the JSON and converts it to the story object
    - Updates the UI to show the current state of the story  
    - **Smart Landing**: Automatically determines the next incomplete step and redirects user to the appropriate selection page for continuing story development
    - Examples:
      - If genre is set but sub-genre isn't: redirects to sub-genre selection
      - If sub-genre is set but writing style isn't: redirects to writing style selection
      - If protagonist archetype is set but no plot line selected: redirects to secondary archetype selection (where plot lines can be generated)
      - If plot line is selected but no characters generated: redirects to plot line selected page (where characters can be generated)
      - If story is complete: redirects to story completion page

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