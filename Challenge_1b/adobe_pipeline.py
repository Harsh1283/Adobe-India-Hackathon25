# Adobe Semantic Retrieval Pipeline (Updated for JSON Input)

import os
import json
import argparse
from datetime import datetime
from typing import List, Dict
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load locally saved model
MODEL_PATH = "sentence_transformer_models/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_PATH, device="cpu")


def extract_chunks_from_pdf(file_path: str) -> List[Dict]:
    doc = fitz.open(file_path)
    chunks = []
    for i, page in enumerate(doc):
        blocks = page.get_text("blocks")
        for b in blocks:
            text = b[4].strip()
            if len(text) > 100:
                chunks.append({
                    "text": text,
                    "page_number": i + 1,
                    "document": os.path.basename(file_path)
                })
    return chunks


def build_faiss_index(chunks: List[Dict]):
    texts = [c['text'] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype='float32'))
    for i, emb in enumerate(embeddings):
        chunks[i]['embedding'] = emb
    return index, chunks


def semantic_search(query: str, index, chunks, top_k=5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding, dtype='float32'), top_k)
    return [chunks[idx] for idx in I[0]]


def build_output_json(input_docs, persona, task, top_chunks):
    now = datetime.now().isoformat()
    return {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona,
            "job_to_be_done": task,
            "processing_timestamp": now
        },
        "extracted_sections": [
            {
                "document": c['document'],
                "page_number": c['page_number'],
                "section_title": c['text'][:80],
                "importance_rank": i + 1
            }
            for i, c in enumerate(top_chunks)
        ],
        "subsection_analysis": [
            {
                "document": c['document'],
                "refined_text": c['text'],
                "page_number": c['page_number']
            }
            for c in top_chunks
        ]
    }


def load_input_json(input_path: str):
    with open(input_path, "r") as f:
        data = json.load(f)

    persona = data["persona"]["role"]
    task = data["job_to_be_done"]["task"]
    files = [doc["filename"] for doc in data["documents"]]
    folders = list(set([os.path.dirname(f) for f in files]))
    return folders, persona, task, files


def run_adobe_pipeline(folder_paths: List[str], persona: str, task: str, allowed_files=None, top_k: int = 5) -> Dict:
    all_chunks = []
    input_files = []

    for folder in folder_paths:
        for fname in os.listdir(folder):
            if fname.endswith(".pdf"):
                full_path = os.path.join(folder, fname)
                rel_path = os.path.join(folder, fname)
                if allowed_files is None or rel_path in allowed_files or fname in allowed_files:
                    chunks = extract_chunks_from_pdf(full_path)
                    all_chunks.extend(chunks)
                    input_files.append(rel_path)

    if not all_chunks:
        raise ValueError("No valid PDF content found to process.")

    faiss_index, enriched_chunks = build_faiss_index(all_chunks)
    query = f"{persona} wants to: {task}"
    top_chunks = semantic_search(query, faiss_index, enriched_chunks, top_k)
    result_json = build_output_json(input_files, persona, task, top_chunks)
    return result_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help="Path to input JSON")
    parser.add_argument('--output', default="output.json", help="Path to output JSON")
    args = parser.parse_args()

    # Load input JSON
    input_data = json.load(open(args.input, "r"))
    documents = input_data.get("documents", [])
    folder_path = os.path.join("input", "folders")
    folders = [folder_path]
    
    persona = input_data["persona"]["role"]
    task = input_data["job_to_be_done"]["task"]
    file_whitelist = [doc["filename"] for doc in documents]

    output = run_adobe_pipeline(folders, persona, task, allowed_files=file_whitelist)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Pipeline completed. Output saved to '{args.output}'")
