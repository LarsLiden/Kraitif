#!/usr/bin/env python3
"""
Flask web application for Story Types and SubTypes

This Flask app provides a web interface to explore the seven classical story types
and their subtypes, and to create and manage stories.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from story_types import StoryTypeRegistry
from genre import GenreRegistry
from archetype import ArchetypeRegistry
from story import Story, StoryBuilder, StoryRegistry
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize the registries
story_type_registry = StoryTypeRegistry()
genre_registry = GenreRegistry()
archetype_registry = ArchetypeRegistry()
story_registry = StoryRegistry()

# Initialize story builder
story_builder = StoryBuilder()


@app.route('/')
def index():
    """Main page showing all story types and user stories."""
    story_types = story_type_registry.get_all_story_types()
    user_stories = story_registry.get_complete_stories()[:5]  # Show last 5 complete stories
    return render_template('index.html', 
                         story_types=story_types, 
                         user_stories=user_stories)


@app.route('/story_types')
def story_types():
    """Page showing all story types."""
    story_types = story_type_registry.get_all_story_types()
    return render_template('story_types.html', story_types=story_types)


@app.route('/story_type/<story_type_name>')
def story_type_detail(story_type_name):
    """Show details and subtypes for a specific story type."""
    story_type = story_type_registry.get_story_type(story_type_name)
    if not story_type:
        return redirect(url_for('story_types'))
    
    return render_template('subtypes.html', story_type=story_type)


@app.route('/subtype/<story_type_name>/<subtype_name>')
def subtype_detail(story_type_name, subtype_name):
    """Show details for a specific subtype."""
    story_type = story_type_registry.get_story_type(story_type_name)
    if not story_type:
        return redirect(url_for('story_types'))
    
    subtype = story_type.get_subtype(subtype_name)
    if not subtype:
        return redirect(url_for('story_type_detail', story_type_name=story_type_name))
    
    return render_template('subtype_detail.html', story_type=story_type, subtype=subtype)


@app.route('/create_story')
def create_story():
    """Show story creation form."""
    genres = genre_registry.get_all_genres()
    story_types = story_type_registry.get_all_story_types()
    archetypes = archetype_registry.get_all_archetypes()
    
    return render_template('create_story.html', 
                         genres=genres, 
                         story_types=story_types, 
                         archetypes=archetypes)


@app.route('/create_story', methods=['POST'])
def create_story_post():
    """Process story creation form."""
    try:
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        genre_name = request.form.get('genre', '').strip()
        sub_genre_name = request.form.get('sub_genre', '').strip()
        story_type_name = request.form.get('story_type', '').strip()
        story_subtype_name = request.form.get('story_subtype', '').strip()
        archetype_names = request.form.getlist('archetypes')
        notes = request.form.get('notes', '').strip()
        
        # Validate required fields
        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('create_story'))
        
        # Build the story
        builder = StoryBuilder()
        builder.set_title(title)
        
        if description:
            builder.set_description(description)
        
        if genre_name:
            builder.set_genre(genre_name)
        
        if sub_genre_name:
            builder.set_sub_genre(sub_genre_name)
        
        if story_type_name:
            builder.set_story_type(story_type_name)
        
        if story_subtype_name:
            builder.set_story_subtype(story_subtype_name)
        
        for archetype_name in archetype_names:
            builder.add_archetype(archetype_name)
        
        if notes:
            builder.set_notes(notes)
        
        # Create the story
        story = builder.build()
        
        # Add to registry
        story_registry.add_story(story)
        
        flash(f'Story "{title}" created successfully!', 'success')
        return redirect(url_for('view_story', story_index=len(story_registry.stories) - 1))
        
    except Exception as e:
        flash(f'Error creating story: {str(e)}', 'error')
        return redirect(url_for('create_story'))


@app.route('/stories')
def list_stories():
    """List all user stories."""
    stories = story_registry.stories
    return render_template('list_stories.html', stories=stories)


@app.route('/story/<int:story_index>')
def view_story(story_index):
    """View a specific story."""
    if story_index < 0 or story_index >= len(story_registry.stories):
        flash('Story not found', 'error')
        return redirect(url_for('list_stories'))
    
    story = story_registry.stories[story_index]
    return render_template('view_story.html', story=story, story_index=story_index)


@app.route('/story/<int:story_index>/edit')
def edit_story(story_index):
    """Edit a story."""
    if story_index < 0 or story_index >= len(story_registry.stories):
        flash('Story not found', 'error')
        return redirect(url_for('list_stories'))
    
    story = story_registry.stories[story_index]
    genres = genre_registry.get_all_genres()
    story_types = story_type_registry.get_all_story_types()
    archetypes = archetype_registry.get_all_archetypes()
    
    return render_template('edit_story.html', 
                         story=story, 
                         story_index=story_index,
                         genres=genres, 
                         story_types=story_types, 
                         archetypes=archetypes)


@app.route('/story/<int:story_index>/edit', methods=['POST'])
def edit_story_post(story_index):
    """Process story edit form."""
    if story_index < 0 or story_index >= len(story_registry.stories):
        flash('Story not found', 'error')
        return redirect(url_for('list_stories'))
    
    try:
        story = story_registry.stories[story_index]
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        genre_name = request.form.get('genre', '').strip()
        sub_genre_name = request.form.get('sub_genre', '').strip()
        story_type_name = request.form.get('story_type', '').strip()
        story_subtype_name = request.form.get('story_subtype', '').strip()
        archetype_names = request.form.getlist('archetypes')
        notes = request.form.get('notes', '').strip()
        
        # Validate required fields
        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('edit_story', story_index=story_index))
        
        # Update the story
        story.title = title
        story.description = description
        story.notes = notes
        
        # Update genre
        if genre_name:
            genre = genre_registry.get_genre(genre_name)
            story.genre = genre
            # Update sub-genre
            if sub_genre_name and genre:
                sub_genre = genre.get_subgenre(sub_genre_name)
                story.sub_genre = sub_genre
            else:
                story.sub_genre = None
        else:
            story.genre = None
            story.sub_genre = None
        
        # Update story type
        if story_type_name:
            story_type = story_type_registry.get_story_type(story_type_name)
            story.story_type = story_type
            # Update story subtype
            if story_subtype_name and story_type:
                story_subtype = story_type.get_subtype(story_subtype_name)
                story.story_subtype = story_subtype
            else:
                story.story_subtype = None
        else:
            story.story_type = None
            story.story_subtype = None
        
        # Update archetypes
        story.archetypes = []
        for archetype_name in archetype_names:
            archetype = archetype_registry.get_archetype(archetype_name)
            if archetype:
                story.add_archetype(archetype)
        
        flash(f'Story "{title}" updated successfully!', 'success')
        return redirect(url_for('view_story', story_index=story_index))
        
    except Exception as e:
        flash(f'Error updating story: {str(e)}', 'error')
        return redirect(url_for('edit_story', story_index=story_index))


@app.route('/story/<int:story_index>/delete', methods=['POST'])
def delete_story(story_index):
    """Delete a story."""
    if story_index < 0 or story_index >= len(story_registry.stories):
        flash('Story not found', 'error')
        return redirect(url_for('list_stories'))
    
    story = story_registry.stories[story_index]
    title = story.title
    
    story_registry.remove_story(story)
    flash(f'Story "{title}" deleted successfully!', 'success')
    return redirect(url_for('list_stories'))


@app.route('/api/sub_genres/<genre_name>')
def get_sub_genres(genre_name):
    """API endpoint to get sub-genres for a genre."""
    genre = genre_registry.get_genre(genre_name)
    if not genre:
        return {'sub_genres': []}
    
    sub_genres = [{'name': sg.name, 'plot': sg.plot} for sg in genre.subgenres]
    return {'sub_genres': sub_genres}


@app.route('/api/story_subtypes/<story_type_name>')
def get_story_subtypes(story_type_name):
    """API endpoint to get story subtypes for a story type."""
    story_type = story_type_registry.get_story_type(story_type_name)
    if not story_type:
        return {'subtypes': []}
    
    subtypes = [{'name': st.name, 'description': st.description} for st in story_type.subtypes]
    return {'subtypes': subtypes}


@app.route('/api/suggested_archetypes/<genre_name>/<sub_genre_name>')
def get_suggested_archetypes(genre_name, sub_genre_name):
    """API endpoint to get suggested archetypes for a sub-genre."""
    genre = genre_registry.get_genre(genre_name)
    if not genre:
        return {'archetypes': []}
    
    sub_genre = genre.get_subgenre(sub_genre_name)
    if not sub_genre:
        return {'archetypes': []}
    
    suggested = []
    for archetype_name in getattr(sub_genre, 'archetypes', []):
        archetype = archetype_registry.get_archetype(archetype_name)
        if archetype:
            suggested.append({'name': archetype.name, 'description': archetype.description})
    
    return {'archetypes': suggested}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)