#!/usr/bin/env python3
"""
Flask web application for Story Types and SubTypes

This Flask app provides a web interface to explore the seven classical story types
and their subtypes.
"""

from flask import Flask, render_template, request, redirect, url_for
from story_types import StoryTypeRegistry

app = Flask(__name__)

# Initialize the story types registry
registry = StoryTypeRegistry()


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)