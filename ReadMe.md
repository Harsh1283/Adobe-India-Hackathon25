# Adobe India Hackathon 2025 – Challenge 1a: PDF Outline Extractor

Welcome to the PDF Outline Extractor – a solution crafted for the Adobe India Hackathon 2025!  
This project automatically analyzes PDF documents and generates structured outlines in JSON format, making it easier to understand, search, and process large sets of documents.

## 🧑‍💻 What Does This Project Do?

- **Reads PDFs** from the `input/` folder.
- **Extracts headings, titles, and structure** using advanced text and style analysis.
- **Outputs a JSON file** for each PDF in the `output/` folder, capturing the document's outline and title.
- Designed for **robustness**: works with forms, flyers, reports, and complex documents (like RFPs).

## 📁 Project Structure

Challenge_1a/
├── dataset/
│   ├── outputs/         # JSON files provided as outputs.
│   ├── input/            # Input PDF files
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Sample processing script
└── README.md           # This file


- `input/`: Place your PDF files here.
- `output/`: Extracted outlines will be saved here as JSON.
- `process_pdf.py`: Main script for PDF processing.
- `requirements.txt`: Python dependencies (uses PyMuPDF).
- `Dockerfile`: Container setup for easy cross-platform execution.

## 🚀 How to Run (Linux & Windows, Dockerized)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system.
- Your PDFs placed in the `input/` folder.

### 1. Build the Docker Image

Open a terminal (Linux) or Command Prompt/PowerShell (Windows) in the project directory and run:

```sh
docker build -t pdf-outline-extractor .

2. Run the Docker Container

on Linux:
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  pdf-outline-extractor

on Windows:
docker run --rm ^
  -v "%cd%/input:/app/input" ^
  -v "%cd%/output:/app/output" ^
  pdf-outline-extractor

The container will process all PDFs in input/ and write JSON outlines to output/.

📝 Example Output
Each output JSON contains:

title: The detected document title.
outline: List of headings with their level and page number.
{
  "title": "Application form for grant of LTC advance",
  "outline": [
    { "level": "H1", "text": "1. Name of the Government Servant", "page": 1 },
    ...
  ]
}

🤖 How Does It Work?
-This project leverages the power of PyMuPDF to read and analyze PDF documents. It extracts text blocks, identifies font sizes, and checks for boldness to determine headings and their structure. The script is designed to adapt to various document types, including forms, reports, and flyers, ensuring robust performance across different formats.

-Uses PyMuPDF to parse PDFs.
-Analyzes text blocks, font sizes, and boldness to detect headings and structure.
-Adapts to different document types (forms, reports, flyers).
-Handles errors gracefully – if a PDF can't be processed, an empty outline is saved.

💡 Why Use Docker?

-No dependency hell: Everything runs in a clean Python 3.10 environment.
-Cross-platform: Works the same on Linux, Windows, or Mac.
-Easy to share and reproduce: Just share your code and Dockerfile!

📚 References
Adobe India Hackathon 2025 Challenge 1a
PyMuPDF Documentation
🙌 Authors & Credits
Crafted for the Adobe India Hackathon 2025.
Inspired by the challenge to make document understanding easier for everyone.

