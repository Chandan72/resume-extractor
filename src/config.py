# src/config.py
"""
Configuration settings for the Resume Extractor.
"""

import os
from pathlib import Path
from typing import Dict, List

class Config:
    """Configuration class for Resume Extractor."""
    
    # Base directories
    BASE_DIR = Path(__file__).parent.parent
    SRC_DIR = BASE_DIR / "src"
    SAMPLE_DIR = BASE_DIR / "sample_resumes"
    OUTPUT_DIR = BASE_DIR / "output"
    
    # File patterns
    SUPPORTED_EXTENSIONS = [".pdf"]
    
    # Extraction settings
    MAX_NAME_WORDS = 4
    MIN_NAME_WORDS = 2
    MAX_SKILL_WORDS = 3
    MIN_SKILL_LENGTH = 2
    
    # Regex patterns
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_PATTERNS = [
        r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
        r'(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})',
        r'\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
    ]
    
    # Keywords for different sections
    EDUCATION_KEYWORDS = [
        'education', 'academic', 'university', 'college', 'school', 'institute',
        'bachelor', 'master', 'phd', 'doctorate', 'degree', 'diploma',
        'b.s.', 'b.a.', 'm.s.', 'm.a.', 'b.tech', 'm.tech', 'mba', 'certification'
    ]
    
    SKILL_KEYWORDS = [
        'skills', 'technical skills', 'programming', 'languages', 'technologies',
        'tools', 'software', 'frameworks', 'databases', 'certifications',
        'competencies', 'expertise', 'proficient'
    ]
    
    EXPERIENCE_KEYWORDS = [
        'experience', 'work experience', 'employment', 'career', 'professional',
        'work history', 'positions', 'roles'
    ]
    
    # Common technical skills
    TECHNICAL_SKILLS = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 
        'go', 'swift', 'kotlin', 'scala', 'rust', 'r', 'matlab', 'sql',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'jquery',
        'bootstrap', 'sass', 'less', 'webpack', 'babel',
        
        # Frameworks and Libraries
        'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net', 'pandas',
        'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
        
        # Databases
        'mysql', 'postgresql', 'mongodb', 'sqlite', 'redis', 'elasticsearch',
        'oracle', 'sql server', 'cassandra',
        
        # Cloud and DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github',
        'gitlab', 'ci/cd', 'terraform', 'ansible',
        
        # Operating Systems
        'linux', 'unix', 'windows', 'macos', 'ubuntu', 'centos',
        
        # Other Tools
        'jira', 'confluence', 'slack', 'trello', 'postman', 'swagger'
    ]
    
    # Degree patterns
    DEGREE_PATTERNS = [
        r'bachelor[\'s]?\s+(?:of\s+)?(?:science|arts|engineering|business)',
        r'master[\'s]?\s+(?:of\s+)?(?:science|arts|engineering|business)',
        r'b\.?[sa]\.?', r'm\.?[sa]\.?', r'ph\.?d\.?', r'mba', r'b\.?tech', r'm\.?tech'
    ]
    
    # Output settings
    CSV_ENCODING = 'utf-8'
    JSON_INDENT = 2
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        for directory in [cls.SAMPLE_DIR, cls.OUTPUT_DIR]:
            directory.mkdir(exist_ok=True)
    
    @classmethod
    def get_sample_files(cls) -> List[Path]:
        """Get list of sample PDF files."""
        cls.ensure_directories()
        return list(cls.SAMPLE_DIR.glob("*.pdf"))


# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = "INFO"


# Select configuration based on environment
config_name = os.getenv('RESUME_EXTRACTOR_ENV', 'development').lower()
if config_name == 'production':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()