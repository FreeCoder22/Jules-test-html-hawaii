import docx
import re
import os

def get_target_file_from_paragraph(paragraph):
    """
    Checks if a paragraph is a target file marker.
    Handles variations like:
    - {PAGE CIBLE: demo-it-business.html}
    - PAGE : demo-it-business.html {
    - PAGE CIBLE : demo-it-business-about.html {
    """
    # More flexible regex
    match = re.search(r'PAGE (?:CIBLE)?\s*:\s*([\w.-]+)', paragraph.text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Original regex for the {PAGE CIBLE:...} format
    match = re.search(r'{PAGE CIBLE:(.*?)}', paragraph.text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return None

def parse_docx(file_path):
    """
    Parses the docx file and returns a dictionary with page content.
    """
    doc = docx.Document(file_path)
    pages = {}
    current_page = None
    content = []

    for para in doc.paragraphs:
        target_file = get_target_file_from_paragraph(para)
        if target_file:
            if current_page:
                # Join content, but remove the closing brace from the last line if it exists
                full_content = "\n".join(content).strip()
                if full_content.endswith("}"):
                    full_content = full_content[:-1].strip()
                pages[current_page] = full_content
            current_page = target_file
            content = []
        elif current_page:
            content.append(para.text)

    if current_page:
        full_content = "\n".join(content).strip()
        if full_content.endswith("}"):
            full_content = full_content[:-1].strip()
        pages[current_page] = full_content


    return pages

if __name__ == "__main__":
    pages_content = parse_docx('Contenus site Hawaii.docx')
    for page, content in pages_content.items():
        print(f"--- Page: {page} ---")
        print(content[:300] + "...")
        print("\n")