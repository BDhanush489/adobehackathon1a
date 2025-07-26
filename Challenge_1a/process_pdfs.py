# import os
# import json
# import re
# from pathlib import Path
# import fitz  # PyMuPDF

# def get_font_weight(font_name, cache):
#     name = font_name.lower()
#     if name in cache:
#         return cache[name]

#     weight = 400  # Default
#     if "thin" in name: weight = 100
#     elif "extralight" in name: weight = 200
#     elif "light" in name: weight = 300
#     elif "regular" in name: weight = 400
#     elif "medium" in name: weight = 500
#     elif "semibold" in name: weight = 600
#     elif "bold" in name: weight = 700
#     elif "extrabold" in name: weight = 800
#     elif "black" in name: weight = 900

#     match = re.search(r'(\d{3})$', name)
#     if match:
#         weight = int(match.group(1))

#     cache[name] = weight
#     return weight

# def detect_headings(pdf_path):
#     doc = fitz.open(pdf_path)
#     headings = []
#     font_weights = {}

#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#         blocks = page.get_text("dict").get("blocks", [])
#         page_width = page.rect.width
#         text_lines = []

#         for block in blocks:
#             for line in block.get("lines", []):
#                 spans = line.get("spans", [])
#                 if not spans:
#                     continue

#                 text = "".join(span.get("text", "") for span in spans).strip()
#                 if not text:
#                     continue

#                 bbox = line["bbox"]
#                 max_size = max(span.get("size", 0) for span in spans)
#                 max_weight = max(get_font_weight(span.get("font", ""), font_weights) for span in spans)

#                 left_margin = bbox[0]
#                 right_margin = bbox[2]
#                 center_threshold = page_width * 0.1
#                 is_centered = abs((left_margin + right_margin) / 2 - page_width / 2) < center_threshold

#                 text_lines.append({
#                     "text": text,
#                     "size": max_size,
#                     "weight": max_weight,
#                     "centered": is_centered,
#                     "page": page_num,
#                     "y_pos": bbox[1]
#                 })

#         if not text_lines:
#             continue

#         # ---------------------- H1 Detection ----------------------
#         h1_candidate = None
#         h1_score = 0

#         for line in text_lines:
#             # Skip weak or long lines (likely paragraph)
#             if line["weight"] < 500:
#                 continue
#             if len(line["text"]) > 100:
#                 continue

#             score = line["size"] * 10 + line["weight"] / 10
#             if line["centered"]:
#                 score *= 1.5

#             if score > h1_score:
#                 h1_score = score
#                 h1_candidate = line

#         if h1_candidate:
#             headings.append({
#                 "text": h1_candidate["text"],
#                 "level": "H1",
#                 "page": h1_candidate["page"],
#                 "y_pos": h1_candidate["y_pos"]
#             })

#         # ---------------------- H2 and H3 Detection ----------------------
#         remaining_lines = [line for line in text_lines if line != h1_candidate]

#         for line in remaining_lines:
#             # Skip short text, weak weight, or lines too long
#             if h1_candidate and line["size"] < h1_candidate["size"] * 0.7:
#                 continue
#             if line["weight"] < 500:
#                 continue
#             if len(line["text"]) > 120:
#                 continue

#             relative_score = (line["size"] * 10 + line["weight"] / 10)
#             if h1_candidate:
#                 relative_score /= h1_score

#             if relative_score > 0.8:
#                 level = "H2"
#             elif relative_score > 0.6:
#                 level = "H3"
#             else:
#                 continue

#             headings.append({
#                 "text": line["text"],
#                 "level": level,
#                 "page": line["page"],
#                 "y_pos": line["y_pos"]
#             })

#     # Sort headings top-down page-wise
#     headings.sort(key=lambda x: (x["page"], x["y_pos"]))
#     return headings

# def process_pdfs():
#     input_dir = Path("sample-dataset")
#     output_dir = Path("output")
#     output_dir.mkdir(parents=True, exist_ok=True)

#     pdf_files = list(input_dir.glob("*.pdf"))

#     for pdf_file in pdf_files:
#         print(f"🔍 Processing: {pdf_file.name}")
#         try:
#             headings = detect_headings(str(pdf_file))
#             title = headings[0]["text"] if headings else "Untitled"

