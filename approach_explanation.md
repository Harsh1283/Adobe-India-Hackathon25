# 🧠 Approach Explanation – PDF Outline Extractor (Challenge 1a)

## Overview

The **PDF Outline Extractor** was designed to solve the problem of extracting semantic structure from PDF documents in a lightweight, efficient, and deterministic way—without relying on large machine learning models. This solution is fully rule-based and uses the powerful [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) library to analyze the visual and structural content of PDFs. Our methodology balances precision and performance, making it ideal for CPU-limited environments like local or Dockerized processing.

## Methodology

### 1. **Text Block Extraction**
We begin by reading each PDF from the `input/` directory using PyMuPDF (`fitz` module). For every page, the `get_text("blocks")` method is used to retrieve blocks of text, including positional and styling metadata such as font size, boldness, and coordinates.

### 2. **Heading Detection Heuristics**
The core of our approach lies in **layout-aware heuristics**:
- We collect font sizes for all text blocks and calculate the most frequent (mode) sizes across pages.
- Text blocks with significantly larger font sizes than the mode are considered **potential headings**.
- To further refine detection, we check for boldness and use textual patterns (e.g., numbered points, capitalization).
- We assign heading levels (`H1`, `H2`, etc.) based on relative font size rank and visual indentation.

This approach enables us to capture document hierarchy without needing OCR or ML models.

### 3. **Title Extraction**
The document title is inferred as the **largest, boldest text block on the first page**, typically placed centrally or at the top. This heuristic proves effective across structured forms, flyers, and formal documents.

### 4. **Robust Error Handling**
The extractor is designed to fail gracefully:
- If a document has no detectable headings, we still output an empty outline JSON with just the title.
- Parsing errors (corrupt or encrypted files) are caught and logged without crashing the entire batch.

### 5. **Output Format**
Each processed file generates a corresponding JSON in `output/`, following the provided schema:

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Heading Text", "page": 1 }
  ]
}
```

### Why This Approach?

- **Lightweight & Fast**: No ML inference, small memory footprint.
- **Cross-Document Compatibility**: Handles various formats like forms, RFPs, and flyers with consistent accuracy.
- **Explainable Logic**: Each heading decision is traceable based on font size and layout.

### Containerized Execution

The entire pipeline runs inside a Docker container built on Python 3.10. This ensures:

- **Platform Independence**: Works the same on Linux, Windows, and macOS.
- **No Setup Hassle**: Dependencies are isolated, ensuring reproducibility.

## Conclusion

This solution provides a deterministic, robust, and containerized approach for extracting outlines from diverse PDF documents using smart layout heuristics powered by PyMuPDF. It is fast, explainable, and perfectly suited for scalable, hackathon-grade challenges.