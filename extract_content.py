import docx
import json
import sys
import re

def clean_text(text):
    """Remove unwanted characters and whitespace."""
    return text.replace('{', '').replace('}', '').strip()

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
    except Exception as e:
        print(f"Error opening docx file: {e}", file=sys.stderr)
        return []

    data = []
    current_page = None
    current_section = None

    for para in doc.paragraphs:
        text = para.text.strip()

        # Use more flexible matching for page targets
        if 'PAGE CIBLE' in text or 'PAGE :' in text:
            if current_page:
                if current_section:
                    current_page['sections'].append(current_section)
                data.append(current_page)

            # Extract page title
            try:
                page_title = clean_text(text.split(':', 1)[1])
                current_page = {'page': page_title, 'sections': []}
                current_section = None
            except IndexError:
                print(f"WARN | Could not parse page title from: '{text}'", file=sys.stderr)
            continue

        # Use flexible matching for sections
        if 'SECTION :' in text:
            if current_page is None:
                print(f"WARN | Found section without a page target. Skipping. | Text: {text}", file=sys.stderr)
                continue

            if current_section:
                current_page['sections'].append(current_section)

            # Extract section title
            try:
                section_title = clean_text(text.split(':', 1)[1])
                current_section = {'title': section_title, 'content': []}
            except IndexError:
                 print(f"WARN | Could not parse section title from: '{text}'", file=sys.stderr)
            continue

        if current_section is not None and text and text not in ['}']:
            current_section['content'].append(text)

    if current_page:
        if current_section:
            current_page['sections'].append(current_section)
        data.append(current_page)

    return data

if __name__ == "__main__":
    docx_path = 'Contenus site Hawaii.docx'
    extracted_data = extract_text_from_docx(docx_path)

    if extracted_data:
        print(json.dumps(extracted_data, indent=4, ensure_ascii=False))
    else:
        print("WARN | No data was extracted. JSON output is empty.", file=sys.stderr)