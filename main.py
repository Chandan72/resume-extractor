#!/usr/bin/env python3
"""
Enhanced main entry point with command-line interface.
"""

import argparse
import os
import sys
from pathlib import Path
import logging

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from resume_extractor import ResumeExtractor
from config import config

def setup_logging(log_level: str = "INFO"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('resume_extractor.log')
        ]
    )

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract structured data from resume PDFs"
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Input file or directory path'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['csv', 'json', 'both'],
        default='both',
        help='Output format (default: both)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--single', '-s',
        type=str,
        help='Process a single resume file'
    )
    
    return parser.parse_args()

def main():
    """Enhanced main function with CLI."""
    args = parse_arguments()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    # Ensure directories exist
    config.ensure_directories()
    Path(args.output).mkdir(exist_ok=True)
    
    # Initialize extractor
    extractor = ResumeExtractor()
    
    print("Resume Data Extraction Tool v1.0")
    print("=" * 40)
    
    try:
        if args.single:
            # Process single file
            if not os.path.exists(args.single):
                print(f"Error: File {args.single} not found")
                return 1
            
            logger.info(f"Processing single file: {args.single}")
            result = extractor.extract_resume_data(args.single)
            
            # Save result
            output_name = Path(args.single).stem
            if args.format in ['json', 'both']:
                extractor.save_to_json([result], f"{args.output}/{output_name}.json")
            if args.format in ['csv', 'both']:
                extractor.save_to_csv([result], f"{args.output}/{output_name}.csv")
                
            print(f"Processing complete! Results saved to {args.output}/")
            
        else:
            # Process directory
            input_dir = args.input or "sample_resumes"
            
            if not os.path.exists(input_dir):
                print(f"Error: Directory {input_dir} not found")
                return 1
            
            pdf_files = list(Path(input_dir).glob("*.pdf"))
            if not pdf_files:
                print(f"No PDF files found in {input_dir}")
                return 1
            
            logger.info(f"Found {len(pdf_files)} PDF files to process")
            
            # Process all files
            if args.format in ['csv', 'both']:
                results = extractor.process_multiple_resumes(
                    input_dir, 
                    f"{args.output}/extracted_resumes.csv"
                )
            else:
                results = []
                for pdf_file in pdf_files:
                    result = extractor.extract_resume_data(str(pdf_file))
                    results.append(result)
            
            # Save JSON if requested
            if args.format in ['json', 'both']:
                extractor.save_to_json(results, f"{args.output}/extracted_resumes.json")
            
            print(f"Processing complete! {len(results)} resumes processed.")
            print(f"Results saved to {args.output}/")
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())