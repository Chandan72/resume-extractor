# src/__init__.py
"""
Resume Data Extraction Package

This package provides tools for extracting structured data from resume PDFs.
"""

__version__ = "1.0.0"
__author__ = "Chandan"
__email__ = "chandan875792@gmail.com"

from .resume_extractor import ResumeExtractor
from .utils import (
    clean_text,
    extract_urls,
    extract_linkedin_profile,
    validate_email,
    format_phone_number
)

__all__ = [
    'ResumeExtractor',
    'clean_text',
    'extract_urls',
    'extract_linkedin_profile',
    'validate_email',
    'format_phone_number'
]

# Package-level configuration
import logging

# Set up package logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Default configuration
DEFAULT_CONFIG = {
    'pdf_extraction': {
        'max_pages': 10,
        'encoding': 'utf-8'
    },
    'text_processing': {
        'min_name_words': 2,
        'max_name_words': 4,
        'skill_min_length': 2
    },
    'output': {
        'csv_delimiter': ',',
        'json_indent': 2
    }
}


# tests/__init__.py
"""
Test suite for Resume Data Extraction Package

This module contains unit tests for the resume extraction functionality.
"""

"""import os
import sys
from pathlib import Path

# Add the src directory to the Python path for testing
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

# Test configuration
TEST_CONFIG = {
    'sample_resumes_dir': project_root / 'sample_resumes',
    'test_output_dir': project_root / 'tests' / 'test_output',
    'test_data_dir': project_root / 'tests' / 'test_data'
}

# Create test directories if they don't exist
for directory in TEST_CONFIG.values():
    if isinstance(directory, Path):
        directory.mkdir(exist_ok=True)

# Test utilities
def get_test_file_path(filename: str) -> str:
    """Get the full path to a test file."""
    return str(TEST_CONFIG['test_data_dir'] / filename)

def get_sample_resume_path(filename: str) -> str:
    """Get the full path to a sample resume."""
    return str(TEST_CONFIG['sample_resumes_dir'] / filename)

def cleanup_test_files():
    """Clean up generated test files."""
    import shutil
    if TEST_CONFIG['test_output_dir'].exists():
        shutil.rmtree(TEST_CONFIG['test_output_dir'])
        TEST_CONFIG['test_output_dir'].mkdir()

__all__ = [
    'TEST_CONFIG',
    'get_test_file_path',
    'get_sample_resume_path',
    'cleanup_test_files'
]"""