#!/usr/bin/env python3
"""
Tests for the message router script to ensure it's working correctly.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the parent directory to the Python path to import the message router
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
parent_dir = script_dir.parent
sys.path.append(str(parent_dir))

# Import functions from the message router module
from script_message_router import (
    route_message,
    parse_marker,
    ensure_file_exists,
    append_to_file,
)

class TestMessageRouter(unittest.TestCase):
    """Test cases for the message router script."""

    def setUp(self):
        """Set up temporary directory and files for testing."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_dir = Path(self.temp_dir.name)
        
        # Override the base paths for testing
        self._original_base_path = os.environ.get("GOD_MODE_BASE_PATH")
        os.environ["GOD_MODE_BASE_PATH"] = str(self.test_dir)

    def tearDown(self):
        """Clean up temporary files and restore environment."""
        # Delete temporary directory
        self.temp_dir.cleanup()
        
        # Restore original environment variable if it existed
        if self._original_base_path:
            os.environ["GOD_MODE_BASE_PATH"] = self._original_base_path
        else:
            if "GOD_MODE_BASE_PATH" in os.environ:
                del os.environ["GOD_MODE_BASE_PATH"]

    def test_ensure_file_exists(self):
        """Test that ensure_file_exists creates files and directories as needed."""
        # Test creating a file in a non-existent directory
        test_file = self.test_dir / "test_dir" / "test_file.txt"
        ensure_file_exists(test_file)
        
        # Check that the directory and file were created
        self.assertTrue(test_file.parent.exists())
        self.assertTrue(test_file.exists())

    def test_append_to_file(self):
        """Test appending content to a file."""
        # Create a test file
        test_file = self.test_dir / "test_append.txt"
        test_content = "Test content"
        
        # Append content to the file
        append_to_file(test_file, test_content)
        
        # Check that the file contains the content
        with open(test_file, "r") as f:
            content = f.read()
        
        self.assertIn(test_content, content)
        
        # Append more content and check that both contents are present
        test_content2 = "More test content"
        append_to_file(test_file, test_content2)
        
        with open(test_file, "r") as f:
            content = f.read()
        
        self.assertIn(test_content, content)
        self.assertIn(test_content2, content)

    def test_parse_marker(self):
        """Test parsing markers from text."""
        # Test LOG_SUMMARY marker
        marker_type, content = parse_marker("[LOG_SUMMARY]Test summary")
        self.assertEqual(marker_type, "LOG_SUMMARY")
        self.assertEqual(content, "Test summary")
        
        # Test FEATURE_LOG marker with feature name
        marker_type, content = parse_marker("[FEATURE_LOG: TestFeature]Test feature log")
        self.assertEqual(marker_type, "FEATURE_LOG")
        self.assertEqual(content, "TestFeature]Test feature log")
        
        # Test DOC_UPDATE marker with doc type
        marker_type, content = parse_marker("[DOC_UPDATE: design]Test doc update")
        self.assertEqual(marker_type, "DOC_UPDATE")
        self.assertEqual(content, "design]Test doc update")
        
        # Test invalid marker
        marker_type, content = parse_marker("This is not a marker")
        self.assertIsNone(marker_type)
        self.assertIsNone(content)

    def test_route_message(self):
        """Test routing messages with various markers."""
        # Create a test message with multiple markers
        test_message = """
        This is a test message.
        
        [LOG_SUMMARY]Test summary log
        
        [LOG_DETAIL]
        # Test Detail Log
        
        This is a test detail log entry.
        
        [MEMORY_UPDATE]
        Test memory update.
        
        [FEATURE_LOG: TestFeature]
        Test feature log for TestFeature.
        
        [DOC_UPDATE: design]
        ## Test Design Doc Update
        
        Test design document update.
        
        [LEARNING]
        Test learning entry.
        
        [PROMPT_LEARNING]
        Test prompt learning entry.
        
        [DISCUSSION]
        Test discussion entry.
        """
        
        # Route the message
        route_message(test_message)
        
        # Check that the appropriate files were created
        memory_dir = self.test_dir / "god_mode" / "memory"
        docs_dir = self.test_dir / "god_mode" / "documentation"
        
        # Check LOG_SUMMARY file
        summary_file = memory_dir / "memory_logs_all.md"
        self.assertTrue(summary_file.exists())
        with open(summary_file, "r") as f:
            content = f.read()
        self.assertIn("Test summary log", content)
        
        # Check LOG_DETAIL file
        detail_file = memory_dir / "memory_logs_detailed.md"
        self.assertTrue(detail_file.exists())
        with open(detail_file, "r") as f:
            content = f.read()
        self.assertIn("Test Detail Log", content)
        
        # Check MEMORY_UPDATE file
        memory_file = memory_dir / "memory_cursor.md"
        self.assertTrue(memory_file.exists())
        with open(memory_file, "r") as f:
            content = f.read()
        self.assertIn("Test memory update.", content)
        
        # Check FEATURE_LOG file
        feature_file = memory_dir / "memory_log_feature_TestFeature.md"
        self.assertTrue(feature_file.exists())
        with open(feature_file, "r") as f:
            content = f.read()
        self.assertIn("Test feature log for TestFeature.", content)
        
        # Check DOC_UPDATE file
        doc_file = docs_dir / "documentation_design.md"
        self.assertTrue(doc_file.exists())
        with open(doc_file, "r") as f:
            content = f.read()
        self.assertIn("Test Design Doc Update", content)
        
        # Check LEARNING file
        learning_file = memory_dir / "memory_learnings.md"
        self.assertTrue(learning_file.exists())
        with open(learning_file, "r") as f:
            content = f.read()
        self.assertIn("Test learning entry.", content)
        
        # Check PROMPT_LEARNING file
        prompt_file = memory_dir / "memory_prompt_learnings.md"
        self.assertTrue(prompt_file.exists())
        with open(prompt_file, "r") as f:
            content = f.read()
        self.assertIn("Test prompt learning entry.", content)
        
        # Check DISCUSSION file
        discussion_file = self.test_dir / "god_mode" / "discussion_grasshop.md"
        self.assertTrue(discussion_file.exists())
        with open(discussion_file, "r") as f:
            content = f.read()
        self.assertIn("Test discussion entry.", content)

if __name__ == "__main__":
    unittest.main() 