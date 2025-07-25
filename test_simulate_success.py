#!/usr/bin/env python3
"""
Add a test route to simulate successful chapter generation
"""

def add_test_route_to_app():
    """Add a test route to simulate successful chapter generation."""
    
    route_code = '''
@app.route('/test-simulate-chapter-success/<int:chapter_number>')
def test_simulate_chapter_success(chapter_number):
    """Test route to simulate successful chapter generation."""
    from objects.continuity_state import ContinuityState
    from objects.continuity_character import ContinuityCharacter
    
    story = get_story_from_session()
    
    # Check if we have the required data
    if not story.chapters:
        return jsonify({'error': 'No chapters in the story.'}), 400
    
    # Check if the requested chapter number exists in the story
    existing_chapter = story.get_chapter(chapter_number)
    if not existing_chapter:
        return jsonify({'error': f'Chapter {chapter_number} does not exist in the story plan.'}), 400
    
    # Check if chapter already has chapter_text (already generated)
    if existing_chapter.chapter_text:
        return jsonify({'error': f'Chapter {chapter_number} has already been generated.'}), 400
    
    # Simulate successful generation
    sample_chapter_text = f"""In Chapter {chapter_number}, our heroes face new challenges as their quest continues.

The party found themselves at a crossroads, both literally and figuratively. The ancient map that Aldric carried showed two possible paths ahead: one through the Whispering Woods, known for its deceptive illusions, and another across the Barren Reaches, where nothing grew and few travelers returned.

Lyra studied both routes with growing concern. Her newly awakened abilities allowed her to sense the magical disturbances ahead - the corruption was spreading faster than they had anticipated.

"We must choose quickly," Kael urged, his hand resting on his sword hilt. "The longer we delay, the stronger the darkness grows."

The decision would shape the rest of their journey, and Lyra felt the weight of leadership settling upon her shoulders."""

    sample_summary = f"Chapter {chapter_number} summary - The party faces critical decisions as their quest progresses."
    
    # Create sample continuity state
    continuity_state = ContinuityState(
        characters=[
            ContinuityCharacter(
                name="Lyra",
                current_location="Crossroads near Millhaven",
                status="Confident but concerned about the spreading corruption",
                inventory=["Ancient Map Fragment", "Glowing Runes (on skin)"]
            ),
            ContinuityCharacter(
                name="Aldric", 
                current_location="Crossroads near Millhaven",
                status="Thoughtful and strategic, consulting ancient texts",
                inventory=["Ancient Tome", "Staff of Enlightenment", "Travel Pack"]
            ),
            ContinuityCharacter(
                name="Kael",
                current_location="Crossroads near Millhaven", 
                status="Alert and ready for action, concerned about delays",
                inventory=["Knight's Sword", "Tattered Banner", "Travel Supplies"]
            )
        ],
        objects=[],
        locations_visited=["Thornfield", "Corrupted Countryside", "Millhaven", "Crossroads"],
        open_plot_threads=[]
    )
    
    # Update the existing chapter with generated content
    existing_chapter.chapter_text = sample_chapter_text
    existing_chapter.summary = sample_summary
    existing_chapter.continuity_state = continuity_state
    
    # Save to session
    save_story_to_session(story)
    
    return jsonify({
        'success': True,
        'chapter': existing_chapter.to_dict(),
        'redirect_url': url_for('chapter_detail', chapter_number=chapter_number),
        'message': f'Successfully generated Chapter {chapter_number} (simulated)'
    })
'''
    
    with open('/home/runner/work/Kraitif/Kraitif/app.py', 'r') as f:
        content = f.read()
    
    # Add the route before the if __name__ == '__main__': line
    insertion_point = content.find("if __name__ == '__main__':")
    if insertion_point != -1:
        new_content = content[:insertion_point] + route_code + "\n\n" + content[insertion_point:]
        
        with open('/home/runner/work/Kraitif/Kraitif/app.py', 'w') as f:
            f.write(new_content)
        
        print("Added test route to app.py")
    else:
        print("Could not find insertion point in app.py")

if __name__ == "__main__":
    add_test_route_to_app()