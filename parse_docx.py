import docx
import json
import re

def parse_word_document(file_path):
    """
    Parses a Word document to extract content for website pages using a two-pass method.

    Args:
        file_path (str): The path to the Word document.

    Returns:
        dict: A dictionary with page names as keys and a list of sections as values.
    """
    doc = docx.Document(file_path)
    # Filter out empty paragraphs from the start
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    pages = {}
    page_indices = []
    page_regex = re.compile(r'(?:PAGE CIBLE|PAGE)\s*:\s*([^\s}]+)', re.IGNORECASE)

    # 1. First pass: Find all page boundaries
    for i, p_text in enumerate(paragraphs):
        match = page_regex.search(p_text)
        if match:
            page_name = match.group(1).strip().replace('}','').strip()
            # Ensure we have a valid page name, not just noise
            if ' ' in page_name or len(page_name) < 3: continue
            page_indices.append({'name': page_name, 'start': i})

    if not page_indices:
        return {}

    # Define the end boundary for each page
    for i in range(len(page_indices) - 1):
        page_indices[i]['end'] = page_indices[i+1]['start']
    page_indices[-1]['end'] = len(paragraphs)

    section_regex = re.compile(r'section\s*:\s*([^}]+)', re.IGNORECASE)

    # 2. Second pass: Process each page to find sections
    for page_info in page_indices:
        page_name = page_info['name']
        # Slice the paragraphs for the current page, excluding the page marker itself
        page_paragraphs = paragraphs[page_info['start'] + 1 : page_info['end']]

        sections = []
        section_indices = []

        # Find section boundaries within the current page's paragraphs
        for i, p_text in enumerate(page_paragraphs):
            match = section_regex.search(p_text)
            if match:
                section_title = match.group(1).strip().replace('}','').strip()
                # Ensure we have a valid section title
                if section_title:
                    section_indices.append({'title': section_title, 'start': i})

        if not section_indices:
            # Case: No explicit section markers found.
            # Treat the whole page block as a single section.
            if page_paragraphs:
                # Remove closing brace if it's the last line
                if page_paragraphs[-1] == '}':
                    page_paragraphs.pop()

                if page_paragraphs:
                    # Assume the first paragraph is the title and the rest is content
                    section_title = page_paragraphs[0]
                    section_content = '\n'.join(page_paragraphs[1:])
                    sections.append({'title': section_title, 'content': section_content})
        else:
            # Case: Explicit section markers found.
            # Define end boundary for each section
            for i in range(len(section_indices) - 1):
                section_indices[i]['end'] = section_indices[i+1]['start']
            section_indices[-1]['end'] = len(page_paragraphs)

            for sec_info in section_indices:
                sec_title = sec_info['title']
                # Get paragraphs between the section marker and the next one (or page end)
                sec_paragraphs = page_paragraphs[sec_info['start'] + 1 : sec_info['end']]

                if sec_paragraphs and sec_paragraphs[-1] == '}':
                    sec_paragraphs.pop()

                sec_content = '\n'.join(p for p in sec_paragraphs if p)
                sections.append({'title': sec_title, 'content': sec_content})

        if sections:
            pages[page_name] = sections

    return pages

if __name__ == "__main__":
    parsed_data = parse_word_document('Contenus site Hawaii.docx')
    with open('parsed_content.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)
    print("Content parsed and saved to parsed_content.json")