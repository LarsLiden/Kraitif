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
from story_types import StoryTypeRegistry
from story import Story
from genre import GenreRegistry
from archetype import ArchetypeRegistry
from style import StyleRegistry
from prompt import Prompt
from plot_line import PlotLine, parse_plot_lines_from_ai_response
from ai.ai_client import get_ai_response

app = Flask(__name__)
app.secret_key = 'kraitif_story_selection_key'  # For session management

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


def get_story_from_session():
    """Get or create a Story object from session data."""
    story = Story()
    if 'story_data' in session:
        story_data = session['story_data']
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
        # Legacy support
        selected_archetypes = story_data.get('selected_archetypes', [])
        if selected_archetypes and not story.protagonist_archetype and not story.secondary_archetypes:
            story.set_archetypes(selected_archetypes)
    return story


def get_protagonist_archetype_object(story):
    """Get the protagonist archetype object from the story."""
    if story.protagonist_archetype:
        return archetype_registry.get_archetype(story.protagonist_archetype)
    return None


def get_writing_style_object(story):
    """Get the writing style object from the story."""
    return story.writing_style


def get_secondary_archetype_objects(story):
    """Get the secondary archetype objects from the story."""
    if story.secondary_archetypes:
        secondary_objects = []
        for archetype_name in story.secondary_archetypes:
            archetype = archetype_registry.get_archetype(archetype_name)
            if archetype:
                secondary_objects.append(archetype)
        return secondary_objects
    return []


def save_story_to_session(story):
    """Save Story object to session."""
    session['story_data'] = {
        'story_type_name': story.story_type_name,
        'subtype_name': story.subtype_name,
        'key_theme': story.key_theme,
        'core_arc': story.core_arc,
        'genre_name': story.genre.name if story.genre else None,
        'sub_genre_name': story.sub_genre.name if story.sub_genre else None,
        'writing_style_name': story.writing_style.name if story.writing_style else None,
        'protagonist_archetype': story.protagonist_archetype,
        'secondary_archetypes': story.secondary_archetypes,
        'selected_archetypes': story.selected_archetypes  # Keep for backward compatibility
    }
    session.modified = True


@app.route('/')
def index():
    """Main page showing all story types."""
    # Clear session data for fresh visits (not navigation within app)
    referrer = request.headers.get('Referer', '')
    app_domain = request.host_url.rstrip('/')
    
    # If no referrer or referrer is from outside our app, clear session
    if not referrer or not referrer.startswith(app_domain):
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
    saved_selections = session.get('story_data', {})
    
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


@app.route('/archetype-selection')
def archetype_selection():
    """Show archetype selection page."""
    story = get_story_from_session()
    
    # Check if story has required data (story type selections, genre, sub-genre, and writing style)
    if not story.story_type_name or not story.subtype_name or not story.genre or not story.sub_genre or not story.writing_style:
        flash('Please complete story type, genre, sub-genre, and writing style selection first.', 'error')
        return redirect(url_for('index'))
    
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
    
    return render_template('archetype_selection.html', 
                         story=story, 
                         typical_archetypes=typical_archetype_objects,
                         other_archetypes=other_archetype_objects,
                         protagonist_archetype_obj=get_protagonist_archetype_object(story),
                         writing_style_obj=get_writing_style_object(story),
                         secondary_archetype_objs=get_secondary_archetype_objects(story))


@app.route('/archetype-selection', methods=['POST'])
def update_archetype_selection():
    """Handle archetype selection form submission."""
    selected_archetypes = request.form.getlist('archetypes')
    
    # Get story from session
    story = get_story_from_session()
    
    # Set archetypes (can be empty list if none selected)
    if story.set_archetypes(selected_archetypes):
        save_story_to_session(story)
        # Redirect to the story completion page
        return redirect(url_for('complete_story_selection'))
    else:
        flash('Error saving archetype selection.', 'error')
        return redirect(url_for('archetype_selection'))


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
                # Redirect to the loaded story's subtype page if story data exists
                if story.story_type_name and story.subtype_name:
                    return redirect(url_for('subtype_detail', 
                                          story_type_name=story.story_type_name, 
                                          subtype_name=story.subtype_name))
            else:
                flash('Invalid story file format', 'error')
        except Exception as e:
            flash('Error loading file', 'error')
    else:
        flash('Please select a JSON file', 'error')
    
    return redirect(url_for('index'))


@app.route('/new')
def new_story():
    """Clear all story selections and start a new story."""
    session.clear()
    flash('New story started. All previous selections have been cleared.', 'success')
    return redirect(url_for('index'))


@app.route('/complete-story-selection')
def complete_story_selection():
    """Show the completed story selection with AI-generated plot lines."""
    story = get_story_from_session()
    
    # Check if we have a reasonably complete story
    if not story.story_type_name or not story.subtype_name:
        flash('Please complete at least the story type and subtype selection first.', 'error')
        return redirect(url_for('index'))
    
    # Generate the prompt text using the new Prompt class
    prompt_text = prompt_generator.generate_plot_prompt(story)
    
    # Generate AI plot lines automatically
    plot_lines = []
    ai_error = None
    try:
        # Get AI response
        ai_response = get_ai_response(prompt_text)
        
        # Parse plot lines from the response
        plot_lines = parse_plot_lines_from_ai_response(ai_response)
    except Exception as e:
        ai_error = f'Failed to generate plot lines: {str(e)}'
    
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
                         plot_lines=plot_lines,
                         ai_error=ai_error,
                         protagonist_archetype_obj=get_protagonist_archetype_object(story),
                         writing_style_obj=get_writing_style_object(story),
                         secondary_archetype_objs=get_secondary_archetype_objects(story),
                         is_story_complete=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)