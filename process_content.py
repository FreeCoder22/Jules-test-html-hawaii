import re
import os
from docx import Document
from bs4 import BeautifulSoup

def parse_docx(file_path):
    """
    Parses the .docx file and extracts content for each page and section.
    This version is more robust to handle variations in the document's formatting.
    """
    document = Document(file_path)
    content = {}
    current_page = None
    current_section = None
    section_content = []
    in_page_block = False

    # A more robust regex that handles "PAGE CIBLE" or "PAGE"
    page_marker_regex = r'PAGE(?: CIBLE)?\s*:\s*([\w\-.]+\.html)'

    for para in document.paragraphs:
        text = para.text.replace('\xa0', ' ').strip()

        # Match the start of a new page block
        page_match = re.search(page_marker_regex, text, re.IGNORECASE)
        if page_match:
            if current_page and current_section: # Save previous section if any
                content[current_page][current_section] = "\n".join(section_content).strip()

            current_page = page_match.group(1).strip()
            content[current_page] = {}
            current_section = None
            section_content = []
            in_page_block = "{" in text
            continue

        # Handle cases where '{' is on a new line
        if not in_page_block and text.strip() == '{' and current_page:
            in_page_block = True
            continue

        # Handle end of page block
        if in_page_block and text.strip() == '}':
            if current_page and current_section:
                content[current_page][current_section] = "\n".join(section_content).strip()
            in_page_block = False
            current_page = None
            current_section = None
            continue

        if not in_page_block or not text:
            continue

        # Match the start of a new section
        section_match = re.match(r'SECTION\s*:\s*(.*)', text, re.IGNORECASE)
        if section_match:
            if current_page and current_section:
                content[current_page][current_section] = "\n".join(section_content).strip()

            current_section = section_match.group(1).strip()
            content[current_page][current_section] = ""
            section_content = []
            continue

        # If it's the first line of content without a section marker, treat it as the first section
        if current_page and not current_section:
            current_section = text
            content[current_page][current_section] = ""
            section_content = []
            continue

        # Append content to the current section
        if current_page and current_section:
            section_content.append(text)

    if current_page and current_section:
        content[current_page][current_section] = "\n".join(section_content).strip()

    return content

def update_homepage_hero(file_path, hero_section_content):
    """
    Updates the hero section of the homepage with new content.
    """
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    hero_section = soup.find('section', class_='cover-background')
    if not hero_section:
        print("Error: Hero section not found in homepage.")
        return

    lines = hero_section_content.split('\n')
    title = lines[0]
    subtitle = lines[1] if len(lines) > 1 else ""
    buttons_text = [b.strip() for b in re.findall(r'\[(.*?)\]', hero_section_content)]

    h1 = hero_section.find('h1')
    if h1:
        h1.string = title
        print(f"Updated hero title to: {title}")

    p = hero_section.find('p', class_='opacity-6')
    if p:
        p.string = subtitle
        print(f"Updated hero subtitle to: {subtitle}")

    buttons = hero_section.find_all('a', class_='btn')
    if len(buttons) >= 2 and len(buttons_text) >= 2:
        for i, text in enumerate(buttons_text):
            btn_text_span = buttons[i].find('span', class_='btn-double-text')
            if btn_text_span:
                btn_text_span['data-text'] = text
                btn_text_span.string = text
                print(f"Updated button {i+1} text to: {text}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    print(f"Successfully updated hero section in {file_path}")

def main():
    """
    Main function to orchestrate the content update process.
    """
    docx_file = 'Contenus site Hawaii.docx'
    homepage_file = 'demo-it-business.html'

    all_content = parse_docx(docx_file)

    # Debugging: Print a summary of the parsed content
    print("--- Parsed Content Summary ---")
    if not all_content:
        print("No content was parsed from the document.")
    else:
        for page, sections in all_content.items():
            print(f"- {page}: Found {len(sections)} sections.")
    print("----------------------------")

    homepage_content = all_content.get(homepage_file)
    if not homepage_content:
        print(f"Error: No content found for {homepage_file} in the document.")
        return

    # Find the hero section content by its title
    hero_section_text = None
    for title, text in homepage_content.items():
        if 'hero' in title.lower() or 'banner' in title.lower():
            hero_section_text = text
            break

    if not hero_section_text:
        print("Error: Could not find a section with 'Hero' or 'Banner' in the title for the homepage.")
        return

    update_homepage_hero(homepage_file, hero_section_text)

if __name__ == "__main__":
    main()