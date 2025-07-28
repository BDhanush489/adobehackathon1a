# Challenge 1a: PDF Processing Solution

## Overview
This project presents a solution for Challenge 1a of the Adobe India Hackathon 2025: "Connecting the Dots". The core objective is to build a PDF processing solution that extracts a structured outline, including the document title and headings (H1, H2, H3), from PDF files and outputs them in a specified JSON format. The solution is containerized using Docker and is designed to meet specific performance and resource constraints, focusing on on-device intelligence without external network calls.


## Solution Approach (process_pdfs.py)

The process_pdfs.py script is designed to extract structural information from PDF documents using PyMuPDF and generate a hierarchical outline in JSON format.

*Key features include:*

  * *Font Analysis:* Analyzes font size and weight to identify potential headings. A higher score is assigned to larger and bolder text.
  * *Centering Detection:* Prioritizes text that is centered, as this often indicates higher-level headings like a document title or H1.
  * *List Item Filtering:* Implements logic to specifically exclude lines that appear to be list items (e.g., bullet points, numbered lists) from being classified as headings, even if they are bold.
  * *Hierarchical Structuring:* Classifies detected headings into H1, H2, and H3 based on their calculated score relative to the highest-scoring candidate on the page.
  * *JSON Output Generation:* Produces a JSON file for each PDF, containing the document title and an array of outline entries, each with its level, text, and page number (1-based index).
  * *Schema Validation:* Validates the generated JSON output against sample-dataset/schema/schema.json to ensure it conforms to the required structure.

## Models and Libraries Used

The solution utilizes the following Python libraries, as defined in requirements.txt:

  * PyMuPDF (fitz): For robust PDF parsing and text extraction.
  * jsonschema: For validating the generated JSON output against the provided schema.
  * sentence-transformers, scikit-learn, transformers, torch: These are listed in requirements.txt from the provided context, suggesting potential future use for semantic analysis (e.g., in Round 1B) though not explicitly used for heading detection in process_pdfs.py for Round 1A. The solution adheres to the model size and CPU-only constraints.


## Sample Docker Configuration

The Dockerfile provided for this solution is:

dockerfile
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY process_pdfs.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "process_pdfs.py"]


## Output Format

Each PDF processed will generate a corresponding JSON file that strictly conforms to the schema defined in sample-dataset/schema/schema.json. An example output structure is:

json
{
  "title": "A Comprehensive Guide to Traditions and Culture in the South of France",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Language and Literature", "page": 2},
    { "level": "H3", "text": "Provençal Language", "page":2}
  ]
}


## Implementation Guidelines

### Quick Start (Running Procedure) 

## Using Pre-built Docker Image

1.  *Navigate to a new Directory:*
    bash
    cd <your-working-directory>
    
2.  *Pull the pre-built Docker image:*
    bash
    docker pull dhanush489/adobehackathon1a:1a
    
3.  *Run the container*
    bash
    docker run --rm -v "C:\Path\to\input:/app/sample-dataset/pdfs:ro" \
               -v "C:\Path\to\output:/app/sample-dataset/output" \
               --network none dhanush489/adobehackathon1a:1a

        Replace C:\Path\to\input with the absolute path of your input PDF directory.

        Replace C:\Path\to\output with the directory where output JSONs should be saved.

### Validation Checklist

  * All PDFs in the input directory are processed.
  * JSON output files are generated for each PDF in the output directory.
  * Output format matches the required structure (title, outline with level, text, page).
  * Output conforms to the schema in sample-dataset/schema/schema.json.
  * Processing completes within 10 seconds for 50-page PDFs.
  * Solution works without internet access during execution.
  * Memory usage stays within the 16GB limit.
  * Compatible with AMD64 architecture.
