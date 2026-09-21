import pymupdf

def extract_lines(pdf_bytes: bytes) -> list[dict]:
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    lines = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text:
                    continue
                bbox = line["bbox"]  # (x0, y0, x1, y1)
                lines.append({
                    "text": text,
                    "page": page_num,
                    "bbox": bbox,
                })

    doc.close()
    return lines
