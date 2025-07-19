#!/usr/bin/env python3
"""
Demonstration of Story Types and SubTypes, plus Archetypes and Writing Styles

This script demonstrates how to use the story types, subtypes, archetypes, and writing styles classes.
"""

from story_types import StoryTypeRegistry
from archetype import ArchetypeRegistry
from style import StyleRegistry


def main():
    """Main demonstration function."""
    print("=== Story Types and SubTypes Demo ===\n")
    
    # Create registry
    registry = StoryTypeRegistry()
    
    # Show all story types
    print("Available Story Types:")
    for name in registry.list_story_types():
        print(f"  - {name}")
    print()
    
    # Demonstrate each story type
    for story_type in registry.get_all_story_types():
        print(f"📚 {story_type.name}")
        print(f"   Description: {story_type.description}")
        
        if story_type.examples:
            print(f"   Examples: {', '.join(story_type.examples)}")
        
        if story_type.narrative_rhythm:
            print(f"   Narrative Rhythm: {story_type.narrative_rhythm}")
        
        if story_type.key_theme:
            print(f"   Key Themes: {', '.join(story_type.key_theme)}")
        
        if story_type.emotional_arc:
            print(f"   Emotional Arc: {', '.join(story_type.emotional_arc)}")
        
        if story_type.common_elements:
            print(f"   Common Elements: {', '.join(story_type.common_elements)}")
        
        print(f"   Subtypes ({len(story_type.subtypes)}):")
        for subtype in story_type.subtypes:
            print(f"     • {subtype.name}: {subtype.description}")
            if subtype.examples:
                print(f"       Examples: {', '.join(subtype.examples)}")
        print()
    
    # Demonstrate specific lookups
    print("=== Specific Lookups ===")
    
    # Get a specific story type
    quest = registry.get_story_type("The Quest")
    if quest:
        print(f"Found: {quest.name}")
        
        # Get a specific subtype
        spiritual_quest = quest.get_subtype("Spiritual Quest")
        if spiritual_quest:
            print(f"Subtype: {spiritual_quest}")
    
    # Show tragedy emotional arc
    tragedy = registry.get_story_type("Tragedy")
    if tragedy:
        print(f"\nTragedy emotional arc: {', '.join(tragedy.emotional_arc)}")
    
    # === NEW ARCHETYPE DEMO ===
    print("\n=== Character Archetypes Demo ===")
    
    # Create archetype registry
    archetype_registry = ArchetypeRegistry()
    
    # Show archetype statistics
    all_archetypes = archetype_registry.get_all_archetypes()
    print(f"\nTotal archetypes available: {len(all_archetypes)}")
    
    # Show some example archetypes
    print("\nSample Character Archetypes:")
    sample_names = ["Chosen One", "Wise Mentor", "Anti-Hero", "Femme Fatale", "Reluctant Hero"]
    for name in sample_names:
        archetype = archetype_registry.get_archetype(name)
        if archetype:
            print(f"  🎭 {archetype}")
    
    # Demonstrate search functionality
    print("\n=== Archetype Search Demo ===")
    hero_archetypes = archetype_registry.search_archetypes("hero")
    print(f"Found {len(hero_archetypes)} hero-related archetypes:")
    for archetype in hero_archetypes[:5]:  # Show first 5
        print(f"  - {archetype.name}: {archetype.description}")
    
    detective_archetypes = archetype_registry.search_archetypes("detective")
    print(f"\nFound {len(detective_archetypes)} detective-related archetypes:")
    for archetype in detective_archetypes:
        print(f"  - {archetype.name}: {archetype.description}")
    
    # === NEW WRITING STYLES DEMO ===
    print("\n=== Writing Styles Demo ===")
    
    # Create style registry
    style_registry = StyleRegistry()
    
    # Show style statistics
    all_styles = style_registry.get_all_styles()
    print(f"\nTotal writing styles available: {len(all_styles)}")
    
    # Show all writing styles
    print("\nAll Writing Styles:")
    for style in all_styles:
        print(f"  ✍️  {style.name}: {style.description}")
    
    # Demonstrate specific style lookup
    print("\n=== Style Details Demo ===")
    sample_styles = ["Concise", "Lyrical", "Experimental", "Satirical"]
    for style_name in sample_styles:
        style = style_registry.get_style(style_name)
        if style:
            print(f"\n📝 {style.name}")
            print(f"   Description: {style.description}")
            print(f"   Characteristics:")
            for char in style.characteristics:
                print(f"     • {char}")
            print(f"   Examples: {', '.join(style.examples)}")
    
    # Demonstrate style search functionality
    print("\n=== Style Search Demo ===")
    emotional_styles = style_registry.search_styles("emotional")
    print(f"Found {len(emotional_styles)} emotional-related styles:")
    for style in emotional_styles:
        print(f"  - {style.name}: {style.description}")
    
    humor_styles = style_registry.search_styles("humor")
    print(f"\nFound {len(humor_styles)} humor-related styles:")
    for style in humor_styles:
        print(f"  - {style.name}: {style.description}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()