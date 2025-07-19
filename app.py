#!/usr/bin/env python3
"""
Flask web application for Story Types and SubTypes

This Flask app provides a web interface to explore the seven classical story types
and their subtypes.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from story_types import StoryTypeRegistry
from story import Story
from genre import GenreRegistry

app = Flask(__name__)
app.secret_key = 'kraitif_story_selection_key'  # For session management

# Initialize the story types registry
registry = StoryTypeRegistry()

# Initialize the genre registry
genre_registry = GenreRegistry()

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
    return story


def save_story_to_session(story):
    """Save Story object to session."""
    session['story_data'] = {
        'story_type_name': story.story_type_name,
        'subtype_name': story.subtype_name,
        'key_theme': story.key_theme,
        'core_arc': story.core_arc,
        'genre_name': story.genre.name if story.genre else None,
        'sub_genre_name': story.sub_genre.name if story.sub_genre else None
    }
    session.modified = True


@app.route('/')
def index():
    """Main page showing all story types."""
    story_types = registry.get_all_story_types()
    return render_template('story_types.html', story_types=story_types)


@app.route('/story_type/<story_type_name>')
def story_type_detail(story_type_name):
    """Show details and subtypes for a specific story type."""
    story_type = registry.get_story_type(story_type_name)
    if not story_type:
        return redirect(url_for('index'))
    
    return render_template('subtypes.html', story_type=story_type)


@app.route('/subtype/<story_type_name>/<subtype_name>')
def subtype_detail(story_type_name, subtype_name):
    """Show details for a specific subtype."""
    story_type = registry.get_story_type(story_type_name)
    if not story_type:
        return redirect(url_for('index'))
    
    subtype = story_type.get_subtype(subtype_name)
    if not subtype:
        return redirect(url_for('story_type_detail', story_type_name=story_type_name))
    
    # Get story selections
    story = get_story_from_session()
    saved_selections = story.get_story_type_selection(story_type_name, subtype_name)
    
    # Add genre and sub-genre to saved selections for display
    if story.genre:
        saved_selections['genre_name'] = story.genre.name
    if story.sub_genre:
        saved_selections['sub_genre_name'] = story.sub_genre.name
    
    return render_template('subtype_detail.html', story_type=story_type, subtype=subtype, saved_selections=saved_selections)


@app.route('/subtype/<story_type_name>/<subtype_name>/update', methods=['POST'])
def update_story_selection(story_type_name, subtype_name):
    """Handle form submission for story element selections."""
    story_type = registry.get_story_type(story_type_name)
    if not story_type:
        return redirect(url_for('index'))
    
    subtype = story_type.get_subtype(subtype_name)
    if not subtype:
        return redirect(url_for('story_type_detail', story_type_name=story_type_name))
    
    # Get or create story from session
    story = get_story_from_session()
    
    # Update story selections using Story class
    key_theme = request.form.get('key_theme')
    core_arc = request.form.get('core_arc')
    
    story.set_story_type_selection(story_type_name, subtype_name, key_theme, core_arc)
    
    # Save story back to session
    save_story_to_session(story)
    
    flash('Your selections have been saved!', 'success')
    # Redirect to genre selection instead of staying on the same page
    return redirect(url_for('genre_selection'))


@app.route('/genre-selection')
def genre_selection():
    """Show genre selection page."""
    story = get_story_from_session()
    
    # Check if story has required data (story type selections)
    if not story.story_type_name or not story.subtype_name:
        flash('Please complete story type selection first.', 'error')
        return redirect(url_for('index'))
    
    genres = genre_registry.get_all_genres()
    return render_template('genre_selection.html', genres=genres, story=story)


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
        flash('Genre selected successfully!', 'success')
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
    
    sub_genres = story.get_available_sub_genres()
    return render_template('subgenre_selection.html', sub_genres=sub_genres, story=story)


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
        flash('Sub-genre selected successfully! Story complete!', 'success')
        # For now, redirect back to the original subtype page to show the complete story
        return redirect(url_for('subtype_detail', 
                              story_type_name=story.story_type_name, 
                              subtype_name=story.subtype_name))
    else:
        flash('Invalid sub-genre selection.', 'error')
        return redirect(url_for('subgenre_selection'))


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)