#             output_data = {
#                 "title": title,
#                 "outline": [
#                     {
#                         "level": h["level"],
#                         "text": h["text"],
#                         "page": h["page"] + 1  # Convert to 1-based index
#                     }
#                     for h in headings
#                 ]
#             }

#             output_file = output_dir / f"{pdf_file.stem}.json"
#             with open(output_file, "w", encoding="utf-8") as f:
#                 json.dump(output_data, f, indent=2)

#             print(f"✅ Generated: {output_file.name}")

#         except Exception as e:
#             print(f"❌ Failed to process {pdf_file.name}: {e}")

# if __name__ == "__main__":
#     print("🚀 Starting PDF Processing")
#     process_pdfs()
#     print("🏁 Completed PDF Processing")


# WOrking
# import os
# import json
# import re
# from pathlib import Path
# import fitz  # PyMuPDF

# def get_font_weight(font_name, cache):
#     name = font_name.lower()
#     if name in cache:
#         return cache[name]

#     weight = 400
#     if "thin" in name: weight = 100
#     elif "extralight" in name: weight = 200
#     elif "light" in name: weight = 300
#     elif "regular" in name: weight = 400
#     elif "medium" in name: weight = 500
#     elif "semibold" in name: weight = 600
#     elif "bold" in name: weight = 700
#     elif "extrabold" in name: weight = 800
#     elif "black" in name: weight = 900

#     match = re.search(r'(\d{3})$', name)
#     if match:
#         weight = int(match.group(1))

#     cache[name] = weight
#     return weight

# def detect_headings_and_title(pdf_path):
#     doc = fitz.open(pdf_path)
#     headings = []
#     font_weights = {}

#     best_title = None
#     best_title_score = 0

#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#         blocks = page.get_text("dict").get("blocks", [])
#         page_width = page.rect.width
#         text_lines = []

#         for block in blocks:
#             for line in block.get("lines", []):
#                 spans = line.get("spans", [])
#                 if not spans:
#                     continue

#                 text = "".join(span.get("text", "") for span in spans).strip()
#                 if not text:
#                     continue

#                 bbox = line["bbox"]
#                 max_size = max(span.get("size", 0) for span in spans)
#                 max_weight = max(get_font_weight(span.get("font", ""), font_weights) for span in spans)

#                 left_margin = bbox[0]
#                 right_margin = bbox[2]
#                 center_threshold = page_width * 0.1
#                 is_centered = abs((left_margin + right_margin) / 2 - page_width / 2) < center_threshold

#                 line_data = {
#                     "text": text.strip(),
#                     "size": max_size,
#                     "weight": max_weight,
#                     "centered": is_centered,
#                     "page": page_num,
#                     "y_pos": bbox[1]
#                 }

#                 text_lines.append(line_data)

#                 # Title candidate: best weight × size
#                 score = max_size * max_weight
#                 if score > best_title_score:
#                     best_title_score = score
#                     best_title = text.strip()

#         if not text_lines:
#             continue

#         # H1
#         h1_candidate = None
#         h1_score = 0

#         for line in text_lines:
#             if line["weight"] < 500:
#                 continue
#             if len(line["text"]) > 100:
#                 continue

#             score = line["size"] * 10 + line["weight"] / 10
#             if line["centered"]:
#                 score *= 1.5

#             if score > h1_score:
#                 h1_score = score
#                 h1_candidate = line

#         if h1_candidate:
#             headings.append({
#                 "text": h1_candidate["text"],
#                 "level": "H1",
#                 "page": h1_candidate["page"],
#                 "y_pos": h1_candidate["y_pos"]
#             })

#         # H2, H3
#         remaining_lines = [line for line in text_lines if line != h1_candidate]

#         for line in remaining_lines:
#             if h1_candidate and line["size"] < h1_candidate["size"] * 0.7:
#                 continue
#             if line["weight"] < 500:
#                 continue
#             if len(line["text"]) > 120:
#                 continue

#             relative_score = (line["size"] * 10 + line["weight"] / 10)
#             if h1_candidate:
#                 relative_score /= h1_score

