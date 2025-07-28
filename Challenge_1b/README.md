
# 🔍 Adobe India Hackathon 2025 – Semantic Document Retrieval Pipeline

This repository contains a lightweight, CPU-efficient semantic retrieval pipeline built for Adobe India Hackathon 2025, Challenge 1b. It processes PDF documents for three domains — 🧾 HR (Acrobat Tutorials), ✈️ Travel Planning, and 🍽️ Cooking — and answers user-specific tasks based on their persona.

---

## 🧠 Objective

Design a **fully offline** system that:
- Ingests PDF documents
- Extracts meaningful chunks
- Converts them to vector embeddings
- Performs **semantic similarity search**
- Returns answers in a structured JSON format

---

## 📁 Folder Structure

```
├── input/
│ ├── folder/ # Place all PDF files here
│ │ ├── South of France - X.pdf
│ │ ├── HR - Onboarding.pdf
│ ├── challenge1b_input.json # Place input JSON here
├── output/
│ └── (output.json generated here)
├── sentence_transformer_models/
│   └── all-MiniLM-L6-v2/   # Local MiniLM model directory
├── adobe_pipeline.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Component        | Tool Used                                 |
|------------------|-------------------------------------------|
| PDF Parser       | PyMuPDF (`fitz`)                          |
| Embeddings       | `all-MiniLM-L6-v2` (SentenceTransformers) |
| Vector Indexing  | FAISS (CPU)                               |
| Language         | Python 3.x                                |

---

## ✅ Features

- ✅ Chunking using layout-aware PDF parsing
- ✅ Sentence embeddings with MiniLM (under 1 GB)
- ✅ Real-time persona + task input
- ✅ Output in structured JSON format
- ✅ Fast execution on CPU (under 60 seconds)
- ❌ No internet required

---

## 🧪 Sample Personas and Tasks

| Persona         | Task                                                                 |
|-----------------|----------------------------------------------------------------------|
| HR Manager      | Create and manage fillable onboarding forms                          |
| Food Contractor | Prepare a vegetarian buffet-style dinner with gluten-free items      |
| Travel Planner  | Plan a 4-day South of France trip for 10 college friends             |

---

## 🐳 Docker Installation & Usage

### 1. **Build the Docker Image**

Open a terminal in your project folder and run:
```bash
docker build -t adobe-semantic-pipeline .
```

### 2. **Run the Pipeline in Docker**

To run and save output to your local folder:
```bash
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" adobe_pipeline_image python adobe_pipeline.py --input input/challenge1b_input.json --output output/output.json

```
- On Mac/Linux, use `$PWD` instead of `%cd%`.

💡 Make sure all PDFs are inside input/folder/
💡 You can change the --input JSON file name if needed (e.g., --input input/hr_case.json)


### 3. **Output**

After running, check your project folder for 
`output.json`.

### 4. **Note**
Ensure you have Docker installed and running on your machine.

---

## 📤 Output Format

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a 4-day trip",
    "processing_timestamp": "2025-07-26T12:34:56"
  },
  "extracted_sections": [
    {
      "document": "South of France - Tips.pdf",
      "page_number": 2,
      "section_title": "Packing Tips",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Tips.pdf",
      "refined_text": "Use packing cubes, bring layers, and carry reusable bags...",
      "page_number": 2
    }
  ]
}
```

---

## 📌 Constraints Satisfied

- ✅ Runs on **CPU only**
- ✅ Uses **< 1GB** model
- ✅ Processes 3–5 documents in **under 60 seconds**
- ✅ Requires **no internet access**

---

## 🏁 Authors & Credits

This project was developed as part of the **Adobe India Hackathon 2025** submission.  
Made with ❤️ using open-source tools like SentenceTransformers, FAISS, and PyMuPDF.

---
