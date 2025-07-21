The user will step through the following interfaces:

1) Select story type
2) Select story sub-type  
3) Select key theme (auto-proceeds to next step)
4) Select core arc (auto-proceeds to next step)
5) Select genre (auto-proceeds to next step)
6) Select sub-genre (auto-proceeds to completion)

## User Experience Flow

The UI provides a streamlined selection experience where users automatically proceed to the next step upon making their selection, eliminating the need for manual "continue" buttons.

### Navigation Behavior
- **Story Type & Subtype Selection**: Users click to navigate between these steps
- **Key Theme Selection**: Clicking a theme card immediately submits and proceeds to core arc selection
- **Core Arc Selection**: Clicking an arc card immediately submits and proceeds to genre selection  
- **Genre Selection**: Clicking a genre card immediately submits and proceeds to sub-genre selection
- **Sub-Genre Selection**: Clicking a sub-genre card immediately submits and completes the story

All selection steps (themes, arcs, genres, and sub-genres) use a consistent card-based UI with hover effects and visual selection states for optimal user experience.

### UI Cleanup
The following pages have been streamlined to show only essential elements:

- **Key Theme Selection**: Shows only the title, theme selection cards, and back button (removed story type description and section titles)
- **Core Arc Selection**: Shows only the title, arc selection cards, and back button (removed step description and "Your Story So Far" section)  
- **Genre Selection**: Shows only the title, genre selection cards, and back button (removed step description and "Your Story So Far" section). Genre cards now display actual sub-genre names instead of counts.

## UI Layout

The UI has a left and right panel

**Left Panel**: 
- Shows save and load buttons at the top
- Displays the choices that the user has made so far (choices are stored in the story class)
- Contains an expandable details panel inside the "Your Story Selections" section that shows:
  - Story type description, examples, emotional arc, key moments, and common elements
  - This details panel persists across all pages once a story type is selected

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