#             if relative_score > 0.8:
#                 level = "H2"
#             elif relative_score > 0.6:
#                 level = "H3"
#             else:
#                 continue

#             headings.append({
#                 "text": line["text"],
#                 "level": level,
#                 "page": line["page"],
#                 "y_pos": line["y_pos"]
#             })

#     headings.sort(key=lambda x: (x["page"], x["y_pos"]))
#     return best_title or "Untitled", headings

# def process_pdfs():
#     input_dir = Path("sample-dataset/pdfs")
#     output_dir = Path("sample-dataset/output")
#     output_dir.mkdir(parents=True, exist_ok=True)

#     pdf_files = list(input_dir.glob("*.pdf"))

#     for pdf_file in pdf_files:
#         print(f"🔍 Processing: {pdf_file.name}")
#         try:
#             title, headings = detect_headings_and_title(str(pdf_file))

#             output_data = {
#                 "title": title,
#                 "outline": [
#                     {
#                         "level": h["level"],
#                         "text": h["text"],
#                         "page": h["page"] + 1  # 1-based
#                     }
#                     for h in headings
#                 ]
#             }

#             output_file = output_dir / f"{pdf_file.stem}.json"
#             with open(output_file, "w", encoding="utf-8") as f:
#                 json.dump(output_data, f, indent=2, ensure_ascii=False)

#             print(f"✅ Generated: {output_file.name}")

#         except Exception as e:
#             print(f"❌ Failed to process {pdf_file.name}: {e}")

# if __name__ == "__main__":
#     print("🚀 Starting PDF Processing")
#     process_pdfs()
#     print("🏁 Completed PDF Processing")



# i have one issues 
# if there is a text that is bold but is followed by a numbering or bullets do not consider it as a h1 h2 or h3

# import os
# import json
# import re
# from pathlib import Path
# import fitz  # PyMuPDF
# from jsonschema import validate, ValidationError

# def get_font_weight(font_name, cache):
#     name = font_name.lower()
#     if name in cache:
#         return cache[name]

#     weight = 400
#     if "thin" in name: weight = 100
#     elif "extralight" in name: weight = 200
#     elif "light" in name: weight = 300
#     elif "regular" in name: weight = 400
#     elif "medium" in name: weight = 500
#     elif "semibold" in name: weight = 600
#     elif "bold" in name: weight = 700
#     elif "extrabold" in name: weight = 800
#     elif "black" in name: weight = 900

#     match = re.search(r'(\d{3})$', name)
#     if match:
#         weight = int(match.group(1))

#     cache[name] = weight
#     return weight

# def detect_headings_and_title(pdf_path):
#     doc = fitz.open(pdf_path)
#     headings = []
#     font_weights = {}

#     best_title = None
#     best_title_score = 0

#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#         blocks = page.get_text("dict").get("blocks", [])
#         page_width = page.rect.width
#         text_lines = []

#         for block in blocks:
#             for line in block.get("lines", []):
#                 spans = line.get("spans", [])
#                 if not spans:
#                     continue

#                 text = "".join(span.get("text", "") for span in spans).strip()
#                 if not text:
#                     continue

#                 bbox = line["bbox"]
#                 max_size = max(span.get("size", 0) for span in spans)
#                 max_weight = max(get_font_weight(span.get("font", ""), font_weights) for span in spans)

#                 left_margin = bbox[0]
#                 right_margin = bbox[2]
#                 center_threshold = page_width * 0.1
#                 is_centered = abs((left_margin + right_margin) / 2 - page_width / 2) < center_threshold

#                 line_data = {
#                     "text": text,
#                     "size": max_size,
#                     "weight": max_weight,
#                     "centered": is_centered,
#                     "page": page_num,
#                     "y_pos": bbox[1]
#                 }

#                 text_lines.append(line_data)

#                 # Track best title (biggest + boldest)
#                 score = max_size * max_weight
#                 if score > best_title_score:
#                     best_title_score = score
#                     best_title = text

#         if not text_lines:
#             continue

#         # ---- Detect H1 ----
#         h1_candidate = None
#         h1_score = 0

#         for line in text_lines:
#             if line["weight"] < 500:
#                 continue
#             if len(line["text"]) > 100:
#                 continue

