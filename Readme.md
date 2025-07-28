# PDF Heading Extractor (Challenge 1A)

A containerized Python-based tool that semantically extracts and detects hierarchical headings (H1, H2, H3) from PDF documents with multilingual support.

---

## Features

- **Semantic Heading Detection**: Automatically identifies meaningful headings (H1, H2, H3) using contextual cues.
- **Multilingual Support**: Utilizes `sentence-transformers` to understand and process PDFs in multiple languages.
- **Dockerized**: Easily run in a containerized environment with no dependency conflicts.
- **Folder-Based Input/Output**: Reads from a given input folder and writes the processed output to a designated output directory.
- **Modular Design**: Easily extendable to include new models or formats (e.g., FastText support coming soon).

---

## Project Structure

```

CHALLENGE\_1A/
├── sample-dataset/
│   ├── pdfs/               # Place input PDFs here
│   ├── output/             # Output results saved here
│   └── schema/             # Optional schema definitions
├── Dockerfile
├── docker-compose.yml
├── process\_pdfs.py         # Core logic for PDF heading extraction
├── requirements.txt
└── README.md

````

---

## Setup & Usage

### Option 1: Run Using Docker (Recommended)

#### Step 1: Pull the Docker Image from Docker Hub

```bash
docker pull dhanush489/adobehackathon1a:1a
````

#### Step 2: Create Input and Output Folders

```
your-folder/
├── input/         # Place PDFs to be processed here
└── output/        # Processed results will appear here
```

#### Step 3: Run the Container

```bash
docker run --rm \
    -v "$(pwd)/input:/app/sample-dataset/pdfs:ro" \
    -v "$(pwd)/output:/app/sample-dataset/output" \
    --network none \
    dhanush489/adobehackathon1a:1a
```

---

### Option 2: 🧪 Run Locally via Python

#### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/pdf-heading-extractor.git
cd pdf-heading-extractor
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Process PDFs

Make sure your input PDFs are in `sample-dataset/pdfs`, then run:

```bash
python process_pdfs.py
```

Output will be saved in `sample-dataset/output`.

---

## 🔮 Future Enhancements

* ✅ Integrate [FastText](https://fasttext.cc/) for lightweight language detection.
* 🔍 Add OCR support for scanned PDFs to improve layout analysis.
* 📊 Export heading data in structured formats (JSON, CSV, XML).
* 📈 GUI or web interface for easier usage.

---
