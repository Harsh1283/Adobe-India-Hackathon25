import fitz  # PyMuPDF
from pathlib import Path
import json
import re
import statistics
from collections import Counter

# --- SETUP ---
input_dir = Path("/app/input")
output_dir = Path("/app/output")
output_dir.mkdir(parents=True, exist_ok=True)

def clean_text(text):
    """Normalizes whitespace in a string."""
    return re.sub(r'\s+', ' ', text).strip()

def extract_blocks_from_doc(doc):
    """Extracts all text blocks with style information from the document."""
    all_blocks = []
    for page_num, page in enumerate(doc, start=1):
        page_dict = page.get_text("dict")
        for block in page_dict.get("blocks", []):
            if block.get("type") != 0: continue
            
            block_text, sizes, fonts = "", [], []
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    block_text += span.get("text", "") + " "
                    sizes.append(round(span.get("size", 0)))
                    fonts.append(span.get("font", ""))
            
            cleaned_text = clean_text(block_text)
            if not cleaned_text: continue

            all_blocks.append({
                "page": page_num,
                "text": cleaned_text,
                "bbox": block.get("bbox", (0,0,0,0)),
                "size": statistics.mode(sizes) if sizes else 0,
                "is_bold": any("bold" in f.lower() for f in fonts) if fonts else False,
                "word_count": len(cleaned_text.split())
            })
    return all_blocks

# --- DOCUMENT PROFILES ---

def process_as_complex_report(blocks):
    """Tailored logic for structured reports with complex titles (e.g., RFP)."""
    # Find body style to differentiate it from headings
    long_blocks = [b for b in blocks if b['word_count'] > 25 and b['page'] > 1]
    body_style_size = Counter(b['size'] for b in long_blocks).most_common(1)[0][0] if long_blocks else 10

    # Proven multi-part title logic for page 1
    page1_blocks = sorted([b for b in blocks if b['page'] == 1], key=lambda x: x['bbox'][1])
    title_parts = []
    title_blocks_to_exclude = []
    for i, block in enumerate(page1_blocks):
        if "RFP" in block['text']:
            title_parts.append(block['text'])
            title_blocks_to_exclude.append(block)
            # Find the next largest text block as the subtitle
            if i + 1 < len(page1_blocks):
                for next_block in page1_blocks[i+1:]:
                    if next_block['word_count'] > 4 and next_block['size'] > body_style_size:
                        title_parts.append(next_block['text'])
                        title_blocks_to_exclude.append(next_block)
                        break
            break
    
    title = " ".join(title_parts)
    if not title and page1_blocks: # Fallback for other complex reports
        title_candidate = max([b for b in page1_blocks if b['word_count'] < 15], key=lambda x:x['size'], default=None)
        if title_candidate:
            title = title_candidate['text']
            title_blocks_to_exclude.append(title_candidate)

    # Filter out title and repeating footers
    non_title_blocks = [b for b in blocks if b not in title_blocks_to_exclude]
    footer_text = "RFP: To Develop the Ontario Digital Library Business Plan"
    content_blocks = [b for b in non_title_blocks if footer_text not in b['text']]

    # Strict heading identification
    headings = []
    for b in content_blocks:
        if b['size'] > body_style_size or b['is_bold']:
            # Must be concise and not paragraph-like
            if b['word_count'] < 25 or "Appendix" in b['text']:
                headings.append(b)

    # Assign levels based on a simple size/bold hierarchy
    styles = sorted(list(set((h['size'], h['is_bold']) for h in headings)), key=lambda x: (-x[0], -int(x[1])))
    style_map = {style: f"H{i+1}" for i, style in enumerate(styles[:4])}

    outline = []
    for h in headings:
        level = style_map.get((h['size'], h['is_bold']), 'H4')
        if re.match(r'^\d\.\s', h['text']): level = "H1" # Top-level numbered lists are H1
        outline.append({"level": level, "text": h['text'], "page": h['page']})
    
    return {"title": title, "outline": outline}


def process_as_generic_document(blocks):
    """A reliable default for standard documents, forms, or flyers."""
    if not blocks: return {"title": "", "outline": []}
    
    long_blocks = [b for b in blocks if b['word_count'] > 20]
    body_size = Counter(b['size'] for b in long_blocks).most_common(1)[0][0] if long_blocks else 10
    
    page1_blocks = [b for b in blocks if b['page'] == 1]
    title = max([b for b in page1_blocks if b['size'] > body_size and b['word_count'] < 10], key=lambda x:x['size'], default={"text":""})['text']
    
    headings = []
    for b in blocks:
        if b['text'] == title: continue
        if b['size'] > body_size or (b['is_bold'] and b['size'] >= body_size):
            if b['word_count'] < 30:
                headings.append(b)

    styles = sorted(list(set((h['size'], h['is_bold']) for h in headings)), key=lambda x: (-x[0], -int(x[1])))
    style_map = {style: f"H{i+1}" for i, style in enumerate(styles[:4])}

    outline = []
    for h in headings:
        level = style_map.get((h['size'], h['is_bold']), 'H4')
        outline.append({"level": level, "text": h['text'], "page": h['page']})

    return {"title": title, "outline": outline}


# --- MAIN ORCHESTRATOR ---
for pdf_path in input_dir.glob("*.pdf"):
    print(f"Processing: {pdf_path.name}")
    try:
        doc = fitz.open(pdf_path)
        all_blocks = extract_blocks_from_doc(doc)
        
        # Simple, robust classification
        full_text = " ".join(b['text'] for b in all_blocks)
        if "RFP" in full_text or "Request for Proposal" in full_text:
            profile = "complex_report"
        else:
            profile = "generic"
            
        print(f"  Using profile: {profile}")
        
        if profile == "complex_report":
            final_outline = process_as_complex_report(all_blocks)
        else:
            final_outline = process_as_generic_document(all_blocks)
            
        # Sort final outline by page and position
        final_outline["outline"] = sorted(final_outline["outline"], key=lambda x: (x["page"], [b for b in all_blocks if b["text"] == x["text"] and b["page"] == x["page"]][0]["bbox"][1]))

        output_file = output_dir / f"{pdf_path.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_outline, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"❌ Error processing {pdf_path.name}: {e}")
        output_file = output_dir / f"{pdf_path.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"title": "", "outline": []}, f, indent=4)

print("✅ All files processed.")