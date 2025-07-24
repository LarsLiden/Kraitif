"""
Unit tests for ChapterSummary object and related classes.
"""

import unittest
import json
from objects.chapter_summary import ChapterSummary
from objects.continuity_state import ContinuityState
from objects.continuity_character import ContinuityCharacter
from objects.continuity_object import ContinuityObject
from objects.plot_thread import PlotThread


class TestContinuityCharacter(unittest.TestCase):
    """Test cases for ContinuityCharacter class."""
    
    def test_character_creation(self):
        """Test basic character creation."""
        char = ContinuityCharacter(
            name="Riven Kairo",
            current_location="Eldertown—foggy main street",
            status="haunted by guilt, resolve rekindled",
            inventory=["town crest badge"]
        )
        
        self.assertEqual(char.name, "Riven Kairo")
        self.assertEqual(char.current_location, "Eldertown—foggy main street")
        self.assertEqual(char.status, "haunted by guilt, resolve rekindled")
        self.assertEqual(char.inventory, ["town crest badge"])
    
    def test_character_creation_validation(self):
        """Test character creation validation."""
        # Empty name should raise ValueError
        with self.assertRaises(ValueError):
            ContinuityCharacter(name="", current_location="location", status="status")
        
        # Empty location should raise ValueError
        with self.assertRaises(ValueError):
            ContinuityCharacter(name="name", current_location="", status="status")
        
        # Empty status should raise ValueError
        with self.assertRaises(ValueError):
            ContinuityCharacter(name="name", current_location="location", status="")
    
    def test_inventory_management(self):
        """Test inventory item management."""
        char = ContinuityCharacter("Test", "Location", "Status")
        
        # Add item
        result = char.add_inventory_item("sword")
        self.assertTrue(result)
        self.assertIn("sword", char.inventory)
        
        # Adding same item should not duplicate
        result = char.add_inventory_item("sword")
        self.assertFalse(result)
        self.assertEqual(char.inventory.count("sword"), 1)
        
        # Add empty item should fail
        result = char.add_inventory_item("")
        self.assertFalse(result)
        
        # Remove item
        result = char.remove_inventory_item("sword")
        self.assertTrue(result)
        self.assertNotIn("sword", char.inventory)
        
        # Remove non-existent item should fail
        result = char.remove_inventory_item("nonexistent")
        self.assertFalse(result)
    
    def test_character_serialization(self):
        """Test character to_dict and from_dict methods."""
        char = ContinuityCharacter(
            name="Test Character",
            current_location="Test Location", 
            status="Test Status",
            inventory=["item1", "item2"]
        )
        
        # Test to_dict
        char_dict = char.to_dict()
        expected_dict = {
            'name': "Test Character",
            'current_location': "Test Location",
            'status': "Test Status",
            'inventory': ["item1", "item2"]
        }
        self.assertEqual(char_dict, expected_dict)
        
        # Test from_dict
        restored_char = ContinuityCharacter.from_dict(char_dict)
        self.assertIsNotNone(restored_char)
        self.assertEqual(restored_char.name, char.name)
        self.assertEqual(restored_char.current_location, char.current_location)
        self.assertEqual(restored_char.status, char.status)
        self.assertEqual(restored_char.inventory, char.inventory)
    
    def test_character_from_dict_invalid(self):
        """Test character from_dict with invalid data."""
        # Invalid data types
        self.assertIsNone(ContinuityCharacter.from_dict("not a dict"))
        self.assertIsNone(ContinuityCharacter.from_dict(None))
        
        # Missing required fields
        self.assertIsNone(ContinuityCharacter.from_dict({}))
        self.assertIsNone(ContinuityCharacter.from_dict({'name': 'test'}))
        self.assertIsNone(ContinuityCharacter.from_dict({'name': 'test', 'current_location': 'loc'}))