#             score = line["size"] * 10 + line["weight"] / 10
#             if line["centered"]:
#                 score *= 1.5

#             if score > h1_score:
#                 h1_score = score
#                 h1_candidate = line

#         if h1_candidate:
#             headings.append({
#                 "text": h1_candidate["text"],
#                 "level": "H1",
#                 "page": h1_candidate["page"],
#                 "y_pos": h1_candidate["y_pos"]
#             })

#         # ---- Detect H2 and H3 ----
#         remaining_lines = [line for line in text_lines if line != h1_candidate]

#         for line in remaining_lines:
#             if line["weight"] < 500:
#                 continue
#             if len(line["text"]) > 120:
#                 continue
#             if h1_candidate and line["size"] < h1_candidate["size"] * 0.7:
#                 continue

#             rel_score = (line["size"] * 10 + line["weight"] / 10)
#             if h1_candidate:
#                 rel_score /= h1_score

#             if rel_score > 0.8:
#                 level = "H2"
#             elif rel_score > 0.6:
#                 level = "H3"
#             else:
#                 continue

#             headings.append({
#                 "text": line["text"],
#                 "level": level,
#                 "page": line["page"],
#                 "y_pos": line["y_pos"]
#             })

#     headings.sort(key=lambda x: (x["page"], x["y_pos"]))
#     return best_title or "Untitled", headings

# def process_pdfs():
#     input_dir = Path("sample-dataset/pdfs")
#     output_dir = Path("sample-dataset/output")
#     output_dir.mkdir(parents=True, exist_ok=True)

#     with open("schema.json") as f:
#         schema = json.load(f)

#     for pdf_file in input_dir.glob("*.pdf"):
#         print(f"🔍 Processing: {pdf_file.name}")
#         try:
#             title, headings = detect_headings_and_title(str(pdf_file))

#             output_data = {
#                 "title": title,
#                 "outline": [
#                     {
#                         "level": h["level"],
#                         "text": h["text"],
#                         "page": h["page"] + 1
#                     }
#                     for h in headings
#                 ]
#             }

#             validate(instance=output_data, schema=schema)

#             output_file = output_dir / f"{pdf_file.stem}.json"
#             with open(output_file, "w", encoding="utf-8") as f:
#                 json.dump(output_data, f, indent=2, ensure_ascii=False)

#             print(f"✅ Generated: {output_file.name}")

#         except ValidationError as ve:
#             print(f"❌ Schema validation failed: {ve.message}")
#         except Exception as e:
#             print(f"❌ Failed to process {pdf_file.name}: {e}")

# if __name__ == "__main__":
#     print("🚀 Starting PDF Processing")
#     process_pdfs()
#     print("🏁 Completed PDF Processing")


import os
import json
import re
from pathlib import Path
import fitz  # PyMuPDF
from jsonschema import validate, ValidationError

# -------- List Item Detection --------
LIST_LEADER_RE = re.compile(
    r"""
    ^\s*
    (?:
        (?:\(?\d+(?:\.\d+)*\)?[\.)]?)   # 1, 1., (1), 1.2.3
      | (?:[ivxlcdm]+[\.)])             # Roman numerals i., iv)
      | (?:[a-zA-Z][\.)])               # a), A., b)
      | [\-\u2013\u2014\*\u2022\u25AA\u25CF\u25E6]  # -, –, —, *, •, ▪, ●, ◦
    )
    \s+
    """,
    re.IGNORECASE | re.VERBOSE
)

def is_list_item(text: str) -> bool:
    text = text.strip()

    # Skip lines starting with bullets/dashes/numbers
    if LIST_LEADER_RE.match(text):
        return True

    # Skip lines where a bold phrase (possibly with commas) ends with ":" 
    # Example: "Cannes, Nice, and Saint-Tropez: ..."
    if re.match(r"^[A-ZÀ-ÿ][A-Za-zÀ-ÿ,'’\- ]+:\s", text):
        return True

    return False

