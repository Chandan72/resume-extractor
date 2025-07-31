import fitz  # PyMuPDF
import re
import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ResumeExtractor:
    def __init__(self):
        """Initialize the Resume Extractor with regex patterns for different fields."""
        
        # Email pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Phone pattern (various formats)
        self.phone_pattern = r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        
        # Common education keywords
        self.education_keywords = [
            'education', 'academic', 'university', 'college', 'school', 'institute',
            'bachelor', 'master', 'phd', 'doctorate', 'degree', 'diploma',
            'b.s.', 'b.a.', 'm.s.', 'm.a.', 'b.tech', 'm.tech', 'mba'
        ]
        
        # Common skill keywords
        self.skill_keywords = [
            'skills', 'technical skills', 'programming', 'languages', 'technologies',
            'tools', 'software', 'frameworks', 'databases', 'certifications'
        ]
        
        # Common programming languages and technologies
        self.tech_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'swift',
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
            'django', 'flask', 'spring', 'mysql', 'postgresql', 'mongodb',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'jenkins', 'machine learning', 'deep learning', 'generative ai',
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract raw text from PDF using PyMuPDF."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            logger.info(f"Successfully extracted text from {pdf_path}")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def normalize_text(self, text: str) -> str:
        """Normalize extracted text by cleaning whitespace and line breaks."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common line break issues
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)  # Handle hyphenated words
        text = re.sub(r'\n+', '\n', text)  # Multiple newlines to single
        
        # Remove extra spaces around punctuation
        text = re.sub(r'\s*([,;:.!?])\s*', r'\1 ', text)
        
        return text.strip()
    
    def extract_name(self, text: str) -> Optional[str]:
        """Extract name from resume text (usually first line or after common patterns)."""
        lines = text.split('\n')
        
        # Try first few lines for name
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            
            # Skip empty lines and common headers
            if not line or line.lower() in ['resume', 'curriculum vitae', 'cv']:
                continue
            
            # Look for lines that might be names (2-4 words, proper case)
            words = line.split()
            if 2 <= len(words) <= 4 and all(word.replace('.', '').isalpha() for word in words):
                if any(word[0].isupper() for word in words):
                    return line
        
        return None
    
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text."""
        emails = re.findall(self.email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text."""
        phones = re.findall(self.phone_pattern, text)
        if phones:
            # Format phone number
            area, first, last = phones[0]
            return f"({area}) {first}-{last}"
        return None
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information from text."""
        education_info = []
        lines = text.lower().split('\n')
        
        # Find education section
        education_start = -1
        for i, line in enumerate(lines):
            if any(keyword in line for keyword in self.education_keywords):
                education_start = i
                break
        
        if education_start == -1:
            return education_info
        
        # Extract education details
        for i in range(education_start, min(education_start + 10, len(lines))):
            line = lines[i].strip()
            if line and not any(keyword in line for keyword in ['experience', 'work', 'skills']):
                # Look for degree patterns
                if any(degree in line for degree in ['bachelor', 'master', 'phd', 'degree', 'b.s.', 'b.a.', 'm.s.', 'm.a.']):
                    education_info.append(line.title())
        
        return education_info
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text."""
        skills = []
        text_lower = text.lower()
        
        # Look for technical skills
        for skill in self.tech_skills:
            if skill in text_lower:
                skills.append(skill.title())
        
        # Find skills section and extract nearby content
        lines = text_lower.split('\n')
        skills_start = -1
        
        for i, line in enumerate(lines):
            if any(keyword in line for keyword in self.skill_keywords):
                skills_start = i
                break
        
        if skills_start != -1:
            # Extract skills from the next few lines
            for i in range(skills_start + 1, min(skills_start + 5, len(lines))):
                line = lines[i].strip()
                if line and not any(keyword in line for keyword in ['experience', 'education', 'work']):
                    # Split by common delimiters
                    line_skills = re.split(r'[,;|•]', line)
                    for skill in line_skills:
                        skill = skill.strip()
                        if skill and len(skill) > 2:
                            skills.append(skill.title())
        
        return list(set(skills))  # Remove duplicates
    
    def extract_resume_data(self, pdf_path: str) -> Dict:
        """Extract all data from a single resume PDF."""
        logger.info(f"Processing resume: {pdf_path}")
        
        # Extract and normalize text
        raw_text = self.extract_text_from_pdf(pdf_path)
        if not raw_text:
            return {"error": "Could not extract text from PDF"}
        
        normalized_text = self.normalize_text(raw_text)
        
        # Extract individual fields
        extracted_data = {
            "file_name": os.path.basename(pdf_path),
            "name": self.extract_name(normalized_text),
            "email": self.extract_email(normalized_text),
            "phone": self.extract_phone(normalized_text),
            "education": self.extract_education(normalized_text),
            "skills": self.extract_skills(normalized_text)
        }
        
        logger.info(f"Extraction completed for {pdf_path}")
        return extracted_data
    
    def process_multiple_resumes(self, resume_folder: str, output_file: str = "extracted_resumes.csv") -> List[Dict]:
        """Process multiple resume PDFs and save results to CSV."""
        resume_folder = Path(resume_folder)
        all_data = []
        
        # Find all PDF files
        pdf_files = list(resume_folder.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {resume_folder}")
            return []
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF
        for pdf_file in pdf_files:
            data = self.extract_resume_data(str(pdf_file))
            all_data.append(data)
        
        # Save to CSV
        self.save_to_csv(all_data, output_file)
        
        return all_data
    
    def save_to_csv(self, data: List[Dict], output_file: str):
        """Save extracted data to CSV file."""
        if not data:
            logger.warning("No data to save")
            return
        
        # Prepare CSV headers
        fieldnames = ['file_name', 'name', 'email', 'phone', 'education', 'skills']
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in data:
                    # Convert lists to strings for CSV
                    csv_row = row.copy()
                    if 'education' in csv_row and isinstance(csv_row['education'], list):
                        csv_row['education'] = '; '.join(csv_row['education'])
                    if 'skills' in csv_row and isinstance(csv_row['skills'], list):
                        csv_row['skills'] = '; '.join(csv_row['skills'])
                    
                    writer.writerow(csv_row)
            
            logger.info(f"Data saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
    
    def save_to_json(self, data: List[Dict], output_file: str = "extracted_resumes.json"):
        """Save extracted data to JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            logger.info(f"Data saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving to JSON: {str(e)}")


def main():
    """Main function to demonstrate usage."""
    extractor = ResumeExtractor()
    
    # Example 1: Process a single resume
    print("=== Single Resume Processing ===")
    single_resume_path = "sample_resumes/resume1.pdf"  # Update this path
    
    if os.path.exists(single_resume_path):
        result = extractor.extract_resume_data(single_resume_path)
        print("Extracted Data:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Sample resume not found at {single_resume_path}")
    
    # Example 2: Process multiple resumes
    print("\n=== Multiple Resume Processing ===")
    resume_folder = "sample_resumes"  # Update this path
    
    if os.path.exists(resume_folder):
        results = extractor.process_multiple_resumes(resume_folder, "output/extracted_resumes.csv")
        print(f"Processed {len(results)} resumes")
        
        # Also save as JSON
        extractor.save_to_json(results, "output/extracted_resumes.json")
    else:
        print(f"Resume folder not found at {resume_folder}")
        print("Please create the folder and add some sample resume PDFs")


if __name__ == "__main__":
    main()