class TestContinuityObject(unittest.TestCase):
    """Test cases for ContinuityObject class."""
    
    def test_object_creation(self):
        """Test basic object creation."""
        obj = ContinuityObject(
            name="Silver Dagger",
            holder=None,
            location="Riven's satchel"
        )
        
        self.assertEqual(obj.name, "Silver Dagger")
        self.assertIsNone(obj.holder)
        self.assertEqual(obj.location, "Riven's satchel")
    
    def test_object_creation_with_holder(self):
        """Test object creation with holder."""
        obj = ContinuityObject(
            name="Ancient Seal",
            holder="High Priestess Merin",
            location="Eldertown Temple"
        )
        
        self.assertEqual(obj.name, "Ancient Seal")
        self.assertEqual(obj.holder, "High Priestess Merin")
        self.assertEqual(obj.location, "Eldertown Temple")
    
    def test_object_creation_validation(self):
        """Test object creation validation."""
        # Empty name should raise ValueError
        with self.assertRaises(ValueError):
            ContinuityObject(name="", holder=None, location="location")
        
        # Empty location should raise ValueError
        with self.assertRaises(ValueError):
            ContinuityObject(name="name", holder=None, location="")
    
    def test_object_serialization(self):
        """Test object to_dict and from_dict methods."""
        obj = ContinuityObject(
            name="Test Object",
            holder="Test Holder",
            location="Test Location"
        )
        
        # Test to_dict
        obj_dict = obj.to_dict()
        expected_dict = {
            'name': "Test Object",
            'holder': "Test Holder",
            'location': "Test Location"
        }
        self.assertEqual(obj_dict, expected_dict)
        
        # Test from_dict
        restored_obj = ContinuityObject.from_dict(obj_dict)
        self.assertIsNotNone(restored_obj)
        self.assertEqual(restored_obj.name, obj.name)
        self.assertEqual(restored_obj.holder, obj.holder)
        self.assertEqual(restored_obj.location, obj.location)
    
    def test_object_serialization_no_holder(self):
        """Test object serialization with no holder."""
        obj = ContinuityObject(
            name="Test Object",
            holder=None,
            location="Test Location"
        )
        
        obj_dict = obj.to_dict()
        self.assertIsNone(obj_dict['holder'])
        
        restored_obj = ContinuityObject.from_dict(obj_dict)
        self.assertIsNotNone(restored_obj)
        self.assertIsNone(restored_obj.holder)
    
    def test_object_from_dict_invalid(self):
        """Test object from_dict with invalid data."""
        # Invalid data types
        self.assertIsNone(ContinuityObject.from_dict("not a dict"))
        self.assertIsNone(ContinuityObject.from_dict(None))
        
        # Missing required fields
        self.assertIsNone(ContinuityObject.from_dict({}))
        self.assertIsNone(ContinuityObject.from_dict({'name': 'test'}))


class TestPlotThread(unittest.TestCase):
    """Test cases for PlotThread class."""
    
    def test_plot_thread_creation(self):
        """Test basic plot thread creation."""
        thread = PlotThread(
            id="HaunterThreat",
            description="The Haunter's next move after the fog-shrouded warning",
            status="pending"
        )
        
        self.assertEqual(thread.id, "HaunterThreat")
        self.assertEqual(thread.description, "The Haunter's next move after the fog-shrouded warning")
        self.assertEqual(thread.status, "pending")
    
    def test_plot_thread_creation_validation(self):
        """Test plot thread creation validation."""
        # Empty id should raise ValueError
        with self.assertRaises(ValueError):
            PlotThread(id="", description="desc", status="status")
        
        # Empty description should raise ValueError
        with self.assertRaises(ValueError):
            PlotThread(id="id", description="", status="status")
        
        # Empty status should raise ValueError
        with self.assertRaises(ValueError):
            PlotThread(id="id", description="desc", status="")
    
    def test_plot_thread_serialization(self):
        """Test plot thread to_dict and from_dict methods."""
        thread = PlotThread(
            id="TestThread",
            description="Test Description",
            status="Test Status"
        )
        
        # Test to_dict
        thread_dict = thread.to_dict()
        expected_dict = {
            'id': "TestThread",
            'description': "Test Description",
            'status': "Test Status"
        }
        self.assertEqual(thread_dict, expected_dict)
        
        # Test from_dict
        restored_thread = PlotThread.from_dict(thread_dict)
        self.assertIsNotNone(restored_thread)
        self.assertEqual(restored_thread.id, thread.id)
        self.assertEqual(restored_thread.description, thread.description)
        self.assertEqual(restored_thread.status, thread.status)
    
    def test_plot_thread_from_dict_invalid(self):
        """Test plot thread from_dict with invalid data."""
        # Invalid data types
        self.assertIsNone(PlotThread.from_dict("not a dict"))
        self.assertIsNone(PlotThread.from_dict(None))
        
        # Missing required fields
        self.assertIsNone(PlotThread.from_dict({}))
        self.assertIsNone(PlotThread.from_dict({'id': 'test'}))
        self.assertIsNone(PlotThread.from_dict({'id': 'test', 'description': 'desc'}))