# -------- Font Weight Detection --------
def get_font_weight(font_name, cache):
    name = font_name.lower()
    if name in cache:
        return cache[name]

    weight = 400
    if "thin" in name: weight = 100
    elif "extralight" in name: weight = 200
    elif "light" in name: weight = 300
    elif "regular" in name: weight = 400
    elif "medium" in name: weight = 500
    elif "semibold" in name: weight = 600
    elif "bold" in name: weight = 700
    elif "extrabold" in name: weight = 800
    elif "black" in name: weight = 900

    match = re.search(r'(\d{3})$', name)
    if match:
        weight = int(match.group(1))

    cache[name] = weight
    return weight

# -------- Headings and Title Detection --------
def detect_headings_and_title(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_weights = {}

    best_title = None
    best_title_score = 0

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict").get("blocks", [])
        page_width = page.rect.width
        text_lines = []

        for block in blocks:
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue

                text = "".join(span.get("text", "") for span in spans).strip()
                if not text:
                    continue

                bbox = line["bbox"]
                max_size = max(span.get("size", 0) for span in spans)
                max_weight = max(get_font_weight(span.get("font", ""), font_weights) for span in spans)

                left_margin = bbox[0]
                right_margin = bbox[2]
                center_threshold = page_width * 0.1
                is_centered = abs((left_margin + right_margin) / 2 - page_width / 2) < center_threshold

                line_data = {
                    "text": text,
                    "size": max_size,
                    "weight": max_weight,
                    "centered": is_centered,
                    "page": page_num,
                    "y_pos": bbox[1]
                }

                text_lines.append(line_data)

                # Track best title (biggest + boldest)
                score = max_size * max_weight
                if score > best_title_score:
                    best_title_score = score
                    best_title = text

        if not text_lines:
            continue

        # ---- Detect H1 ----
        h1_candidate = None
        h1_score = 0

        for line in text_lines:
            if is_list_item(line["text"]):  # Skip bullets/numbered items
                continue
            if line["weight"] < 500:
                continue
            if len(line["text"]) > 100:
                continue

            score = line["size"] * 10 + line["weight"] / 10
            if line["centered"]:
                score *= 1.5

            if score > h1_score:
                h1_score = score
                h1_candidate = line

        if h1_candidate:
            headings.append({
                "text": h1_candidate["text"],
                "level": "H1",
                "page": h1_candidate["page"],
                "y_pos": h1_candidate["y_pos"]
            })

        # ---- Detect H2 and H3 ----
        remaining_lines = [line for line in text_lines if line != h1_candidate]

        for line in remaining_lines:
            if is_list_item(line["text"]):  # Skip bullets/numbered items
                continue
            if line["weight"] < 500:
                continue
            if len(line["text"]) > 120:
                continue
            if h1_candidate and line["size"] < h1_candidate["size"] * 0.7:
                continue

            rel_score = (line["size"] * 10 + line["weight"] / 10)
            if h1_candidate:
                rel_score /= h1_score

            if rel_score > 0.8:
                level = "H2"
            elif rel_score > 0.6:
                level = "H3"
            else:
                continue

            headings.append({
                "text": line["text"],
                "level": level,
                "page": line["page"],
                "y_pos": line["y_pos"]
            })

    headings.sort(key=lambda x: (x["page"], x["y_pos"]))
    return best_title or "Untitled", headings

# -------- Process PDFs --------
def process_pdfs():
    input_dir = Path("sample-dataset/pdfs")
    output_dir = Path("sample-dataset/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open("sample-dataset/schema/schema.json") as f:
        schema = json.load(f)

    for pdf_file in input_dir.glob("*.pdf"):
        print(f"🔍 Processing: {pdf_file.name}")
        try:
            title, headings = detect_headings_and_title(str(pdf_file))

            output_data = {
                "title": title,
                "outline": [
                    {
                        "level": h["level"],
                        "text": h["text"],
                        "page": h["page"] + 1
                    }
                    for h in headings
                ]
            }

            validate(instance=output_data, schema=schema)

            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Generated: {output_file.name}")

        except ValidationError as ve:
            print(f"❌ Schema validation failed: {ve.message}")
        except Exception as e:
            print(f"❌ Failed to process {pdf_file.name}: {e}")

if __name__ == "__main__":
    print("🚀 Starting PDF Processing")
    process_pdfs()
    print("🏁 Completed PDF Processing")
