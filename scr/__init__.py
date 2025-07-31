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


