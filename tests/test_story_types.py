#!/usr/bin/env python3
"""
Basic tests for Story Types and SubTypes

This script provides basic validation tests for the story types implementation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from story_types import StoryTypeRegistry, StoryType, StorySubType
from archetype import ArchetypeRegistry, Archetype
from genre import GenreRegistry, Genre, SubGenre, GenreEnum, SubGenreEnum
from style import StyleRegistry, Style, StyleEnum


def test_story_type_registry():
    """Test the StoryTypeRegistry functionality."""
    print("Testing StoryTypeRegistry...")
    
    registry = StoryTypeRegistry()
    
    # Test that all 7 story types are available
    story_types = registry.get_all_story_types()
    assert len(story_types) == 7, f"Expected 7 story types, got {len(story_types)}"
    
    # Test that story type names are correct
    expected_names = [
        "Overcoming the Monster",
        "Rags to Riches", 
        "The Quest",
        "Voyage and Return",
        "Comedy",
        "Tragedy",
        "Rebirth"
    ]
    
    actual_names = registry.list_story_types()
    for name in expected_names:
        assert name in actual_names, f"Missing story type: {name}"
    
    # Test lookup by name
    quest = registry.get_story_type("The Quest")
    assert quest is not None, "Could not find The Quest story type"
    assert quest.name == "The Quest", f"Expected 'The Quest', got '{quest.name}'"
    
    # Test case-insensitive lookup
    quest2 = registry.get_story_type("the quest")
    assert quest2 is not None, "Case-insensitive lookup failed"
    
    # Test lookup with underscores
    quest3 = registry.get_story_type("the_quest")
    assert quest3 is not None, "Underscore lookup failed"
    
    print("✓ StoryTypeRegistry tests passed")


def test_story_subtypes():
    """Test that each story type has the correct subtypes."""
    print("Testing Story SubTypes...")
    
    registry = StoryTypeRegistry()
    
    # Test Overcoming the Monster subtypes
    monster = registry.get_story_type("Overcoming the Monster")
    assert len(monster.subtypes) == 3, f"Expected 3 subtypes for Overcoming the Monster, got {len(monster.subtypes)}"
    assert len(monster.examples) >= 1, "Overcoming the Monster should have examples"
    assert "Beowulf" in monster.examples or "Jaws" in monster.examples, "Should have Beowulf or Jaws as examples"
    
    predator = monster.get_subtype("Predator")
    assert predator is not None, "Could not find Predator subtype"
    assert "Jaws" in predator.examples, "Jaws should be in Predator examples"
    
    # Test Rags to Riches subtypes
    rags = registry.get_story_type("Rags to Riches")
    assert len(rags.subtypes) == 3, f"Expected 3 subtypes for Rags to Riches, got {len(rags.subtypes)}"
    assert len(rags.examples) >= 1, "Rags to Riches should have examples"
    assert "True worth comes from character, not wealth or status." in rags.key_theme, "Should have character theme"
    
    # Test The Quest subtypes
    quest = registry.get_story_type("The Quest")
    assert len(quest.subtypes) == 3, f"Expected 3 subtypes for The Quest, got {len(quest.subtypes)}"
    assert len(quest.examples) >= 1, "The Quest should have examples"
    assert "Loyal companions" in quest.common_elements, "Loyal companions should be in Quest common elements"
    
    # Test Voyage and Return
    voyage = registry.get_story_type("Voyage and Return")
    assert len(voyage.examples) >= 1, "Voyage and Return should have examples"
    assert "Curiosity" in voyage.emotional_arc, "Curiosity should be in emotional arc"
    
    # Test Comedy subtypes
    comedy = registry.get_story_type("Comedy")
    assert len(comedy.subtypes) == 3, f"Expected 3 subtypes for Comedy, got {len(comedy.subtypes)}"
    assert len(comedy.examples) >= 1, "Comedy should have examples"
    
    # Test Tragedy subtypes  
    tragedy = registry.get_story_type("Tragedy")
    assert len(tragedy.examples) >= 1, "Tragedy should have examples"
    assert "Catharsis" in tragedy.emotional_arc, "Catharsis should be in emotional arc"
    
    # Test Rebirth subtypes
    rebirth = registry.get_story_type("Rebirth")
    assert len(rebirth.examples) >= 1, "Rebirth should have examples"
    assert "Transformation begins with self-awareness." in rebirth.key_theme, "Should have transformation theme"
    
    print("✓ Story SubTypes tests passed")


def test_story_subtype_class():
    """Test the StorySubType class."""
    print("Testing StorySubType class...")
    
    # Create a subtype
    subtype = StorySubType(
        name="Test Subtype",
        description="A test subtype",
        examples=["Example 1", "Example 2"]
    )
    
    assert subtype.name == "Test Subtype"
    assert subtype.description == "A test subtype"
    assert len(subtype.examples) == 2
    assert "Example 1" in subtype.examples
    
    # Test string representation
    str_repr = str(subtype)
    assert "Test Subtype" in str_repr
    assert "A test subtype" in str_repr
    
    print("✓ StorySubType class tests passed")


def test_story_type_class():
    """Test the StoryType class."""
    print("Testing StoryType class...")
    
    # Create a story type
    story_type = StoryType(
        name="Test Story Type",
        description="A test story type",
        examples=["Example Work 1", "Example Work 2"]
    )
    
    # Test examples
    assert len(story_type.examples) == 2
    assert "Example Work 1" in story_type.examples
    assert "Example Work 2" in story_type.examples
    
    # Add a subtype
    subtype = StorySubType("Test Sub", "Test description")
    story_type.add_subtype(subtype)
    
    assert len(story_type.subtypes) == 1
    assert story_type.get_subtype("Test Sub") is not None
    assert story_type.get_subtype("nonexistent") is None
    
    # Test case-insensitive lookup
    assert story_type.get_subtype("test sub") is not None
    
    print("✓ StoryType class tests passed")


def test_archetype_registry():
    """Test the ArchetypeRegistry functionality."""
    print("Testing ArchetypeRegistry...")
    
    registry = ArchetypeRegistry()
    
    # Test that archetypes are loaded
    archetypes = registry.get_all_archetypes()
    assert len(archetypes) > 0, f"Expected archetypes to be loaded, got {len(archetypes)}"
    
    # Test that we have expected number of archetypes (should be around 108)
    assert len(archetypes) >= 100, f"Expected at least 100 archetypes, got {len(archetypes)}"
    
    # Test lookup by name
    chosen_one = registry.get_archetype("Chosen One")
    assert chosen_one is not None, "Could not find Chosen One archetype"
    assert chosen_one.name == "Chosen One", f"Expected 'Chosen One', got '{chosen_one.name}'"
    
    # Test case-insensitive lookup
    chosen_one2 = registry.get_archetype("chosen one")
    assert chosen_one2 is not None, "Case-insensitive lookup failed"
    assert chosen_one2.name == "Chosen One", "Case-insensitive lookup returned wrong archetype"
    
    # Test lookup with underscores
    chosen_one3 = registry.get_archetype("chosen_one")
    assert chosen_one3 is not None, "Underscore lookup failed"
    
    # Test search functionality
    hero_archetypes = registry.search_archetypes("hero")
    assert len(hero_archetypes) > 0, "Should find hero-related archetypes"
    
    # Test list archetype names
    names = registry.list_archetype_names()
    assert len(names) == len(archetypes), "Names list should match archetypes count"
    assert "Chosen One" in names, "Should find Chosen One in names list"
    
    print("✓ ArchetypeRegistry tests passed")


def test_archetype_class():
    """Test the Archetype class."""
    print("Testing Archetype class...")
    
    # Create an archetype
    archetype = Archetype(
        name="Test Archetype",
        description="A test archetype for validation"
    )
    
    assert archetype.name == "Test Archetype"
    assert archetype.description == "A test archetype for validation"
    
    # Test string representation
    str_repr = str(archetype)
    assert "Test Archetype" in str_repr
    assert "A test archetype for validation" in str_repr
    
    print("✓ Archetype class tests passed")


def test_genre_registry():
    """Test the GenreRegistry functionality."""
    print("Testing GenreRegistry...")
    
    registry = GenreRegistry()
    
    # Test that all 15 genres are available
    genres = registry.get_all_genres()
    assert len(genres) == 15, f"Expected 15 genres, got {len(genres)}"
    
    # Test that genre names are correct
    expected_names = [
        "Fantasy", "Science Fiction", "Western", "Mystery", "Thriller", 
        "Horror", "Romance", "Comedy", "Drama", "Adventure", 
        "Historical", "Crime", "Action", "Documentary", "Musical"
    ]
    
    actual_names = registry.list_genres()
    for name in expected_names:
        assert name in actual_names, f"Missing genre: {name}"
    
    # Test lookup by name
    fantasy = registry.get_genre("Fantasy")
    assert fantasy is not None, "Could not find Fantasy genre"
    assert fantasy.name == "Fantasy", f"Expected 'Fantasy', got '{fantasy.name}'"
    
    # Test case-insensitive lookup
    fantasy2 = registry.get_genre("fantasy")
    assert fantasy2 is not None, "Case-insensitive lookup failed"
    
    # Test lookup with underscores
    sci_fi = registry.get_genre("science_fiction")
    assert sci_fi is not None, "Underscore lookup failed"
    
    print("✓ GenreRegistry tests passed")


def test_genre_subgenres():
    """Test that each genre has the correct sub-genres."""
    print("Testing Genre SubGenres...")
    
    registry = GenreRegistry()
    
    # Test Fantasy sub-genres
    fantasy = registry.get_genre("Fantasy")
    assert len(fantasy.subgenres) == 7, f"Expected 7 sub-genres for Fantasy, got {len(fantasy.subgenres)}"
    
    high_fantasy = fantasy.get_subgenre("High Fantasy")
    assert high_fantasy is not None, "Could not find High Fantasy sub-genre"
    assert "The Lord of the Rings" in high_fantasy.examples, "The Lord of the Rings should be in High Fantasy examples"
    assert "Chosen One" in high_fantasy.archetypes, "Chosen One should be in High Fantasy archetypes"
    
    # Test Science Fiction sub-genres
    sci_fi = registry.get_genre("Science Fiction")
    assert len(sci_fi.subgenres) == 6, f"Expected 6 sub-genres for Science Fiction, got {len(sci_fi.subgenres)}"
    
    cyberpunk = sci_fi.get_subgenre("Cyberpunk")
    assert cyberpunk is not None, "Could not find Cyberpunk sub-genre"
    assert "Blade Runner" in cyberpunk.examples, "Blade Runner should be in Cyberpunk examples"
    
    # Test Western sub-genres
    western = registry.get_genre("Western")
    assert len(western.subgenres) == 4, f"Expected 4 sub-genres for Western, got {len(western.subgenres)}"
    
    # Test Mystery sub-genres
    mystery = registry.get_genre("Mystery")
    assert len(mystery.subgenres) == 4, f"Expected 4 sub-genres for Mystery, got {len(mystery.subgenres)}"
    
    # Test Horror sub-genres
    horror = registry.get_genre("Horror")
    assert len(horror.subgenres) == 5, f"Expected 5 sub-genres for Horror, got {len(horror.subgenres)}"
    
    print("✓ Genre SubGenres tests passed")


def test_subgenre_class():
    """Test the SubGenre class."""
    print("Testing SubGenre class...")
    
    # Create a sub-genre
    subgenre = SubGenre(
        name="Test SubGenre",
        archetypes=["Hero", "Villain"],
        plot="Good vs Evil",
        examples=["Example 1", "Example 2"]
    )
    
    assert subgenre.name == "Test SubGenre"
    assert subgenre.plot == "Good vs Evil"
    assert len(subgenre.archetypes) == 2
    assert len(subgenre.examples) == 2
    assert "Hero" in subgenre.archetypes
    assert "Example 1" in subgenre.examples
    
    # Test string representation
    str_repr = str(subgenre)
    assert "Test SubGenre" in str_repr
    assert "Good vs Evil" in str_repr
    
    print("✓ SubGenre class tests passed")


def test_genre_class():
    """Test the Genre class."""
    print("Testing Genre class...")
    
    # Create a genre
    genre = Genre(name="Test Genre")
    
    assert genre.name == "Test Genre"
    assert len(genre.subgenres) == 0
    
    # Add a sub-genre
    subgenre = SubGenre(name="Test Sub", plot="Test plot")
    genre.add_subgenre(subgenre)
    
    assert len(genre.subgenres) == 1
    assert genre.get_subgenre("Test Sub") is not None
    assert genre.get_subgenre("nonexistent") is None
    
    # Test case-insensitive lookup
    assert genre.get_subgenre("test sub") is not None
    
    # Test string representation
    str_repr = str(genre)
    assert "Test Genre" in str_repr
    assert "1 sub-genres" in str_repr
    
    print("✓ Genre class tests passed")


def test_genre_enum():
    """Test the GenreEnum."""
    print("Testing GenreEnum...")
    
    # Test that all expected genres are present
    assert GenreEnum.FANTASY.value == "Fantasy"
    assert GenreEnum.SCIENCE_FICTION.value == "Science Fiction"
    assert GenreEnum.HORROR.value == "Horror"
    assert GenreEnum.ROMANCE.value == "Romance"
    assert GenreEnum.DOCUMENTARY.value == "Documentary"
    
    # Test that we have the correct number of genres
    genres = list(GenreEnum)
    assert len(genres) == 15, f"Expected 15 genres in enum, got {len(genres)}"
    
    print("✓ GenreEnum tests passed")


def test_subgenre_enum():
    """Test the SubGenreEnum."""
    print("Testing SubGenreEnum...")
    
    # Test that some expected sub-genres are present
    assert SubGenreEnum.HIGH_FANTASY.value == "High Fantasy"
    assert SubGenreEnum.CYBERPUNK.value == "Cyberpunk"
    assert SubGenreEnum.CLASSIC_WESTERN.value == "Classic Western"
    assert SubGenreEnum.PSYCHOLOGICAL_HORROR.value == "Psychological Horror"
    
    # Test that we have a reasonable number of sub-genres
    subgenres = list(SubGenreEnum)
    assert len(subgenres) > 60, f"Expected more than 60 sub-genres in enum, got {len(subgenres)}"
    
    print("✓ SubGenreEnum tests passed")


def test_style_registry():
    """Test the StyleRegistry functionality."""
    print("Testing StyleRegistry...")
    
    registry = StyleRegistry()
    
    # Test that all 15 styles are available
    styles = registry.get_all_styles()
    assert len(styles) == 15, f"Expected 15 styles, got {len(styles)}"
    
    # Test that style names are correct
    expected_names = [
        "Concise", "Lyrical", "Analytical", "Whimsical", "Descriptive",
        "Conversational", "Philosophical", "Satirical", "Suspenseful", 
        "Romantic", "Detached", "Experimental", "Journalistic", 
        "Reflective", "Persuasive"
    ]
    
    actual_names = registry.list_styles()
    for name in expected_names:
        assert name in actual_names, f"Missing style: {name}"
    
    # Test lookup by name
    concise = registry.get_style("Concise")
    assert concise is not None, "Could not find Concise style"
    assert concise.name == "Concise", f"Expected 'Concise', got '{concise.name}'"
    
    # Test case-insensitive lookup
    concise2 = registry.get_style("concise")
    assert concise2 is not None, "Case-insensitive lookup failed"
    
    # Test lookup with underscores
    concise3 = registry.get_style("concise")
    assert concise3 is not None, "Underscore lookup failed"
    
    print("✓ StyleRegistry tests passed")


def test_style_properties():
    """Test that each style has the correct properties."""
    print("Testing Style Properties...")
    
    registry = StyleRegistry()
    
    # Test Concise style
    concise = registry.get_style("Concise")
    assert concise.description == "Minimalist, efficient, no wasted words", "Concise description incorrect"
    assert len(concise.characteristics) >= 3, f"Expected at least 3 characteristics for Concise, got {len(concise.characteristics)}"
    assert len(concise.examples) >= 1, "Concise should have examples"
    assert "Ernest Hemingway" in concise.examples, "Ernest Hemingway should be in Concise examples"
    
    # Test Lyrical style
    lyrical = registry.get_style("Lyrical")
    assert lyrical.description == "Musical, poetic, flowing rhythm", "Lyrical description incorrect"
    assert "Toni Morrison" in lyrical.examples, "Toni Morrison should be in Lyrical examples"
    assert "Gabriel García Márquez" in lyrical.examples, "Gabriel García Márquez should be in Lyrical examples"
    
    # Test Analytical style
    analytical = registry.get_style("Analytical")
    assert analytical.description == "Logical, structured, evidence-based", "Analytical description incorrect"
    assert "George Orwell" in analytical.examples, "George Orwell should be in Analytical examples"
    
    # Test Whimsical style
    whimsical = registry.get_style("Whimsical")
    assert whimsical.description == "Playful, imaginative, quirky", "Whimsical description incorrect"
    assert "Roald Dahl" in whimsical.examples, "Roald Dahl should be in Whimsical examples"
    assert "Douglas Adams" in whimsical.examples, "Douglas Adams should be in Whimsical examples"
    
    # Test Descriptive style
    descriptive = registry.get_style("Descriptive")
    assert descriptive.description == "Rich sensory detail, vivid imagery", "Descriptive description incorrect"
    assert "Virginia Woolf" in descriptive.examples, "Virginia Woolf should be in Descriptive examples"
    
    # Test search functionality
    search_results = registry.search_styles("humor")
    humor_found = any("humor" in style.characteristics for style in search_results if style.characteristics)
    assert humor_found or len(search_results) > 0, "Should find styles related to humor"
    
    print("✓ Style Properties tests passed")


def test_style_class():
    """Test the Style class."""
    print("Testing Style class...")
    
    # Create a style
    style = Style(
        name="Test Style",
        description="A test writing style",
        characteristics=["Clear", "Direct", "Simple"],
        examples=["Example Author 1", "Example Author 2"]
    )
    
    assert style.name == "Test Style"
    assert style.description == "A test writing style"
    assert len(style.characteristics) == 3
    assert len(style.examples) == 2
    assert "Clear" in style.characteristics
    assert "Example Author 1" in style.examples
    
    # Test string representation
    str_repr = str(style)
    assert "Test Style" in str_repr
    assert "A test writing style" in str_repr
    
    print("✓ Style class tests passed")


def test_style_enum():
    """Test the StyleEnum."""
    print("Testing StyleEnum...")
    
    # Test that all expected styles are present
    assert StyleEnum.CONCISE.value == "Concise"
    assert StyleEnum.LYRICAL.value == "Lyrical"
    assert StyleEnum.ANALYTICAL.value == "Analytical"
    assert StyleEnum.WHIMSICAL.value == "Whimsical"
    assert StyleEnum.PHILOSOPHICAL.value == "Philosophical"
    assert StyleEnum.EXPERIMENTAL.value == "Experimental"
    assert StyleEnum.PERSUASIVE.value == "Persuasive"
    
    # Test that we have the correct number of styles
    styles = list(StyleEnum)
    assert len(styles) == 15, f"Expected 15 styles in enum, got {len(styles)}"
    
    print("✓ StyleEnum tests passed")


def run_all_tests():
    """Run all tests."""
    print("=== Running Story Types Tests ===\n")
    
    try:
        test_story_type_registry()
        test_story_subtypes()
        test_story_subtype_class()
        test_story_type_class()
        test_archetype_registry()
        test_archetype_class()
        test_genre_registry()
        test_genre_subgenres()
        test_subgenre_class()
        test_genre_class()
        test_genre_enum()
        test_subgenre_enum()
        test_style_registry()
        test_style_properties()
        test_style_class()
        test_style_enum()
        
        print("\n✅ All tests passed!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)