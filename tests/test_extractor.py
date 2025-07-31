"""
Unit tests for resume extractor.
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from resume_extractor import ResumeExtractor

class TestResumeExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = ResumeExtractor()
    
    def test_extract_email(self):
        text = "Contact me at john.doe@email.com for more information."
        result = self.extractor.extract_email(text)
        self.assertEqual(result, "john.doe@email.com")
    
    def test_extract_phone(self):
        text = "Call me at (555) 123-4567 or 555.123.4567"
        result = self.extractor.extract_phone(text)
        self.assertEqual(result, "(555) 123-4567")
    
    def test_normalize_text(self):
        text = "This   has    extra    spaces\n\n\nand   newlines"
        result = self.extractor.normalize_text(text)
        self.assertNotIn("   ", result)  # No triple spaces
    
    def test_extract_skills(self):
        text = "Skills: Python, JavaScript, React, Node.js, MySQL"
        result = self.extractor.extract_skills(text)
        self.assertIn("Python", result)
        self.assertIn("Javascript", result)

if __name__ == '__main__':
    unittest.main()