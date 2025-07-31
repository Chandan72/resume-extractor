#!/usr/bin/env python3
"""
Main entry point for the Resume Data Extraction project.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from resume_extractor import ResumeExtractor
import logging

def setup_directories():
    """Create necessary directories if they don't exist."""
    directories = ['sample_resumes', 'output', 'tests']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def main():
    """Main function."""
    setup_directories()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    extractor = ResumeExtractor()
    
    print("Resume Data Extraction Tool")
    print("=" * 30)
    
    # Check if sample resumes exist
    sample_dir = Path("sample_resumes")
    pdf_files = list(sample_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in sample_resumes/ directory.")
        print("Please add some resume PDFs to get started.")
        return
    
    print(f"Found {len(pdf_files)} resume(s) to process:")
    for pdf in pdf_files:
        print(f"  - {pdf.name}")
    
    # Process all resumes
    results = extractor.process_multiple_resumes(
        "sample_resumes", 
        "output/extracted_resumes.csv"
    )
    
    # Save as JSON too
    extractor.save_to_json(results, "output/extracted_resumes.json")
    
    print(f"\nProcessing complete! Results saved to:")
    print("  - output/extracted_resumes.csv")
    print("  - output/extracted_resumes.json")

if __name__ == "__main__":
    main()