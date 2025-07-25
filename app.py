#!/usr/bin/env python3
"""
Flask web application for Story Types and SubTypes

This Flask app provides a web interface to explore the seven classical story types
and their subtypes.

IMPORTANT: When making changes to the project please makes sure to consults the following files that are designed to help AI coding agents:
- design_spec.md
- architectural_spec.md

Please also update the design_spec and architecture_spec documents to reflext any changes that would help an AI coding agent
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from objects.story_types import StoryTypeRegistry
from objects.story import Story
from objects.genre import GenreRegistry
from objects.archetype import ArchetypeRegistry
from objects.style import StyleRegistry
from prompt import Prompt
from objects.plot_line import PlotLine, parse_plot_lines_from_ai_response
from objects.character_parser import parse_characters_from_ai_response
from objects.chapter_parser import parse_chapters_from_ai_response, validate_chapter_character_names, parse_single_chapter_from_ai_response
from ai.ai_client import get_ai_response
from prompt_types import PromptType
import os
import uuid
import json
import tempfile
import atexit
import glob
import time

app = Flask(__name__)
app.secret_key = 'kraitif_story_selection_key'  # For session management

# Create a temporary directory for storing story data
STORY_DATA_DIR = tempfile.mkdtemp(prefix='kraitif_stories_')

# Clean up temporary files on exit
def cleanup_temp_files():
    """Clean up temporary story files on application exit."""
    import shutil
    if os.path.exists(STORY_DATA_DIR):
        shutil.rmtree(STORY_DATA_DIR, ignore_errors=True)

atexit.register(cleanup_temp_files)

# Initialize the story types registry
registry = StoryTypeRegistry()

# Initialize the genre registry
genre_registry = GenreRegistry()

# Initialize the archetype registry
archetype_registry = ArchetypeRegistry()

# Initialize the style registry
style_registry = StyleRegistry()

# Initialize the prompt generator
prompt_generator = Prompt()

# Custom Jinja2 filter for formatting emotional arc as arrows
@app.template_filter('arrow_format')
def arrow_format(arc_list):
    """Format a list as arrow-separated progression."""
    if not arc_list or not isinstance(arc_list, list):
        return ""
    return " → ".join(arc_list)


# Custom Jinja2 filter for converting newlines to HTML line breaks
@app.template_filter('nl2br')
def nl2br(text):
    """Convert newlines to HTML line breaks."""
    if not text:
        return ""
    from markupsafe import Markup
    return Markup(text.replace('\n', '<br>'))


def get_story_id():
    """Get or create a story ID for the current session."""
    if 'story_id' not in session:
        session['story_id'] = str(uuid.uuid4())
        session.modified = True
    return session['story_id']


def get_story_file_path(story_id):
    """Get the file path for a story ID."""
    return os.path.join(STORY_DATA_DIR, f"story_{story_id}.json")


def load_story_from_file(story_id):
    """Load story data from file."""
    file_path = get_story_file_path(story_id)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_story_to_file(story_id, story_data):
    """Save story data to file."""
    file_path = get_story_file_path(story_id)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def cleanup_old_story_files():
    """Clean up story files older than 24 hours."""
    try:
        cutoff_time = time.time() - (24 * 60 * 60)  # 24 hours ago
        for file_path in glob.glob(os.path.join(STORY_DATA_DIR, "story_*.json")):
            if os.path.getctime(file_path) < cutoff_time:
                os.remove(file_path)
    except Exception:
        pass  # Ignore cleanup errors


def get_story_from_session():
    """Get or create a Story object from session data."""
    story = Story()
    
    # Get story ID and load data from file
    story_id = get_story_id()
    story_data = load_story_from_file(story_id)
    
    # If no file data exists, try to get from session (backward compatibility)
    if not story_data:
        story_data = session.get('story_data', {})
    
    if story_data:
        story.story_type_name = story_data.get('story_type_name')
        story.subtype_name = story_data.get('subtype_name')
        story.key_theme = story_data.get('key_theme')
        story.core_arc = story_data.get('core_arc')
        # Load genre and sub-genre data
        genre_name = story_data.get('genre_name')
        if genre_name:
            story.set_genre(genre_name)
        sub_genre_name = story_data.get('sub_genre_name')
        if sub_genre_name:
            story.set_sub_genre(sub_genre_name)
        # Load writing style data
        writing_style_name = story_data.get('writing_style_name')
        if writing_style_name:
            story.set_writing_style(writing_style_name)
        # Load archetype selections
        protagonist_archetype = story_data.get('protagonist_archetype')
        if protagonist_archetype:
            story.set_protagonist_archetype(protagonist_archetype)
        secondary_archetypes = story_data.get('secondary_archetypes', [])
        if secondary_archetypes:
            story.set_secondary_archetypes(secondary_archetypes)
        
        # Load selected plot line
        selected_plot_line_data = story_data.get('selected_plot_line')
        if selected_plot_line_data and isinstance(selected_plot_line_data, dict):
            if 'name' in selected_plot_line_data and 'plotline' in selected_plot_line_data:
                plot_line = PlotLine(
                    name=selected_plot_line_data['name'],
                    plotline=selected_plot_line_data['plotline']
                )
                story.set_selected_plot_line(plot_line)
        
        # Load expanded plot line
        expanded_plot_line = story_data.get('expanded_plot_line')
        if expanded_plot_line:
            story.set_expanded_plot_line(expanded_plot_line)
        
        # Load characters
        characters_data = story_data.get('characters', [])
        from objects.character import Character
        for char_data in characters_data:
            character = Character.from_dict(char_data)
            if character:
                story.add_character(character)
        
        # Load chapters
        chapters_data = story_data.get('chapters', [])
        from objects.chapter import Chapter
        for chapter_data in chapters_data:
            chapter = Chapter.from_dict(chapter_data)
            if chapter:
                story.add_chapter(chapter)
        
        # Ensure session story_data is populated for template access
        if 'story_data' not in session:
            session['story_data'] = story_data
            session.modified = True
    
    return story


def get_protagonist_archetype_object(story):
    """Get the protagonist archetype object from the story."""
    if story.protagonist_archetype:
        return archetype_registry.get_archetype(story.protagonist_archetype.value)
    return None


def get_writing_style_object(story):
    """Get the writing style object from the story."""
    return story.writing_style


def get_secondary_archetype_objects(story):
    """Get the secondary archetype objects from the story."""
    if story.secondary_archetypes:
        secondary_objects = []
        for archetype_enum in story.secondary_archetypes:
            archetype = archetype_registry.get_archetype(archetype_enum.value)
            if archetype:
                secondary_objects.append(archetype)
        return secondary_objects
    return []


def save_story_to_session(story):
    """Save Story object to file-based storage."""
    story_id = get_story_id()
    story_data = {
        'story_type_name': story.story_type_name,
        'subtype_name': story.subtype_name,
        'key_theme': story.key_theme,
        'core_arc': story.core_arc,
        'genre_name': story.genre.name if story.genre else None,
        'sub_genre_name': story.sub_genre.name if story.sub_genre else None,
        'writing_style_name': story.writing_style.name if story.writing_style else None,
        'protagonist_archetype': story.protagonist_archetype.value if story.protagonist_archetype else None,
        'secondary_archetypes': [archetype.value for archetype in story.secondary_archetypes],
        'selected_plot_line': story.selected_plot_line.to_dict() if story.selected_plot_line else None,
        'expanded_plot_line': story.expanded_plot_line,
        'characters': [char.to_dict() for char in story.characters],
        'chapters': [chapter.to_dict() for chapter in story.chapters]
    }
    
    # Save to file instead of session
    save_story_to_file(story_id, story_data)
    
    # Also save basic story data to session for template access (left panel)
    session['story_data'] = story_data
    session.modified = True
    
    # Clean up old files periodically
    cleanup_old_story_files()


def get_next_incomplete_step(story):
    """Determine the next incomplete step in the story creation process."""
    # Check each step in order and return the first incomplete one
    
    # Step 1: Story type
    if not story.story_type_name:
        return 'index'
    
    # Step 2: Story subtype
    if not story.subtype_name:
        return 'story_type'
    
    # Step 3: Key theme
    if not story.key_theme:
        return 'key_theme_selection'
    
    # Step 4: Core arc
    if not story.core_arc:
        return 'core_arc_selection'
    
    # Step 5: Genre
    if not story.genre:
        return 'genre_selection'
    
    # Step 6: Sub-genre
    if not story.sub_genre:
        return 'subgenre_selection'
    
    # Step 7: Writing style
    if not story.writing_style:
        return 'writing_style_selection'
    
    # Step 8: Protagonist archetype
    if not story.protagonist_archetype:
        return 'protagonist_archetype_selection'
    
    # Step 9: Plot line selection
    # If protagonist archetype is set but no plot line is selected,
    # go to secondary archetype selection (where plot lines can be generated)
    if not story.selected_plot_line:
        return 'secondary_archetype_selection'
    
    # Step 10: Character generation
    # If plot line is selected but no characters generated,
    # go to the selected plot line page (where characters can be generated)
    if not story.characters:
        return 'plot_line_selected'
    
    # Step 11: Chapter plan
    # If characters are generated and chapters exist, go to chapter plan
    if story.chapters:
        return 'chapter_plan'
    
    # If all steps are complete, go to story completion
    return 'complete_story_selection'


@app.route('/')
def index():
    """Main page showing all story types."""
    # Clear session data for fresh visits (not navigation within app)
    referrer = request.headers.get('Referer', '')
    app_domain = request.host_url.rstrip('/')
    
    # If no referrer or referrer is from outside our app, clear session
    if not referrer or not referrer.startswith(app_domain):
        # Clear the story file if it exists
        if 'story_id' in session:
            story_id = session['story_id']
            file_path = get_story_file_path(story_id)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass
        session.clear()
    
    story_types = registry.get_all_story_types()
    
    # Get story and objects for left panel
    story = get_story_from_session() 
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    writing_style_obj = get_writing_style_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    
    return render_template('story_types.html', story_types=story_types, story=story, 
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         writing_style_obj=writing_style_obj,
                         secondary_archetype_objs=secondary_archetype_objs)


@app.route('/story_type/<story_type_name>')
def story_type_detail(story_type_name):
    """Show details and subtypes for a specific story type."""
    story_type = registry.get_story_type(story_type_name)
    if not story_type:
        return redirect(url_for('index'))
    
    # Get story from session and update with story type selection
    story = get_story_from_session()
    previous_story_type_name = story.story_type_name
    story.story_type_name = story_type_name
    
    # Clear subtype and subsequent selections if story type changes
    if previous_story_type_name and previous_story_type_name != story_type_name:
        # We're changing to a different story type, clear dependent selections
        story.subtype_name = None
        story.key_theme = None
        story.core_arc = None
    
    save_story_to_session(story)
    
    # Get the subtype object
    subtype = story_type.get_subtype(story.subtype_name) if story.subtype_name else None
    
    # Get objects for left panel
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    writing_style_obj = get_writing_style_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    
    return render_template('subtypes.html', story_type=story_type, subtype=subtype, story=story, 
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         writing_style_obj=writing_style_obj,
                         secondary_archetype_objs=secondary_archetype_objs)


@app.route('/subtype/<story_type_name>/<subtype_name>')
def subtype_detail(story_type_name, subtype_name):
    """Show subtype detail page with current story progress."""
    story_type = registry.get_story_type(story_type_name)
    if not story_type:
        return redirect(url_for('index'))
    
    subtype = story_type.get_subtype(subtype_name)
    if not subtype:
        return redirect(url_for('story_type_detail', story_type_name=story_type_name))
    
    # Get story from session and update with story type/subtype selection
    story = get_story_from_session()
    story.story_type_name = story_type_name
    story.subtype_name = subtype_name
    save_story_to_session(story)
    
    # Check if this is a redirect from completion or if story already has selections
    # If story has no selections beyond type/subtype, redirect to key theme selection
    if not story.key_theme and not story.core_arc:
        return redirect(url_for('key_theme_selection'))
    
    # Get session data for the template
    story_id = get_story_id()
    saved_selections = load_story_from_file(story_id)
    
    # Get objects for left panel
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    writing_style_obj = get_writing_style_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    
    # Render the subtype detail page showing current progress
    return render_template('subtype_detail.html', 
                         story_type=story_type, 
                         subtype=subtype, 
                         story=story, 
                         saved_selections=saved_selections,
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         writing_style_obj=writing_style_obj,
                         secondary_archetype_objs=secondary_archetype_objs)


@app.route('/key-theme-selection')
def key_theme_selection():
    """Show key theme selection page."""
    story = get_story_from_session()
    
    # Check if story has required data (story type and subtype selections)
    if not story.story_type_name or not story.subtype_name:
        flash('Please complete story type and subtype selection first.', 'error')
        return redirect(url_for('index'))
    
    # Get the story type to access key themes
    story_type = registry.get_story_type(story.story_type_name)
    if not story_type:
        flash('Invalid story type.', 'error')
        return redirect(url_for('index'))
    
    # Get the subtype object
    subtype = story_type.get_subtype(story.subtype_name) if story.subtype_name else None
    
    # Get objects for left panel
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    writing_style_obj = get_writing_style_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    
    return render_template('key_theme_selection.html', story=story, story_type=story_type, subtype=subtype, 
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         writing_style_obj=writing_style_obj,
                         secondary_archetype_objs=secondary_archetype_objs)


@app.route('/key-theme-selection', methods=['POST'])
def update_key_theme_selection():
    """Handle key theme selection form submission."""
    key_theme = request.form.get('key_theme')
    if not key_theme:
        flash('Please select a key theme.', 'error')
        return redirect(url_for('key_theme_selection'))
    
    # Get story from session
    story = get_story_from_session()
    
    # Set key theme
    story.key_theme = key_theme
    save_story_to_session(story)
    
    return redirect(url_for('core_arc_selection'))


@app.route('/core-arc-selection')
def core_arc_selection():
    """Show core arc selection page."""
    story = get_story_from_session()
    
    # Check if story has required data (story type, subtype, and key theme selections)
    if not story.story_type_name or not story.subtype_name or not story.key_theme:
        flash('Please complete story type, subtype, and key theme selection first.', 'error')
        return redirect(url_for('index'))
    
    # Get the story type to access core arcs
    story_type = registry.get_story_type(story.story_type_name)
    if not story_type:
        flash('Invalid story type.', 'error')
        return redirect(url_for('index'))
    
    # Get the subtype object
    subtype = story_type.get_subtype(story.subtype_name) if story.subtype_name else None
    
    # Get objects for left panel
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    writing_style_obj = get_writing_style_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    
    return render_template('core_arc_selection.html', story=story, story_type=story_type, subtype=subtype, 
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         writing_style_obj=writing_style_obj,
                         secondary_archetype_objs=secondary_archetype_objs)


@app.route('/core-arc-selection', methods=['POST'])
def update_core_arc_selection():
    """Handle core arc selection form submission."""
    core_arc = request.form.get('core_arc')
    if not core_arc:
        flash('Please select a core arc.', 'error')
        return redirect(url_for('core_arc_selection'))
    
    # Get story from session
    story = get_story_from_session()
    
    # Set core arc
    story.core_arc = core_arc
    save_story_to_session(story)
    
    return redirect(url_for('genre_selection'))


@app.route('/genre-selection')
def genre_selection():
    """Show genre selection page."""
    story = get_story_from_session()
    
    # Check if story has required data (story type selections)
    if not story.story_type_name or not story.subtype_name:
        flash('Please complete story type selection first.', 'error')
        return redirect(url_for('index'))
    
    # Get the story type to access details for the left panel
    story_type = registry.get_story_type(story.story_type_name)
    
    # Get the subtype object
    subtype = story_type.get_subtype(story.subtype_name) if story.subtype_name else None
    
    # Get objects for left panel
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    writing_style_obj = get_writing_style_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    
    genres = genre_registry.get_all_genres()
    return render_template('genre_selection.html', genres=genres, story=story, story_type=story_type, subtype=subtype, 
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         writing_style_obj=writing_style_obj,
                         secondary_archetype_objs=secondary_archetype_objs)


@app.route('/genre-selection', methods=['POST'])
def update_genre_selection():
    """Handle genre selection form submission."""
    genre_name = request.form.get('genre')
    if not genre_name:
        flash('Please select a genre.', 'error')
        return redirect(url_for('genre_selection'))
    
    # Get story from session
    story = get_story_from_session()
    
    # Set genre
    if story.set_genre(genre_name):
        save_story_to_session(story)
        return redirect(url_for('subgenre_selection'))
    else:
        flash('Invalid genre selection.', 'error')
        return redirect(url_for('genre_selection'))


@app.route('/subgenre-selection')
def subgenre_selection():
    """Show sub-genre selection page."""
    story = get_story_from_session()
    
    # Check if story has required data (story type selections and genre)
    if not story.story_type_name or not story.subtype_name or not story.genre:
        flash('Please complete story type and genre selection first.', 'error')
        return redirect(url_for('index'))
    
    # Get the story type to access details for the left panel
    story_type = registry.get_story_type(story.story_type_name)
    
    # Get the subtype object
    subtype = story_type.get_subtype(story.subtype_name) if story.subtype_name else None
    
    # Get objects for left panel
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    writing_style_obj = get_writing_style_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    
    sub_genres = story.get_available_sub_genres()
    return render_template('subgenre_selection.html', sub_genres=sub_genres, story=story, story_type=story_type, subtype=subtype, 
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         writing_style_obj=writing_style_obj,
                         secondary_archetype_objs=secondary_archetype_objs)


@app.route('/subgenre-selection', methods=['POST'])
def update_subgenre_selection():
    """Handle sub-genre selection form submission."""
    sub_genre_name = request.form.get('sub_genre')
    if not sub_genre_name:
        flash('Please select a sub-genre.', 'error')
        return redirect(url_for('subgenre_selection'))
    
    # Get story from session
    story = get_story_from_session()
    
    # Set sub-genre
    if story.set_sub_genre(sub_genre_name):
        save_story_to_session(story)
        # Redirect to writing style selection instead of protagonist archetype selection
        return redirect(url_for('writing_style_selection'))
    else:
        flash('Invalid sub-genre selection.', 'error')
        return redirect(url_for('subgenre_selection'))


@app.route('/writing-style-selection')
def writing_style_selection():
    """Show writing style selection page."""
    story = get_story_from_session()
    
    # Check if story has required data (story type selections, genre, and sub-genre)
    if not story.story_type_name or not story.subtype_name or not story.genre or not story.sub_genre:
        flash('Please complete story type, genre, and sub-genre selection first.', 'error')
        return redirect(url_for('index'))
    
    # Get the story type to access details for the left panel
    story_type = registry.get_story_type(story.story_type_name)
    
    # Get the subtype object
    subtype = story_type.get_subtype(story.subtype_name) if story.subtype_name else None
    
    # Get all available writing styles
    styles = story.get_available_styles()
    
    # Get objects for left panel
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    writing_style_obj = get_writing_style_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    
    return render_template('writing_style_selection.html', 
                         styles=styles, 
                         story=story, 
                         story_type=story_type, 
                         subtype=subtype,
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         writing_style_obj=writing_style_obj,
                         secondary_archetype_objs=secondary_archetype_objs)


@app.route('/writing-style-selection', methods=['POST'])
def update_writing_style_selection():
    """Handle writing style selection form submission."""
    writing_style_name = request.form.get('writing_style')
    if not writing_style_name:
        flash('Please select a writing style.', 'error')
        return redirect(url_for('writing_style_selection'))
    
    # Get story from session
    story = get_story_from_session()
    
    # Set writing style
    if story.set_writing_style(writing_style_name):
        save_story_to_session(story)
        return redirect(url_for('protagonist_archetype_selection'))
    else:
        flash('Invalid writing style selection.', 'error')
        return redirect(url_for('writing_style_selection'))


@app.route('/protagonist-archetype-selection')
def protagonist_archetype_selection():
    """Show protagonist archetype selection page."""
    story = get_story_from_session()
    
    # Check if story has required data (story type selections, genre, sub-genre, and writing style)
    if not story.story_type_name or not story.subtype_name or not story.genre or not story.sub_genre or not story.writing_style:
        flash('Please complete story type, genre, sub-genre, and writing style selection first.', 'error')
        return redirect(url_for('index'))
    
    # Get the story type to access details for the left panel
    story_type = registry.get_story_type(story.story_type_name)
    
    # Get the subtype object
    subtype = story_type.get_subtype(story.subtype_name) if story_type and story.subtype_name else None
    
    # Get typical and other archetypes
    typical_archetypes = story.get_typical_archetypes()
    other_archetype_names = story.get_other_archetypes()
    
    # Get archetype objects with descriptions
    typical_archetype_objects = []
    for name in typical_archetypes:
        archetype = archetype_registry.get_archetype(name)
        if archetype:
            typical_archetype_objects.append(archetype)
    
    other_archetype_objects = []
    for name in other_archetype_names:
        archetype = archetype_registry.get_archetype(name)
        if archetype:
            other_archetype_objects.append(archetype)
    
    return render_template('protagonist_archetype_selection.html', 
                         story=story, 
                         story_type=story_type,
                         subtype=subtype,
                         typical_archetypes=typical_archetype_objects,
                         other_archetypes=other_archetype_objects,
                         protagonist_archetype_obj=get_protagonist_archetype_object(story),
                         writing_style_obj=get_writing_style_object(story),
                         secondary_archetype_objs=get_secondary_archetype_objects(story))


@app.route('/protagonist-archetype-selection', methods=['POST'])
def update_protagonist_archetype_selection():
    """Handle protagonist archetype selection form submission."""
    protagonist_archetype = request.form.get('protagonist_archetype')
    
    if not protagonist_archetype:
        flash('Please select a protagonist archetype.', 'error')
        return redirect(url_for('protagonist_archetype_selection'))
    
    # Get story from session
    story = get_story_from_session()
    
    # Set protagonist archetype
    if story.set_protagonist_archetype(protagonist_archetype):
        save_story_to_session(story)
        return redirect(url_for('secondary_archetype_selection'))
    else:
        flash('Invalid protagonist archetype selection.', 'error')
        return redirect(url_for('protagonist_archetype_selection'))


@app.route('/secondary-archetype-selection')
def secondary_archetype_selection():
    """Show secondary archetype selection page."""
    story = get_story_from_session()
    
    # Check if story has required data including protagonist archetype and writing style
    if not story.story_type_name or not story.subtype_name or not story.genre or not story.sub_genre or not story.writing_style or not story.protagonist_archetype:
        flash('Please complete story type, genre, sub-genre, writing style, and protagonist archetype selection first.', 'error')
        return redirect(url_for('index'))
    
    # Get the story type to access details for the left panel
    story_type = registry.get_story_type(story.story_type_name)
    
    # Get the subtype object
    subtype = story_type.get_subtype(story.subtype_name) if story_type and story.subtype_name else None
    
    # Get typical and other archetypes, including the already selected protagonist
    typical_archetypes = story.get_typical_archetypes()
    other_archetype_names = story.get_other_archetypes()
    
    # Don't remove protagonist archetype - we want to show it as disabled
    
    # Get archetype objects with descriptions
    typical_archetype_objects = []
    for name in typical_archetypes:
        archetype = archetype_registry.get_archetype(name)
        if archetype:
            typical_archetype_objects.append(archetype)
    
    other_archetype_objects = []
    for name in other_archetype_names:
        archetype = archetype_registry.get_archetype(name)
        if archetype:
            other_archetype_objects.append(archetype)
    
    return render_template('secondary_archetype_selection.html', 
                         story=story, 
                         story_type=story_type,
                         subtype=subtype,
                         typical_archetypes=typical_archetype_objects,
                         other_archetypes=other_archetype_objects,
                         protagonist_archetype_obj=get_protagonist_archetype_object(story),
                         writing_style_obj=get_writing_style_object(story),
                         secondary_archetype_objs=get_secondary_archetype_objects(story))


@app.route('/secondary-archetype-selection', methods=['POST'])
def update_secondary_archetype_selection():
    """Handle secondary archetype selection form submission."""
    secondary_archetypes = request.form.getlist('secondary_archetypes')
    
    # Get story from session
    story = get_story_from_session()
    
    # Set secondary archetypes (can be empty list if none selected)
    if story.set_secondary_archetypes(secondary_archetypes):
        save_story_to_session(story)
        # Redirect to the story completion page
        return redirect(url_for('complete_story_selection'))
    else:
        flash('Error saving secondary archetype selection.', 'error')
        return redirect(url_for('secondary_archetype_selection'))


@app.route('/navigate-to-step/<step>')
def navigate_to_step(step):
    """Navigate back to a specific selection step, clearing dependent selections."""
    story = get_story_from_session()
    
    # Define step hierarchy - when going back to a step, clear that step and all after it
    step_hierarchy = [
        'story_type',
        'subtype', 
        'key_theme',
        'core_arc',
        'genre',
        'sub_genre',
        'writing_style',
        'protagonist_archetype',
        'secondary_archetypes'
    ]
    
    # Find the step index to clear from
    try:
        step_index = step_hierarchy.index(step)
    except ValueError:
        flash('Invalid navigation step.', 'error')
        return redirect(url_for('index'))
    
    # Clear the selected step and all subsequent steps
    steps_to_clear = step_hierarchy[step_index:]
    
    for clear_step in steps_to_clear:
        if clear_step == 'story_type':
            story.story_type_name = None
        elif clear_step == 'subtype':
            story.subtype_name = None
        elif clear_step == 'key_theme':
            story.key_theme = None
        elif clear_step == 'core_arc':
            story.core_arc = None
        elif clear_step == 'genre':
            story.genre = None
        elif clear_step == 'sub_genre':
            story.sub_genre = None
        elif clear_step == 'writing_style':
            story.writing_style = None
        elif clear_step == 'protagonist_archetype':
            story.protagonist_archetype = None
        elif clear_step == 'secondary_archetypes':
            story.secondary_archetypes = []
    
    # Clear selected plot line when any step is changed
    story.clear_selected_plot_line()
    
    save_story_to_session(story)
    
    # Redirect to the appropriate selection page
    if step == 'story_type':
        return redirect(url_for('index'))
    elif step == 'subtype':
        if story.story_type_name:
            return redirect(url_for('story_type_detail', story_type_name=story.story_type_name))
        else:
            return redirect(url_for('index'))
    elif step == 'key_theme':
        return redirect(url_for('key_theme_selection'))
    elif step == 'core_arc':
        return redirect(url_for('core_arc_selection'))
    elif step == 'genre':
        return redirect(url_for('genre_selection'))
    elif step == 'sub_genre':
        return redirect(url_for('subgenre_selection'))
    elif step == 'writing_style':
        return redirect(url_for('writing_style_selection'))
    elif step == 'protagonist_archetype':
        return redirect(url_for('protagonist_archetype_selection'))
    elif step == 'secondary_archetypes':
        return redirect(url_for('secondary_archetype_selection'))
    else:
        return redirect(url_for('index'))


@app.route('/edit-plot-line')
def edit_plot_line():
    """Edit the selected plot line by clearing it and returning to secondary character selection."""
    story = get_story_from_session()
    
    # Clear plot line related data
    story.clear_selected_plot_line()
    story.clear_expanded_plot_line()
    # Clear all characters since they were generated based on the plot line
    story.characters = []
    
    save_story_to_session(story)
    
    # Redirect to secondary archetype selection where plot lines can be generated
    return redirect(url_for('secondary_archetype_selection'))


@app.route('/save')
def save_story():
    """Save current story to JSON file."""
    story = get_story_from_session()
    json_data = story.to_json()
    
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=kraitif_story.json'
    
    return response


@app.route('/load', methods=['POST'])
def load_story():
    """Load story from uploaded JSON file."""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and file.filename.endswith('.json'):
        try:
            content = file.read().decode('utf-8')
            story = Story()
            if story.from_json(content):
                save_story_to_session(story)
                flash('Story loaded successfully!', 'success')
                
                # Determine the next incomplete step and redirect appropriately
                next_step = get_next_incomplete_step(story)
                
                if next_step == 'index':
                    return redirect(url_for('index'))
                elif next_step == 'story_type':
                    # If we have a story type name, redirect to that story type detail page
                    if story.story_type_name:
                        return redirect(url_for('story_type_detail', story_type_name=story.story_type_name))
                    else:
                        return redirect(url_for('index'))
                elif next_step == 'key_theme_selection':
                    return redirect(url_for('key_theme_selection'))
                elif next_step == 'core_arc_selection':
                    return redirect(url_for('core_arc_selection'))
                elif next_step == 'genre_selection':
                    return redirect(url_for('genre_selection'))
                elif next_step == 'subgenre_selection':
                    return redirect(url_for('subgenre_selection'))
                elif next_step == 'writing_style_selection':
                    return redirect(url_for('writing_style_selection'))
                elif next_step == 'protagonist_archetype_selection':
                    return redirect(url_for('protagonist_archetype_selection'))
                elif next_step == 'secondary_archetype_selection':
                    return redirect(url_for('secondary_archetype_selection'))
                elif next_step == 'plot_line_selected':
                    return redirect(url_for('plot_line_selected'))
                elif next_step == 'chapter_plan':
                    return redirect(url_for('chapter_plan'))
                elif next_step == 'complete_story_selection':
                    return redirect(url_for('complete_story_selection'))
                else:
                    # Fallback to index if something goes wrong
                    return redirect(url_for('index'))
            else:
                flash('Invalid story file format', 'error')
        except Exception as e:
            flash(f'Error loading file: {str(e)}', 'error')
    else:
        flash('Please select a JSON file', 'error')
    
    return redirect(url_for('index'))


@app.route('/new')
def new_story():
    """Clear all story selections and start a new story."""
    # Clear the story file if it exists
    if 'story_id' in session:
        story_id = session['story_id']
        file_path = get_story_file_path(story_id)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
    
    session.clear()
    flash('New story started. All previous selections have been cleared.', 'success')
    return redirect(url_for('index'))


@app.route('/generate-plot-lines', methods=['POST'])
def generate_plot_lines():
    """Generate plot lines using AI based on the current story configuration."""
    story = get_story_from_session()
    
    # Check if we have a reasonably complete story
    if not story.story_type_name or not story.subtype_name:
        return jsonify({'error': 'Please complete at least the story type and subtype selection first.'}), 400
    
    try:
        # Generate the prompt text
        prompt_text = prompt_generator.generate_plot_prompt(story)
        
        # Get AI response
        ai_response = get_ai_response(prompt_text, PromptType.PLOT_LINES)
        
        # Parse plot lines from the response
        plot_lines = parse_plot_lines_from_ai_response(ai_response)
        
        # Convert to dictionaries for JSON response
        plot_lines_data = [plot_line.to_dict() for plot_line in plot_lines]
        
        return jsonify({
            'success': True,
            'plot_lines': plot_lines_data,
            'ai_response': ai_response  # Include for debugging if needed
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/select-plot-line', methods=['POST'])
def select_plot_line():
    """Select a plot line and save it to the story."""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'plotline' not in data:
            return jsonify({
                'success': False,
                'error': 'Invalid plot line data provided'
            }), 400
        
        # Get story from session
        story = get_story_from_session()
        
        # Create plot line object
        plot_line = PlotLine(name=data['name'], plotline=data['plotline'])
        
        # Set the selected plot line
        if story.set_selected_plot_line(plot_line):
            save_story_to_session(story)
            return jsonify({
                'success': True,
                'message': 'Plot line selected successfully',
                'redirect_url': url_for('plot_line_selected')
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to set selected plot line'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/plot-line-selected')
def plot_line_selected():
    """Show the selected plot line details page."""
    story = get_story_from_session()
    
    # Check if we have a selected plot line
    if not story.selected_plot_line:
        flash('Please select a plot line first.', 'error')
        return redirect(url_for('complete_story_selection'))
    
    # Get additional context objects for the template
    story_type = None
    subtype = None
    if story.story_type_name:
        story_type = registry.get_story_type(story.story_type_name)
        if story_type and story.subtype_name:
            subtype = story_type.get_subtype(story.subtype_name)
    
    # Get protagonist and secondary archetype objects
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    writing_style_obj = get_writing_style_object(story)
    
    return render_template('plot_line_selected.html',
                         story=story,
                         story_type=story_type,
                         subtype=subtype,
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         secondary_archetype_objs=secondary_archetype_objs,
                         writing_style_obj=writing_style_obj,
                         genre_registry=genre_registry,
                         archetype_registry=archetype_registry,
                         style_registry=style_registry)


@app.route('/generate-characters', methods=['POST'])
def generate_characters():
    """Generate characters and expanded plot line using AI based on the current story configuration."""
    story = get_story_from_session()
    
    # Check if we have a selected plot line
    if not story.selected_plot_line:
        return jsonify({'error': 'Please select a plot line first.'}), 400
    
    # Check if we have a reasonably complete story
    if not story.story_type_name or not story.subtype_name:
        return jsonify({'error': 'Please complete at least the story type and subtype selection first.'}), 400
    
    try:
        # Generate the prompt text
        prompt_text = prompt_generator.generate_character_prompt(story)
        
        # Get AI response
        ai_response = get_ai_response(prompt_text, PromptType.CHARACTERS)
        
        # Parse characters and expanded plot line from the response
        expanded_plot_line, characters = parse_characters_from_ai_response(ai_response)
        
        # Update the story with the results
        if expanded_plot_line:
            story.set_expanded_plot_line(expanded_plot_line)
        
        # Clear existing characters and add new ones
        story.characters.clear()
        for character in characters:
            story.add_character(character)
        
        # Save to session
        save_story_to_session(story)
        
        return jsonify({
            'success': True,
            'expanded_plot_line': expanded_plot_line,
            'characters': [char.to_dict() for char in characters],
            'ai_response': ai_response  # Include for debugging if needed
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/expanded-story')
def expanded_story():
    """Show the expanded story with characters and expanded plot line."""
    story = get_story_from_session()
    
    # Check if we have the required data
    if not story.selected_plot_line:
        flash('Please select a plot line first.', 'error')
        return redirect(url_for('complete_story_selection'))
    
    if not story.expanded_plot_line and not story.characters:
        flash('Please generate characters first.', 'error')
        return redirect(url_for('complete_story_selection'))
    
    # Get additional context objects for the template
    story_type = None
    subtype = None
    if story.story_type_name:
        story_type = registry.get_story_type(story.story_type_name)
        if story_type and story.subtype_name:
            subtype = story_type.get_subtype(story.subtype_name)
    
    # Get protagonist and secondary archetype objects
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    writing_style_obj = get_writing_style_object(story)
    
    return render_template('expanded_story.html',
                         story=story,
                         story_type=story_type,
                         subtype=subtype,
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         secondary_archetype_objs=secondary_archetype_objs,
                         writing_style_obj=writing_style_obj,
                         genre_registry=genre_registry,
                         archetype_registry=archetype_registry,
                         style_registry=style_registry)


@app.route('/chapter-plan')
def chapter_plan():
    """Show the chapter plan page with detailed chapter outlines."""
    story = get_story_from_session()
    
    # Check if we have the required data
    if not story.selected_plot_line:
        flash('Please select a plot line first.', 'error')
        return redirect(url_for('complete_story_selection'))
    
    if not story.expanded_plot_line or not story.characters:
        flash('Please generate characters first.', 'error')
        return redirect(url_for('expanded_story'))
    
    if not story.chapters:
        flash('Please generate a chapter plan first.', 'error')
        return redirect(url_for('expanded_story'))
    
    # Get additional context objects for the template
    story_type = None
    subtype = None
    if story.story_type_name:
        story_type = registry.get_story_type(story.story_type_name)
        if story_type and story.subtype_name:
            subtype = story_type.get_subtype(story.subtype_name)
    
    # Get protagonist and secondary archetype objects
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    writing_style_obj = get_writing_style_object(story)
    
    return render_template('chapter_plan.html',
                         story=story,
                         story_type=story_type,
                         subtype=subtype,
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         secondary_archetype_objs=secondary_archetype_objs,
                         writing_style_obj=writing_style_obj,
                         genre_registry=genre_registry,
                         archetype_registry=archetype_registry,
                         style_registry=style_registry,
                         is_chapter_plan_page=True)


@app.route('/generate-chapters', methods=['POST'])
def generate_chapters():
    """Generate chapter plan using AI based on the current story configuration."""
    story = get_story_from_session()
    
    # Check if we have the required data
    if not story.expanded_plot_line or not story.characters:
        return jsonify({'error': 'Please generate characters first.'}), 400
    
    # Check if we have a reasonably complete story
    if not story.story_type_name or not story.subtype_name:
        return jsonify({'error': 'Please complete at least the story type and subtype selection first.'}), 400
    
    try:
        # Generate the prompt text using chapter outline prompt
        prompt_text = prompt_generator.generate_chapter_outline_prompt(story)
        
        # Get AI response
        ai_response = get_ai_response(prompt_text, PromptType.CHAPTER_OUTLINE)
        
        # Parse chapters from the response
        chapters = parse_chapters_from_ai_response(ai_response)
        
        # Validate that all character names in chapters exist in story
        story_character_names = [char.name for char in story.characters]
        missing_characters = validate_chapter_character_names(chapters, story_character_names)
        
        if missing_characters:
            return jsonify({
                'success': False,
                'error': 'character_validation',
                'missing_characters': missing_characters,
                'message': f'Some characters referenced in chapters do not exist in the story: {", ".join(missing_characters)}'
            })
        
        # Clear existing chapters and add new ones
        story.chapters.clear()
        for chapter in chapters:
            story.add_chapter(chapter)
        
        # Save to session
        save_story_to_session(story)
        
        return jsonify({
            'success': True,
            'chapters': [chapter.to_dict() for chapter in chapters],
            'ai_response': ai_response  # Include for debugging if needed
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/generate-chapter/<int:chapter_number>', methods=['POST'])
def generate_chapter(chapter_number):
    """Generate a single chapter using AI based on the current story configuration."""
    story = get_story_from_session()
    
    # Check if we have the required data
    if not story.expanded_plot_line or not story.characters:
        return jsonify({'error': 'Please generate characters first.'}), 400
    
    if not story.chapters:
        return jsonify({'error': 'Please generate a chapter plan first.'}), 400
    
    # Check if the requested chapter number exists in the story
    existing_chapter = story.get_chapter(chapter_number)
    if not existing_chapter:
        return jsonify({'error': f'Chapter {chapter_number} does not exist in the story plan.'}), 400
    
    # Check if chapter already has chapter_text (already generated)
    if existing_chapter.chapter_text:
        return jsonify({'error': f'Chapter {chapter_number} has already been generated.'}), 400
    
    try:
        # Generate the prompt text using chapter prompt
        prompt_text = prompt_generator.generate_chapter_prompt(story, chapter_number)
        
        # Get AI response
        ai_response = get_ai_response(prompt_text, PromptType.CHAPTER)
        
        # Parse chapter from the response
        generated_chapter = parse_single_chapter_from_ai_response(ai_response, chapter_number)
        
        if not generated_chapter:
            return jsonify({
                'success': False,
                'error': 'Failed to parse chapter from AI response'
            })
        
        # Validate that all character names in chapter exist in story
        story_character_names = [char.name for char in story.characters]
        chapter_missing_chars = []
        
        # Check continuity state for character references
        if generated_chapter.continuity_state:
            for cont_char in generated_chapter.continuity_state.characters:
                if cont_char.name.lower() not in [name.lower() for name in story_character_names]:
                    chapter_missing_chars.append(cont_char.name)
        
        if chapter_missing_chars:
            return jsonify({
                'success': False,
                'error': 'character_validation',
                'missing_characters': chapter_missing_chars,
                'message': f'Some characters referenced in chapter do not exist in the story: {", ".join(chapter_missing_chars)}'
            })
        
        # Update the existing chapter with generated content
        existing_chapter.chapter_text = generated_chapter.chapter_text
        existing_chapter.summary = generated_chapter.summary
        existing_chapter.continuity_state = generated_chapter.continuity_state
        
        # Save to session
        save_story_to_session(story)
        
        return jsonify({
            'success': True,
            'chapter': existing_chapter.to_dict(),
            'redirect_url': url_for('chapter_detail', chapter_number=chapter_number),
            'ai_response': ai_response  # Include for debugging if needed
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/chapter/<int:chapter_number>')
def chapter_detail(chapter_number):
    """Show details for a specific chapter."""
    story = get_story_from_session()
    
    # Check if we have the required data
    if not story.chapters:
        flash('Please generate a chapter plan first.', 'error')
        return redirect(url_for('chapter_plan'))
    
    # Get the specific chapter
    chapter = story.get_chapter(chapter_number)
    if not chapter:
        flash(f'Chapter {chapter_number} does not exist.', 'error')
        return redirect(url_for('chapter_plan'))
    
    # Get additional context objects for the template
    story_type = None
    subtype = None
    if story.story_type_name:
        story_type = registry.get_story_type(story.story_type_name)
        if story_type and story.subtype_name:
            subtype = story_type.get_subtype(story.subtype_name)
    
    # Get protagonist and secondary archetype objects
    protagonist_archetype_obj = get_protagonist_archetype_object(story)
    secondary_archetype_objs = get_secondary_archetype_objects(story)
    writing_style_obj = get_writing_style_object(story)
    
    return render_template('chapter_detail.html',
                         story=story,
                         chapter=chapter,
                         chapter_number=chapter_number,
                         story_type=story_type,
                         subtype=subtype,
                         protagonist_archetype_obj=protagonist_archetype_obj,
                         secondary_archetype_objs=secondary_archetype_objs,
                         writing_style_obj=writing_style_obj,
                         genre_registry=genre_registry,
                         archetype_registry=archetype_registry,
                         style_registry=style_registry,
                         is_chapter_detail_page=True)


@app.route('/test-chapters')
def test_chapters():
    """Test route to manually create a story with chapters for UI testing."""
    from objects.plot_line import PlotLine
    from objects.character import Character
    from objects.archetype import ArchetypeEnum
    from objects.functional_role import FunctionalRoleEnum
    from objects.emotional_function import EmotionalFunctionEnum
    from objects.chapter import Chapter
    from objects.narrative_function import NarrativeFunctionEnum
    
    # Create test story
    story = Story()
    story.story_type_name = 'The Quest'
    story.subtype_name = 'Object Quest'
    story.key_theme = 'Growth occurs through shared adventure and sacrifice.'
    story.core_arc = 'Hero discovers strength through perseverance.'
    story.set_genre('Fantasy')
    story.set_sub_genre('High Fantasy')
    story.set_writing_style('Lyrical')
    story.protagonist_archetype = ArchetypeEnum.CHOSEN_ONE
    
    # Add plot line
    plot_line = PlotLine(
        name='The Ancient Relic Quest',
        plotline='A young chosen one must retrieve an ancient magical artifact to save their realm from an encroaching darkness.'
    )
    story.selected_plot_line = plot_line
    story.expanded_plot_line = "In the realm of Aethermoor, young Lyra discovers she is the prophesied Chosen One when ancient runes appear on her skin during her village's harvest festival. The mysterious sage Aldric reveals that the Shadowblight is spreading across the land, corrupting everything it touches. Only the legendary Sunstone of Vaelthara can restore the balance."
    
    # Add characters
    characters = [
        Character(
            name="Lyra",
            archetype=ArchetypeEnum.CHOSEN_ONE,
            functional_role=FunctionalRoleEnum.PROTAGONIST,
            emotional_function=EmotionalFunctionEnum.SYMPATHETIC_CHARACTER,
            backstory="A simple village girl who discovers her destiny when ancient runes appear on her skin during the harvest festival.",
            character_arc="Transforms from a frightened, reluctant hero into a confident leader who understands that true power comes from unity and sacrifice."
        ),
        Character(
            name="Aldric",
            archetype=ArchetypeEnum.WISE_MENTOR,
            functional_role=FunctionalRoleEnum.MENTOR,
            emotional_function=EmotionalFunctionEnum.CATALYST,
            backstory="An ancient sage who has waited centuries for the prophesied Chosen One to appear.",
            character_arc="Learns to trust in the new generation and finds peace in passing on his wisdom."
        ),
        Character(
            name="Kael",
            archetype=ArchetypeEnum.LOYAL_COMPANION,
            functional_role=FunctionalRoleEnum.GUARDIAN_GATEKEEPER,
            emotional_function=EmotionalFunctionEnum.VICTIM,
            backstory="A former knight of the fallen kingdom of Drakmoor, haunted by his failure to protect his people.",
            character_arc="Overcomes his guilt and self-doubt to become a true protector."
        )
    ]
    
    for character in characters:
        story.add_character(character)
    
    # Add test chapters
    chapters = [
        Chapter(
            chapter_number=1,
            title="The Awakening",
            overview="In the village of Thornfield, Lyra discovers her destiny when ancient runes suddenly appear on her skin during the harvest festival. The mysterious sage Aldric arrives to explain her role as the Chosen One.",
            character_impact=[
                {"character": "Lyra", "effect": "Discovers her identity as the Chosen One and reluctantly accepts her destiny, feeling overwhelmed but determined."},
                {"character": "Aldric", "effect": "Reveals long-held secrets about the prophecy and begins mentoring Lyra, finding purpose in his centuries of waiting."}
            ],
            point_of_view="Lyra",
            narrative_function=NarrativeFunctionEnum.INCITING_INCIDENT,
            foreshadow_or_echo="The glowing runes foreshadow the final ritual where Lyra must sacrifice her ego to save the realm.",
            scene_highlights="The dramatic moment when the runes first glow, the festival crowd's reaction, and Aldric's mystical entrance.",
            chapter_text="The harvest festival was in full swing when it happened. Lyra had been laughing with her friends, the golden wheat swaying in the evening breeze, when the burning sensation began. It started as a tingling in her palms, then spread up her arms like fire racing through her veins.\n\nShe gasped, stumbling backward as intricate runes blazed to life across her skin—silver lines that pulsed with an otherworldly light. The music stopped. The laughter died. Every eye in the village square turned to her.\n\n'The Chosen One,' whispered an old woman, falling to her knees.\n\nThat was when Aldric appeared, as if stepping from the very shadows themselves. His ancient eyes held both sorrow and hope as he looked upon her glowing marks.\n\n'It is time,' he said simply.",
            summary="Lyra discovers her destiny as the Chosen One when ancient runes appear on her skin during the harvest festival, and the sage Aldric arrives to guide her."
        ),
        Chapter(
            chapter_number=2,
            title="The Gathering Storm", 
            overview="Lyra and Aldric begin their journey, seeking the first clues to the Sunstone's location. They encounter the spreading Shadowblight and witness its devastating effects on the countryside.",
            character_impact=[
                {"character": "Lyra", "effect": "Sees the true scope of the threat and realizes the urgency of her mission, beginning to overcome her self-doubt."},
                {"character": "Aldric", "effect": "Shares more of his burden and knowledge while training Lyra in basic magic and survival skills."}
            ],
            point_of_view="Lyra",
            narrative_function=NarrativeFunctionEnum.RISING_TENSION,
            foreshadow_or_echo="The corruption patterns echo the ancient texts Aldric carries, hinting at the cyclical nature of this threat.",
            scene_highlights="A haunting scene of a corrupted forest, Lyra's first attempts at magic, and refugees fleeing the blight.",
            chapter_text="Three days had passed since leaving Thornfield, and the world around them grew darker with each mile. Where once green fields had stretched toward the horizon, now twisted black veins spider-webbed across the earth—the unmistakable mark of the Shadowblight.\n\nLyra watched in horror as a once-proud oak tree crumbled to ash at their approach, its bark having turned an unnatural shade of violet. 'How long has it been spreading?' she asked, her voice barely above a whisper.\n\nAldric's weathered face was grim. 'Faster than ever before. The barrier between realms grows thin.' He knelt beside a corrupted stream, its waters running black as midnight. 'We must find the Sunstone before the blight reaches the capital.'",
            summary="Lyra and Aldric witness the devastating spread of the Shadowblight as they begin their quest for the Sunstone."
        ),
        Chapter(
            chapter_number=3,
            title="Allies and Enemies",
            overview="In the border town of Millhaven, Lyra and Aldric recruit their first companions. They meet Kael, a disgraced knight seeking redemption, and Zara, a thief with hidden magical abilities.",
            character_impact=[
                {"character": "Lyra", "effect": "Learns to trust others and begins developing leadership skills, though still struggling with confidence."},
                {"character": "Kael", "effect": "Finds new purpose in the quest and begins to believe in redemption through service to others."}
            ],
            point_of_view="Kael",
            narrative_function=NarrativeFunctionEnum.CHARACTER_INTRODUCTION,
            foreshadow_or_echo="Kael's story of failure echoes themes of redemption that will be central to the climax.",
            scene_highlights="A tavern brawl that reveals each character's skills, and the group's first bonding moment around a campfire."
        )
    ]
    
    for chapter in chapters:
        story.add_chapter(chapter)
    
    # Save to session
    save_story_to_session(story)
    
    return redirect(url_for('chapter_plan'))


@app.route('/complete-story-selection')
def complete_story_selection():
    """Show the completed story selection with interactive plot line generation."""
    story = get_story_from_session()
    
    # Check if we have a reasonably complete story
    if not story.story_type_name or not story.subtype_name:
        flash('Please complete at least the story type and subtype selection first.', 'error')
        return redirect(url_for('index'))
    
    # Generate the prompt text using the new Prompt class
    prompt_text = prompt_generator.generate_plot_prompt(story)
    
    # Get additional context objects for the template
    story_type = None
    subtype = None
    if story.story_type_name and story.subtype_name:
        story_type = registry.get_story_type(story.story_type_name)
        if story_type:
            subtype = story_type.get_subtype(story.subtype_name)
    
    return render_template('story_completion.html',
                         story=story,
                         story_type=story_type,
                         subtype=subtype,
                         prompt_text=prompt_text,
                         protagonist_archetype_obj=get_protagonist_archetype_object(story),
                         writing_style_obj=get_writing_style_object(story),
                         secondary_archetype_objs=get_secondary_archetype_objects(story),
                         is_story_complete=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)