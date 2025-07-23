#!/usr/bin/env python3
"""
Test script to reproduce the missing archetype issue in STORY_CONFIGURATION
"""

from story import Story

def test_missing_archetypes_in_story_configuration():
    """Test that protagonist_archetype and secondary_archetypes appear in STORY_CONFIGURATION"""
    # Create a story with basic selections including archetypes but no Character objects
    story = Story()
    story.story_type_name = 'The Quest'
    story.subtype_name = 'Epic Quest'
    story.set_genre('Fantasy')
    story.set_sub_genre('High Fantasy')
    story.set_writing_style('Epic')
    
    # Set the archetype fields that are used by the web UI
    story.set_protagonist_archetype('Chosen One')
    story.set_secondary_archetypes(['Wise Mentor', 'Loyal Companion'])
    
    # Verify the archetype fields are set
    assert story.protagonist_archetype is not None, "Protagonist archetype should be set"
    assert len(story.secondary_archetypes) == 2, "Secondary archetypes should be set"
    
    # Verify there are no Character objects (this is the current web UI state)
    assert len(story.characters) == 0, "No Character objects should exist"
    
    # Get the STORY_CONFIGURATION output
    config_text = story.to_prompt_text()
    print("=== STORY CONFIGURATION OUTPUT ===")
    print(config_text)
    print("=" * 50)
    
    # Check if archetype information is missing
    if "CHARACTER ARCHETYPES:" in config_text:
        print("✓ CHARACTER ARCHETYPES section found")
    else:
        print("✗ CHARACTER ARCHETYPES section missing")
    
    if "Chosen One" in config_text:
        print("✓ Protagonist archetype 'Chosen One' found in output")
    else:
        print("✗ Protagonist archetype 'Chosen One' MISSING from output")
    
    if "Wise Mentor" in config_text:
        print("✓ Secondary archetype 'Wise Mentor' found in output")
    else:
        print("✗ Secondary archetype 'Wise Mentor' MISSING from output")
    
    if "Loyal Companion" in config_text:
        print("✓ Secondary archetype 'Loyal Companion' found in output")
    else:
        print("✗ Secondary archetype 'Loyal Companion' MISSING from output")
    
    # The issue: protagonist_archetype and secondary_archetypes should appear in STORY_CONFIGURATION
    # but they don't when there are no Character objects
    return config_text

if __name__ == "__main__":
    test_missing_archetypes_in_story_configuration()