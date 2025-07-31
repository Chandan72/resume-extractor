# Resume Data Extractor

A Python tool to automatically extract key information like name, email, phone number, education, and skills from resume PDF files.

## Features

- Parses multiple PDF resumes from a specified folder.
- Extracts Name, Email, Phone Number, Education, and Skills.
- Saves the extracted data to both CSV and JSON formats for easy use.
- Simple command-line interface.

## Setup and Installation

Follow these steps to get the project up and running on your local machine.

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd resume-extractor
    ```

2.  **Create and Activate a Virtual Environment**

    It is highly recommended to use a virtual environment to manage project dependencies.

    ```bash
    # Create the virtual environment
    python3 -m venv .venv

    # Activate it (macOS/Linux)
    source .venv/bin/activate

    # Or activate it (Windows PowerShell)
    # .\.venv\Scripts\Activate.ps1
    ```

3.  **Install Dependencies**
    With the virtual environment active, install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Place the resume PDF files you want to process into the `sample_resumes/` directory.
2.  Run the main script from the root of the project:
    ```bash
    python main.py
    ```
3.  The script will process all PDFs in the `sample_resumes` folder.

### Output

The extracted data will be saved in the `output/` directory in two formats:
- `extracted_resumes.csv`
- `extracted_resumes.json`