class TestContinuityState(unittest.TestCase):
    """Test cases for ContinuityState class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.continuity_state = ContinuityState()
    
    def test_continuity_state_creation(self):
        """Test basic continuity state creation."""
        self.assertEqual(len(self.continuity_state.characters), 0)
        self.assertEqual(len(self.continuity_state.objects), 0)
        self.assertEqual(len(self.continuity_state.locations_visited), 0)
        self.assertEqual(len(self.continuity_state.open_plot_threads), 0)
    
    def test_character_management(self):
        """Test character management in continuity state."""
        char = ContinuityCharacter("Test", "Location", "Status")
        
        # Add character
        result = self.continuity_state.add_character(char)
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.characters), 1)
        
        # Get character
        retrieved_char = self.continuity_state.get_character("Test")
        self.assertIsNotNone(retrieved_char)
        self.assertEqual(retrieved_char.name, "Test")
        
        # Case insensitive get
        retrieved_char = self.continuity_state.get_character("test")
        self.assertIsNotNone(retrieved_char)
        
        # Update existing character
        updated_char = ContinuityCharacter("Test", "New Location", "New Status")
        result = self.continuity_state.add_character(updated_char)
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.characters), 1)  # Should still be 1
        
        retrieved_char = self.continuity_state.get_character("Test")
        self.assertEqual(retrieved_char.current_location, "New Location")
        self.assertEqual(retrieved_char.status, "New Status")
        
        # Remove character
        result = self.continuity_state.remove_character("Test")
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.characters), 0)
        
        # Remove non-existent character
        result = self.continuity_state.remove_character("NonExistent")
        self.assertFalse(result)
    
    def test_object_management(self):
        """Test object management in continuity state."""
        obj = ContinuityObject("Test Object", "Holder", "Location")
        
        # Add object
        result = self.continuity_state.add_object(obj)
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.objects), 1)
        
        # Get object
        retrieved_obj = self.continuity_state.get_object("Test Object")
        self.assertIsNotNone(retrieved_obj)
        self.assertEqual(retrieved_obj.name, "Test Object")
        
        # Case insensitive get
        retrieved_obj = self.continuity_state.get_object("test object")
        self.assertIsNotNone(retrieved_obj)
        
        # Update existing object
        updated_obj = ContinuityObject("Test Object", "New Holder", "New Location")
        result = self.continuity_state.add_object(updated_obj)
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.objects), 1)  # Should still be 1
        
        retrieved_obj = self.continuity_state.get_object("Test Object")
        self.assertEqual(retrieved_obj.holder, "New Holder")
        self.assertEqual(retrieved_obj.location, "New Location")
        
        # Remove object
        result = self.continuity_state.remove_object("Test Object")
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.objects), 0)
        
        # Remove non-existent object
        result = self.continuity_state.remove_object("NonExistent")
        self.assertFalse(result)
    
    def test_location_management(self):
        """Test location management in continuity state."""
        # Add location
        result = self.continuity_state.add_location("Test Location")
        self.assertTrue(result)
        self.assertIn("Test Location", self.continuity_state.locations_visited)
        
        # Add duplicate location (should not duplicate)
        result = self.continuity_state.add_location("Test Location")
        self.assertFalse(result)
        self.assertEqual(self.continuity_state.locations_visited.count("Test Location"), 1)
        
        # Add empty location should fail
        result = self.continuity_state.add_location("")
        self.assertFalse(result)
        
        # Remove location
        result = self.continuity_state.remove_location("Test Location")
        self.assertTrue(result)
        self.assertNotIn("Test Location", self.continuity_state.locations_visited)
        
        # Remove non-existent location
        result = self.continuity_state.remove_location("NonExistent")
        self.assertFalse(result)
    
    def test_plot_thread_management(self):
        """Test plot thread management in continuity state."""
        thread = PlotThread("TestId", "Test Description", "Test Status")
        
        # Add plot thread
        result = self.continuity_state.add_plot_thread(thread)
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.open_plot_threads), 1)
        
        # Get plot thread
        retrieved_thread = self.continuity_state.get_plot_thread("TestId")
        self.assertIsNotNone(retrieved_thread)
        self.assertEqual(retrieved_thread.id, "TestId")
        
        # Case insensitive get
        retrieved_thread = self.continuity_state.get_plot_thread("testid")
        self.assertIsNotNone(retrieved_thread)
        
        # Update existing plot thread
        updated_thread = PlotThread("TestId", "New Description", "New Status")
        result = self.continuity_state.add_plot_thread(updated_thread)
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.open_plot_threads), 1)  # Should still be 1
        
        retrieved_thread = self.continuity_state.get_plot_thread("TestId")
        self.assertEqual(retrieved_thread.description, "New Description")
        self.assertEqual(retrieved_thread.status, "New Status")
        
        # Remove plot thread
        result = self.continuity_state.remove_plot_thread("TestId")
        self.assertTrue(result)
        self.assertEqual(len(self.continuity_state.open_plot_threads), 0)
        
        # Remove non-existent plot thread
        result = self.continuity_state.remove_plot_thread("NonExistent")
        self.assertFalse(result)
    
    def test_continuity_state_serialization(self):
        """Test continuity state serialization."""
        # Set up test data
        char = ContinuityCharacter("Test Char", "Location", "Status", ["item1"])
        obj = ContinuityObject("Test Obj", "Holder", "Location")
        thread = PlotThread("TestId", "Description", "Status")
        
        self.continuity_state.add_character(char)
        self.continuity_state.add_object(obj)
        self.continuity_state.add_location("Test Location")
        self.continuity_state.add_plot_thread(thread)
        
        # Test to_dict
        state_dict = self.continuity_state.to_dict()
        
        self.assertEqual(len(state_dict['characters']), 1)
        self.assertEqual(len(state_dict['objects']), 1)
        self.assertEqual(len(state_dict['locations_visited']), 1)
        self.assertEqual(len(state_dict['open_plot_threads']), 1)
        
        # Test from_dict
        restored_state = ContinuityState.from_dict(state_dict)
        self.assertIsNotNone(restored_state)
        self.assertEqual(len(restored_state.characters), 1)
        self.assertEqual(len(restored_state.objects), 1)
        self.assertEqual(len(restored_state.locations_visited), 1)
        self.assertEqual(len(restored_state.open_plot_threads), 1)
        
        # Verify data integrity
        self.assertEqual(restored_state.characters[0].name, "Test Char")
        self.assertEqual(restored_state.objects[0].name, "Test Obj")
        self.assertEqual(restored_state.locations_visited[0], "Test Location")
        self.assertEqual(restored_state.open_plot_threads[0].id, "TestId")
    
    def test_continuity_state_from_dict_invalid(self):
        """Test continuity state from_dict with invalid data."""
        # Invalid data types
        self.assertIsNone(ContinuityState.from_dict("not a dict"))
        self.assertIsNone(ContinuityState.from_dict(None))
        
        # Empty dict should work (create empty state)
        empty_state = ContinuityState.from_dict({})
        self.assertIsNotNone(empty_state)
        self.assertEqual(len(empty_state.characters), 0)


class TestChapterSummary(unittest.TestCase):
    """Test cases for ChapterSummary class."""
    
    def test_chapter_summary_creation(self):
        """Test basic chapter summary creation."""
        summary = ChapterSummary("recap of what just happened in the chapter")
        
        self.assertEqual(summary.summary, "recap of what just happened in the chapter")
        self.assertIsNotNone(summary.continuity_state)
        self.assertEqual(len(summary.continuity_state.characters), 0)
    
    def test_chapter_summary_creation_validation(self):
        """Test chapter summary creation validation."""
        # Empty summary should raise ValueError
        with self.assertRaises(ValueError):
            ChapterSummary("")
    
    def test_chapter_summary_with_continuity(self):
        """Test chapter summary with continuity state."""
        continuity_state = ContinuityState()
        char = ContinuityCharacter("Test", "Location", "Status")
        continuity_state.add_character(char)
        
        summary = ChapterSummary("Test summary", continuity_state)
        
        self.assertEqual(summary.summary, "Test summary")
        self.assertEqual(len(summary.continuity_state.characters), 1)
    
    def test_chapter_summary_serialization(self):
        """Test chapter summary serialization."""
        # Create test data
        continuity_state = ContinuityState()
        char = ContinuityCharacter("Riven Kairo", "Eldertown—foggy main street", 
                                   "haunted by guilt, resolve rekindled", ["town crest badge"])
        obj = ContinuityObject("Silver Dagger", None, "Riven's satchel")
        thread = PlotThread("HaunterThreat", 
                           "The Haunter's next move after the fog-shrouded warning", 
                           "pending")
        
        continuity_state.add_character(char)
        continuity_state.add_object(obj)
        continuity_state.add_location("Eldertown main street")
        continuity_state.add_plot_thread(thread)
        
        summary = ChapterSummary("recap of what just happened in the chapter", continuity_state)
        
        # Test to_dict
        summary_dict = summary.to_dict()
        
        self.assertEqual(summary_dict['summary'], "recap of what just happened in the chapter")
        self.assertIn('continuity_state', summary_dict)
        self.assertEqual(len(summary_dict['continuity_state']['characters']), 1)
        self.assertEqual(len(summary_dict['continuity_state']['objects']), 1)
        self.assertEqual(len(summary_dict['continuity_state']['locations_visited']), 1)
        self.assertEqual(len(summary_dict['continuity_state']['open_plot_threads']), 1)
        
        # Test from_dict
        restored_summary = ChapterSummary.from_dict(summary_dict)
        self.assertIsNotNone(restored_summary)
        self.assertEqual(restored_summary.summary, summary.summary)
        self.assertEqual(len(restored_summary.continuity_state.characters), 1)
        
        # Verify character data
        restored_char = restored_summary.continuity_state.characters[0]
        self.assertEqual(restored_char.name, "Riven Kairo")
        self.assertEqual(restored_char.current_location, "Eldertown—foggy main street")
        self.assertEqual(restored_char.status, "haunted by guilt, resolve rekindled")
        self.assertEqual(restored_char.inventory, ["town crest badge"])
    
    def test_chapter_summary_json_serialization(self):
        """Test chapter summary JSON serialization."""
        summary = ChapterSummary("Test summary")
        
        # Test to_json
        json_str = summary.to_json()
        self.assertIsInstance(json_str, str)
        
        # Test from_json
        restored_summary = ChapterSummary.from_json(json_str)
        self.assertIsNotNone(restored_summary)
        self.assertEqual(restored_summary.summary, summary.summary)
    
    def test_chapter_summary_from_sample_json(self):
        """Test chapter summary from the provided sample JSON."""
        sample_json = {
            "summary": "recap of what just happened in the chapter",
            "continuity_state": {
                "characters": [
                    {
                        "name": "Riven Kairo",
                        "current_location": "Eldertown—foggy main street",
                        "status": "haunted by guilt, resolve rekindled",
                        "inventory": ["town crest badge"]
                    },
                    {
                        "name": "Corbin Hale",
                        "current_location": "The Hillside Hermitage",
                        "status": "mysterious prophet",
                        "inventory": []
                    }
                ],
                "objects": [
                    {
                        "name": "Ancient Seal",
                        "holder": "High Priestess Merin",
                        "location": "Eldertown Temple"
                    },
                    {
                        "name": "Silver Dagger",
                        "holder": None,
                        "location": "Riven's satchel"
                    }
                ],
                "locations_visited": [
                    "Eldertown main street",
                    "Hillside Hermitage"
                ],
                "open_plot_threads": [
                    {
                        "id": "HaunterThreat",
                        "description": "The Haunter's next move after the fog-shrouded warning",
                        "status": "pending"
                    },
                    {
                        "id": "RivenGuilt",
                        "description": "Riven's reckoning with past failure",
                        "status": "in progress"
                    }
                ]
            }
        }
        
        # Test creating from sample JSON
        summary = ChapterSummary.from_dict(sample_json)
        self.assertIsNotNone(summary)
        
        # Verify summary
        self.assertEqual(summary.summary, "recap of what just happened in the chapter")
        
        # Verify characters
        self.assertEqual(len(summary.continuity_state.characters), 2)
        riven = summary.continuity_state.get_character("Riven Kairo")
        self.assertIsNotNone(riven)
        self.assertEqual(riven.current_location, "Eldertown—foggy main street")
        self.assertEqual(riven.status, "haunted by guilt, resolve rekindled")
        self.assertEqual(riven.inventory, ["town crest badge"])
        
        corbin = summary.continuity_state.get_character("Corbin Hale")
        self.assertIsNotNone(corbin)
        self.assertEqual(corbin.current_location, "The Hillside Hermitage")
        self.assertEqual(corbin.status, "mysterious prophet")
        self.assertEqual(corbin.inventory, [])
        
        # Verify objects
        self.assertEqual(len(summary.continuity_state.objects), 2)
        seal = summary.continuity_state.get_object("Ancient Seal")
        self.assertIsNotNone(seal)
        self.assertEqual(seal.holder, "High Priestess Merin")
        self.assertEqual(seal.location, "Eldertown Temple")
        
        dagger = summary.continuity_state.get_object("Silver Dagger")
        self.assertIsNotNone(dagger)
        self.assertIsNone(dagger.holder)
        self.assertEqual(dagger.location, "Riven's satchel")
        
        # Verify locations
        self.assertEqual(len(summary.continuity_state.locations_visited), 2)
        self.assertIn("Eldertown main street", summary.continuity_state.locations_visited)
        self.assertIn("Hillside Hermitage", summary.continuity_state.locations_visited)
        
        # Verify plot threads
        self.assertEqual(len(summary.continuity_state.open_plot_threads), 2)
        haunter_threat = summary.continuity_state.get_plot_thread("HaunterThreat")
        self.assertIsNotNone(haunter_threat)
        self.assertEqual(haunter_threat.description, "The Haunter's next move after the fog-shrouded warning")
        self.assertEqual(haunter_threat.status, "pending")
        
        riven_guilt = summary.continuity_state.get_plot_thread("RivenGuilt")
        self.assertIsNotNone(riven_guilt)
        self.assertEqual(riven_guilt.description, "Riven's reckoning with past failure")
        self.assertEqual(riven_guilt.status, "in progress")
    
    def test_chapter_summary_from_dict_invalid(self):
        """Test chapter summary from_dict with invalid data."""
        # Invalid data types
        self.assertIsNone(ChapterSummary.from_dict("not a dict"))
        self.assertIsNone(ChapterSummary.from_dict(None))
        
        # Missing summary
        self.assertIsNone(ChapterSummary.from_dict({}))
        self.assertIsNone(ChapterSummary.from_dict({'continuity_state': {}}))
    
    def test_chapter_summary_from_json_invalid(self):
        """Test chapter summary from_json with invalid JSON."""
        # Invalid JSON string
        self.assertIsNone(ChapterSummary.from_json("invalid json"))
        self.assertIsNone(ChapterSummary.from_json(""))
    
    def test_chapter_summary_string_representation(self):
        """Test chapter summary string representation."""
        continuity_state = ContinuityState()
        char = ContinuityCharacter("Test", "Location", "Status")
        obj = ContinuityObject("Test Obj", "Holder", "Location")
        continuity_state.add_character(char)
        continuity_state.add_object(obj)
        continuity_state.add_location("Test Location")
        thread = PlotThread("TestId", "Description", "Status")
        continuity_state.add_plot_thread(thread)
        
        summary = ChapterSummary("This is a very long summary that should be truncated in the string representation", continuity_state)
        
        str_repr = str(summary)
        self.assertIn("This is a very long summary that should be truncat", str_repr)
        self.assertIn("Characters: 1", str_repr)
        self.assertIn("Objects: 1", str_repr)
        self.assertIn("Locations: 1", str_repr)
        self.assertIn("Plot Threads: 1", str_repr)


if __name__ == '__main__':
    unittest.main()