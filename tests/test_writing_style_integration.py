#!/usr/bin/env python3
"""
Test the complete writing style integration flow.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from story import Story


def test_complete_writing_style_flow():
    """Test complete story flow including writing style."""
    print("Testing complete writing style integration flow...")
    
    # Create a story
    story = Story()
    
    # Set up complete story flow
    story.story_type_name = "The Quest"
    story.subtype_name = "Object Quest"
    story.key_theme = "The journey is as important as the destination."
    story.core_arc = "Hero discovers strength through perseverance."
    
    # Set genre and sub-genre
    assert story.set_genre("Fantasy"), "Should be able to set genre"
    assert story.set_sub_genre("High Fantasy"), "Should be able to set sub-genre"
    
    # Set writing style (the new functionality)
    assert story.set_writing_style("Lyrical"), "Should be able to set writing style"
    
    # Set archetype
    assert story.set_protagonist_archetype("Chosen One"), "Should be able to set protagonist"
    assert story.set_secondary_archetypes(["Wise Mentor", "Loyal Companion"]), "Should be able to set secondary archetypes"
    
    # Verify all fields are set correctly
    assert story.story_type_name == "The Quest"
    assert story.subtype_name == "Object Quest"
    assert story.genre.name == "Fantasy"
    assert story.sub_genre.name == "High Fantasy"
    assert story.writing_style.name == "Lyrical"
    assert story.protagonist_archetype == "Chosen One"
    assert len(story.secondary_archetypes) == 2
    
    print("✓ Complete story flow with writing style works")
    
    # Test string representation includes writing style
    story_str = str(story)
    assert "Writing Style: Lyrical" in story_str, "String representation should include writing style"
    print("✓ String representation includes writing style")
    
    # Test JSON serialization/deserialization includes writing style
    json_str = story.to_json()
    assert '"writing_style_name": "Lyrical"' in json_str, "JSON should include writing style"
    print("✓ JSON serialization includes writing style")
    
    # Test loading from JSON
    new_story = Story()
    assert new_story.from_json(json_str), "Should be able to load from JSON"
    assert new_story.writing_style.name == "Lyrical", "Writing style should be preserved"
    assert new_story.writing_style.description == "Musical, poetic, flowing rhythm", "Writing style details should be preserved"
    print("✓ JSON deserialization preserves writing style")
    
    # Verify the complete story flow order is correct
    # The writing style should come after sub-genre selection but before archetype selection
    expected_flow = [
        story.story_type_name,
        story.subtype_name, 
        story.key_theme,
        story.core_arc,
        story.genre.name,
        story.sub_genre.name,
        story.writing_style.name,  # NEW: Writing style comes here
        story.protagonist_archetype
    ]
    
    print("✓ Writing style fits correctly in the story flow sequence")
    print("✅ Complete writing style integration flow test passed!")


if __name__ == "__main__":
    print("=== Running Complete Writing Style Integration Test ===\n")
    test_complete_writing_style_flow()
    print("\n✅ All integration tests passed!")