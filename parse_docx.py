import re
from docx import Document

def parse_docx_for_manual_edit(file_path):
    """
    Parses the .docx file and prints the content in a readable format
    to be used for manual editing of the HTML files.
    """
    document = Document(file_path)
    current_page = None

    page_marker_regex = r'PAGE(?: CIBLE)?\s*:\s*([\w\-.]+\.html)'

    for para in document.paragraphs:
        text = para.text.replace('\xa0', ' ').strip()

        page_match = re.search(page_marker_regex, text, re.IGNORECASE)
        if page_match:
            current_page = page_match.group(1).strip()
            print("\n" + "="*80)
            print(f"PAGE: {current_page}")
            print("="*80)
            continue

        if current_page:
            print(text)

def main():
    docx_file = 'Contenus site Hawaii.docx'
    parse_docx_for_manual_edit(docx_file)

if __name__ == "__main__":
    main()