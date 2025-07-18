#!/usr/bin/env python3
"""
Demo script showing Story functionality

This script demonstrates how to create and use Story objects.
"""

from story import Story, StoryBuilder, StoryRegistry


def demo_story_creation():
    """Demo creating stories with the StoryBuilder."""
    print("=== Story Creation Demo ===\n")
    
    # Create a story builder
    builder = StoryBuilder()
    
    # Build a fantasy story
    print("Creating a fantasy story...")
    fantasy_story = (builder
                    .set_title("The Dragon's Heart")
                    .set_description("A young warrior must retrieve a magical artifact to save their kingdom")
                    .set_genre("Fantasy")
                    .set_sub_genre("High Fantasy")
                    .set_story_type("The Quest")
                    .set_story_subtype("Spiritual Quest")
                    .add_archetype("Chosen One")
                    .add_archetype("Wise Mentor")
                    .add_archetype("Loyal Companion")
                    .add_tag("magic")
                    .add_tag("adventure")
                    .set_notes("Inspired by classic fantasy literature")
                    .build())
    
    print(f"Created story: {fantasy_story}")
    print(f"Completion: {fantasy_story.completion_percentage:.1f}%")
    print(f"Is complete: {fantasy_story.is_complete}")
    print()
    
    # Build a sci-fi story
    print("Creating a sci-fi story...")
    scifi_story = (builder.reset()
                  .set_title("Neural Network")
                  .set_description("A hacker discovers a conspiracy in virtual reality")
                  .set_genre("Science Fiction")
                  .set_sub_genre("Cyberpunk")
                  .set_story_type("Overcoming the Monster")
                  .add_archetype("Anti-Hero")
                  .add_archetype("Femme Fatale")
                  .add_tag("technology")
                  .build())
    
    print(f"Created story: {scifi_story}")
    print(f"Completion: {scifi_story.completion_percentage:.1f}%")
    print(f"Is complete: {scifi_story.is_complete}")
    print()
    
    return fantasy_story, scifi_story


def demo_story_registry():
    """Demo managing stories with StoryRegistry."""
    print("=== Story Registry Demo ===\n")
    
    # Create stories
    fantasy_story, scifi_story = demo_story_creation()
    
    # Create a registry
    registry = StoryRegistry()
    registry.add_story(fantasy_story)
    registry.add_story(scifi_story)
    
    print(f"Total stories in registry: {len(registry.stories)}")
    print()
    
    # Search by genre
    fantasy_stories = registry.get_stories_by_genre("Fantasy")
    print(f"Fantasy stories: {len(fantasy_stories)}")
    for story in fantasy_stories:
        print(f"  - {story.title}")
    print()
    
    # Search by story type
    quest_stories = registry.get_stories_by_story_type("The Quest")
    print(f"Quest stories: {len(quest_stories)}")
    for story in quest_stories:
        print(f"  - {story.title}")
    print()
    
    # Search by archetype
    chosen_one_stories = registry.get_stories_by_archetype("Chosen One")
    print(f"Stories with 'Chosen One' archetype: {len(chosen_one_stories)}")
    for story in chosen_one_stories:
        print(f"  - {story.title}")
    print()
    
    # Get complete vs incomplete stories
    complete_stories = registry.get_complete_stories()
    incomplete_stories = registry.get_incomplete_stories()
    
    print(f"Complete stories: {len(complete_stories)}")
    print(f"Incomplete stories: {len(incomplete_stories)}")
    print()
    
    return registry


def demo_story_serialization():
    """Demo saving and loading stories."""
    print("=== Story Serialization Demo ===\n")
    
    # Create a registry with stories
    registry = demo_story_registry()
    
    # Save to file
    filename = "/tmp/demo_stories.json"
    registry.save_to_file(filename)
    print(f"Saved {len(registry.stories)} stories to {filename}")
    
    # Load from file
    new_registry = StoryRegistry()
    new_registry.load_from_file(filename)
    print(f"Loaded {len(new_registry.stories)} stories from {filename}")
    
    # Verify loaded stories
    for story in new_registry.stories:
        print(f"  - {story.title}: {story.completion_percentage:.1f}% complete")
    print()


def demo_story_builder_helpers():
    """Demo StoryBuilder helper methods."""
    print("=== Story Builder Helpers Demo ===\n")
    
    builder = StoryBuilder()
    
    # Show available genres
    print("Available genres:")
    for genre in builder.genre_registry.get_all_genres():
        print(f"  - {genre.name}")
    print()
    
    # Set genre and show available sub-genres
    builder.set_genre("Fantasy")
    print("Available sub-genres for Fantasy:")
    for sub_genre in builder.get_available_sub_genres():
        print(f"  - {sub_genre.name}")
    print()
    
    # Show available story types
    print("Available story types:")
    for story_type in builder.story_registry.get_all_story_types():
        print(f"  - {story_type.name}")
    print()
    
    # Set story type and show available subtypes
    builder.set_story_type("The Quest")
    print("Available subtypes for The Quest:")
    for subtype in builder.get_available_story_subtypes():
        print(f"  - {subtype.name}")
    print()
    
    # Show suggested archetypes for sub-genre
    builder.set_sub_genre("High Fantasy")
    print("Suggested archetypes for High Fantasy:")
    for archetype in builder.get_suggested_archetypes():
        print(f"  - {archetype.name}")
    print()


def main():
    """Run all demos."""
    print("Story Object Demo\n")
    print("This demo shows how to create and manage Story objects that back user choices.")
    print("=" * 70)
    print()
    
    demo_story_creation()
    demo_story_registry()
    demo_story_serialization()
    demo_story_builder_helpers()
    
    print("=" * 70)
    print("Demo complete! The Story object successfully backs user choices like:")
    print("- Genre and sub-genre selection")
    print("- Story type and subtype selection")
    print("- Character archetype selection")
    print("- Story metadata and notes")
    print("- Story completion tracking")
    print("- Story persistence (save/load)")
    print("- Story search and filtering")


if __name__ == "__main__":
    main()