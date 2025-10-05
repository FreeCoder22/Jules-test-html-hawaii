import docx
import re
import json

def get_text(filename):
    doc = docx.Document(filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def parse_content(text):
    pages = {}
    # Make the "CIBLE" part optional in the regex
    page_regex = re.compile(r"PAGE\s*(?:CIBLE)?\s*:\s*(.*?)\s*{", re.IGNORECASE)
    section_regex = re.compile(r"SECTION\s*:\s*(.*)", re.IGNORECASE)

    # Splitting the text by page markers
    parts = page_regex.split(text)

    page_names = parts[1::2]
    page_contents = parts[2::2]

    for i, page_name in enumerate(page_names):
        page_name = page_name.strip()
        content = page_contents[i]

        sections_raw = section_regex.split(content)

        sections = []
        # The first element is the content before the first section
        # Then it's title, content, title, content, ...
        for j in range(1, len(sections_raw), 2):
            title = sections_raw[j].strip()
            section_content = sections_raw[j+1].strip().split('}')[0] # Stop at the closing brace of the page

            # Clean up content
            lines = [line.strip() for line in section_content.split('\n') if line.strip()]
            cleaned_content = '\n'.join(lines)

            sections.append({
                "title": title,
                "content": cleaned_content
            })

        pages[page_name] = sections

    return pages

if __name__ == "__main__":
    file_path = 'Contenus site Hawaii.docx'
    text_content = get_text(file_path)
    parsed_data = parse_content(text_content)

    # Print the parsed data in a readable format
    print(json.dumps(parsed_data, indent=2, ensure_ascii=False))