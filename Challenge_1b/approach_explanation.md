
# 🧠 Challenge 1B – Detailed Technical Approach

## 🔍 Problem Statement Summary
Given a directory structure where multiple folders (e.g., cook, travel, hr) contain multiple PDFs, extract meaningful content chunks from each PDF for further semantic processing. The system should:

- Efficiently parse multiple PDFs per category
- Filter noise and short/non-informative texts
- Be layout-aware (respect blocks and headings)
- Maintain folder-level metadata

---

## ⚙️ Core Pipeline Overview

1. **Directory Traversal**
2. **PDF Reading & Chunk Extraction**
3. **Filtering and Heuristics**
4. **Metadata Association**
5. **Storage or Output**

---

## 📁 1. Directory Traversal

Use Python’s `os` module or `Pathlib` to recursively walk through all folders (e.g., `cook/`, `travel/`, etc.) and collect paths to all `.pdf` files.

```python
from pathlib import Path

pdf_paths = list(Path(base_dir).rglob("*.pdf"))
```

---

## 📄 2. PDF Reading & Chunk Extraction

Use **PyMuPDF (`fitz`)** to open each PDF and extract **block-level content** from each page.

```python
import fitz  # PyMuPDF

doc = fitz.open(pdf_path)
for page in doc:
    blocks = page.get_text("blocks")  # Returns layout-aware text blocks
```

Each `block` is a tuple, where `block[4]` contains the actual text.

---

## 🧹 3. Filtering and Heuristics

We filter out blocks based on simple heuristics:

- Ignore empty or whitespace-only blocks
- Skip blocks with less than a threshold (e.g., 50 characters)
- Strip noisy characters

```python
if len(text.strip()) > 100:
    chunks.append({
        "text": text.strip(),
        "page": i + 1,
        "file": pdf_path.name
    })
```

---

## 🏷️ 4. Metadata Association

Each chunk includes the following metadata:

- PDF filename
- Page number
- Folder (category like `cook`, `hr`, etc.) if needed

You can extend chunk objects like:

```python
{
    "text": "...",
    "page": 2,
    "file": "doc1.pdf",
    "category": "cook"
}
```

---

## 💾 5. Output Format

All chunks are collected in a Python list and can be:

- Stored in a JSON/CSV for later use
- Sent to a vector store for semantic search
- Passed into a transformer pipeline

---

## 🧠 Key Notes

- This approach is **lightweight** and **does not require ML**.
- Fully works on CPU — fast enough for batch processing PDFs.
- Can be scaled for 1000s of documents.

---

## 🤖 Transformer Integration (Optional)

The extracted chunks can optionally be encoded using Sentence Transformers (`all-MiniLM-L6-v2`) for retrieval or classification.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode([chunk["text"] for chunk in chunks])
```

---

## ✅ Summary

This pipeline is:
- Fast ✅
- Robust ✅
- Layout-aware ✅
- Semantic-ready ✅

It fulfills the requirements of Challenge 1B in a scalable, modular way.
