#!/usr/bin/env python3
"""
Flask web application for Story Types and SubTypes

This Flask app provides a web interface to explore the seven classical story types
and their subtypes.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from story_types import StoryTypeRegistry

app = Flask(__name__)
app.secret_key = 'kraitif_story_selection_key'  # For session management

# Initialize the story types registry
registry = StoryTypeRegistry()

# Custom Jinja2 filter for formatting emotional arc as arrows
@app.template_filter('arrow_format')
def arrow_format(arc_list):
    """Format a list as arrow-separated progression."""
    if not arc_list or not isinstance(arc_list, list):
        return ""
    return " → ".join(arc_list)


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
    
    return render_template('subtype_detail.html', story_type=story_type, subtype=subtype)


@app.route('/subtype/<story_type_name>/<subtype_name>/update', methods=['POST'])
def update_story_selection(story_type_name, subtype_name):
    """Handle form submission for story element selections."""
    story_type = registry.get_story_type(story_type_name)
    if not story_type:
        return redirect(url_for('index'))
    
    subtype = story_type.get_subtype(subtype_name)
    if not subtype:
        return redirect(url_for('story_type_detail', story_type_name=story_type_name))
    
    # Initialize session storage for this subtype if not exists
    session_key = f"{story_type_name}_{subtype_name}"
    if 'story_selections' not in session:
        session['story_selections'] = {}
    
    # Store the selected values
    selections = {}
    if 'key_theme' in request.form:
        selections['key_theme'] = request.form['key_theme']
    if 'key_moment' in request.form:
        selections['key_moment'] = request.form['key_moment']
    if 'core_arc' in request.form:
        selections['core_arc'] = request.form['core_arc']
    
    session['story_selections'][session_key] = selections
    session.modified = True
    
    flash('Your selections have been saved!', 'success')
    return redirect(url_for('subtype_detail', story_type_name=story_type_name, subtype_name=subtype_name))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)