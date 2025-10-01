import os
import re
from bs4 import BeautifulSoup
from docx import Document

# --- REGEX DEFINITIONS (GLOBAL) ---
target_page_regex = re.compile(r'^PAGE(?: CIBLE)?:.*?\s*([\w-]+\.html)', re.IGNORECASE)
semantic_section_regex = re.compile(r'^SECTION(?: SÉMANTIQUE)?:(.*?)(?:\(|$)', re.IGNORECASE)
# A more robust marker regex to handle 'KEYWORD (type):' and 'KEYWORD:'
marker_regex = re.compile(r'^(.*?)(?:\s+\(([\w_]+)\))?:\s*(.*)')
bullet_point_regex = re.compile(r'^\s*[•-]\s*(.*)')
ordered_list_regex = re.compile(r'^\s*\d+\.\s*(.*)')
end_marker_regex = re.compile(r'--- FIN (?:EXPERTISE|ENGAGEMENT|BÉNÉFICE) ---', re.IGNORECASE)

def extract_content_from_docx(docx_path):
    document = Document(docx_path)
    pages_data = {}

    pending_section = None
    current_block_type = None
    accumulated_content = []

    def clean_and_store_content(content_str):
        content_str = re.sub(r'\[(.*?)\]', r'\1', content_str).strip()
        content_str = re.sub(r'\|\s*\[Rôle de l\'URL.*$', '', content_str).strip()
        return content_str

    def flush_block():
        nonlocal pending_section, current_block_type, accumulated_content
        if pending_section and current_block_type and accumulated_content:
            full_text = '\n'.join(accumulated_content).strip()
            cleaned_text = end_marker_regex.sub('', full_text).strip()

            if not cleaned_text:
                accumulated_content = []; current_block_type = None; return

            if 'list' in current_block_type:
                items = [m.group(1).strip() for line in cleaned_text.split('\n') if (m := bullet_point_regex.match(line) or ordered_list_regex.match(line))]
                pending_section['content'][current_block_type] = items
            elif 'buttons' in current_block_type or 'butons' in current_block_type:
                pending_section['content'][current_block_type] = [clean_and_store_content(btn) for btn in cleaned_text.split('|')]
            else:
                final_content = clean_and_store_content(cleaned_text)
                if current_block_type in pending_section['content']:
                    if not isinstance(pending_section['content'][current_block_type], list):
                        pending_section['content'][current_block_type] = [pending_section['content'][current_block_type]]
                    pending_section['content'][current_block_type].append(final_content)
                else:
                    pending_section['content'][current_block_type] = final_content

        accumulated_content = []
        current_block_type = None

    for para in document.paragraphs:
        text = para.text.strip()

        target_match = target_page_regex.search(text)
        if target_match:
            flush_block()
            page_name = target_match.group(1).strip()
            if page_name not in pages_data:
                pages_data[page_name] = []
            if pending_section:
                if pending_section.get('content'):
                    pages_data[page_name].append(pending_section)
                pending_section = None
            continue

        section_match = semantic_section_regex.search(text)
        if section_match:
            flush_block()
            if pending_section and pending_section.get('content'):
                 print(f"Warning: Discarding section '{pending_section.get('section_name')}' without a target page.")
            section_name = section_match.group(1).strip()
            pending_section = {'section_name': section_name, 'content': {}}
            continue

        if not text:
            flush_block()
            continue

        if not pending_section:
            continue

        marker_match = marker_regex.match(text)
        if marker_match:
            flush_block()
            keyword = marker_match.group(1).strip()
            semantic_type = marker_match.group(2)
            content_on_same_line = marker_match.group(3).strip()

            current_block_type = semantic_type.strip() if semantic_type else keyword.lower().replace(' ', '_')

            if content_on_same_line:
                accumulated_content.append(content_on_same_line)
        elif current_block_type:
            accumulated_content.append(text)

    flush_block()
    return pages_data

def handle_about_promise(soup, content):
    """Injects content for the 'À propos – Notre promesse' section."""
    print("  -> Running handler for 'À propos – Notre promesse'")
    # Use a lambda for a more robust search that ignores whitespace issues
    about_span = soup.find(lambda tag: tag.name == 'span' and 'Creative approach' in tag.get_text(strip=True))
    if not about_span:
        print("  - Warning: Could not find the 'Creative approach' span.")
        return
    about_section = about_span.find_parent(class_=re.compile(r'col-'))
    if not about_section:
        print("  - Warning: Could not find parent column for about section.")
        return

    if content.get('h2_title'):
        title_tag = about_section.select_one('h3')
        if title_tag:
            title_tag.string = content['h2_title']
            print(f"    - Updated about title to: \"{content['h2_title'][:30]}...\"")
    if content.get('description_body'):
        p_tag = about_section.select_one('p')
        if p_tag:
            p_tag.string = content['description_body']
            print("    - Updated about paragraph.")
    if content.get('bullet_points_list'):
        progress_div = about_section.select_one('.progress-bar-style-02')
        if progress_div:
            new_ul = soup.new_tag('ul', attrs={'class': 'p-0 list-style-01 fs-16'})
            for item in content['bullet_points_list']:
                li = soup.new_tag('li')
                li.string = item
                new_ul.append(li)
            progress_div.replace_with(new_ul)
            print("    - Replaced progress bars with a list.")

def handle_expertise_section(soup, content):
    """Injects content into the 'Nos Expertises' section (the services slider)."""
    print("  -> Running handler for 'Nos Expertises'")
    section_title = soup.find('h3', string=re.compile(r'business services|Nos Expertises', re.IGNORECASE))
    if not section_title:
        print("  - Warning: Could not find the services section title.")
        return
    services_section = section_title.find_parent('section')
    if not services_section:
        print("  - Warning: Could not find parent <section> for services.")
        return

    if content.get('h2_title'):
        section_title.string = content['h2_title']
        print(f"    - Updated section title to: \"{content['h2_title']}\"")

    slides = services_section.select('.swiper-slide')
    titles = content.get('item_title', [])
    descriptions = content.get('item_description', [])

    for i, slide in enumerate(slides):
        if i >= len(titles): break
        title_tag = slide.select_one('a.fs-18')
        p_tag = slide.select_one('p')

        if title_tag and i < len(titles):
            title_tag.string = titles[i]
            print(f"    - Updated slide {i+1} title to: \"{titles[i]}\"")
        if p_tag and i < len(descriptions):
            desc = descriptions[i]
            if '•' in desc:
                new_ul = soup.new_tag('ul', **{'class': 'p-0 list-style-01 fs-16 text-start'})
                list_items = [li.strip() for li in desc.split('\n') if li.strip()]
                for item_text in list_items:
                    clean_item_text = bullet_point_regex.sub(r'\1', item_text).strip()
                    if clean_item_text:
                        li = soup.new_tag('li')
                        li.string = clean_item_text
                        new_ul.append(li)
                p_tag.replace_with(new_ul)
                print(f"    - Replaced slide {i+1} description with a list.")
            else:
                p_tag.string = desc
                print(f"    - Updated slide {i+1} description.")

def handle_case_studies(soup, content):
    """Injects content into the 'Recent case studies' section."""
    print("  -> Running handler for 'Réalisations clients'")
    section_title = soup.find('h3', string=re.compile(r'Recent case studies', re.IGNORECASE))
    if not section_title:
        print("  - Warning: Could not find the case studies section title.")
        return

    if content.get('h2_title'):
        section_title.string = content['h2_title']
        print(f"    - Updated case studies title to: \"{content['h2_title']}\"")

    if content.get('description_teaser'):
        # The teaser paragraph doesn't exist in the template, so create and insert it.
        new_p = soup.new_tag('p', **{'class': 'w-80 md-w-100 mt-20px'}) # Add classes for styling
        new_p.string = content['description_teaser']
        section_title.insert_after(new_p)
        print("    - Inserted new teaser paragraph for case studies.")

def handle_methodology(soup, content):
    """Replaces the 'industries' section with the methodology content."""
    print("  -> Running handler for 'Méthodologie Éprouvée'")
    section_title = soup.find('h3', string=re.compile(r'Serving our clients', re.IGNORECASE))
    if not section_title:
        print("  - Warning: Could not find the 'industries' section title.")
        return

    methodology_section = section_title.find_parent('section')
    if not methodology_section:
        print("  - Warning: Could not find the parent section for 'industries'.")
        return

    # Clear the old content (title and grid)
    methodology_section.clear()

    # Rebuild the section with new content
    container = soup.new_tag('div', **{'class': 'container'})
    methodology_section.append(container)

    title_div = soup.new_tag('div', **{'class': 'row justify-content-center mb-4'})
    title_col = soup.new_tag('div', **{'class': 'col-lg-8 text-center'})

    new_title = soup.new_tag('h2', **{'class': 'text-white'})
    new_title.string = content.get('h2_title', 'Méthodologie éprouvée')
    title_col.append(new_title)

    if content.get('description_body'):
        new_p = soup.new_tag('p', **{'class': 'text-white opacity-6'})
        new_p.string = content['description_body']
        title_col.append(new_p)

    title_div.append(title_col)
    container.append(title_div)

    if content.get('ordered_steps_list'):
        list_row = soup.new_tag('div', **{'class': 'row row-cols-1 row-cols-lg-4 row-cols-md-2 justify-content-center'})
        for i, item in enumerate(content['ordered_steps_list']):
            col = soup.new_tag('div', **{'class': 'col mt-4'})
            step_div = soup.new_tag('div', **{'class': 'feature-box p-4 bg-dark-slate-blue border-radius-6px'})
            step_div.append(soup.new_tag('h4', string=f"0{i+1}", **{'class':'text-white'}))
            step_div.append(soup.new_tag('p', string=item, **{'class':'text-white opacity-6'}))
            col.append(step_div)
            list_row.append(col)
        container.append(list_row)
    print("    - Replaced 'industries' section with methodology steps.")

def handle_testimonials(soup, content):
    """Updates the testimonials section title and adds a teaser."""
    print("  -> Running handler for 'Témoignages'")
    section_title = soup.find('h3', string=re.compile(r'Trusted by the world', re.IGNORECASE))
    if not section_title:
        print("  - Warning: Could not find the testimonials section title.")
        return

    if content.get('h2_title'):
        section_title.string = content['h2_title']
        print(f"    - Updated testimonials title to: \"{content['h2_title']}\"")

    if content.get('description_teaser'):
        new_p = soup.new_tag('p', **{'class': 'fs-18 mt-20px'})
        new_p.string = content['description_teaser']
        section_title.find_parent('div').append(new_p)
        print("    - Inserted new teaser paragraph for testimonials.")

def handle_contact_cta(soup, content):
    """Updates the final call-to-action section."""
    print("  -> Running handler for 'Contactez-nous'")
    section_title = soup.find('h1', string=re.compile(r'We make the creative solutions', re.IGNORECASE))
    if not section_title:
        print("  - Warning: Could not find the final CTA section title.")
        return

    if content.get('h2_title'):
        section_title.string = content['h2_title']
        print(f"    - Updated final CTA title to: \"{content['h2_title']}\"")

    if content.get('description_teaser'):
        # The teaser is in a span with a specific structure
        teaser_span = section_title.find_previous_sibling('span')
        if teaser_span:
            # Preserve the icon if it exists
            icon_tag = teaser_span.find('i')
            teaser_span.string = content['description_teaser']
            if icon_tag:
                teaser_span.insert(0, icon_tag)
            print("    - Updated final CTA teaser text.")

def handle_about_intro(soup, content):
    """Injects content into the about page introduction section."""
    print("  -> Running handler for 'Notre Promesse - Introduction'")
    section_title = soup.find('h3', string=re.compile(r'Provide advanced business solutions', re.IGNORECASE))
    if not section_title:
        print("  - Warning: Could not find the 'advanced business solutions' section title.")
        return

    if content.get('h2_title'):
        section_title.string = content['h2_title']
        print(f"    - Updated intro title to: \"{content['h2_title']}\"")

    if content.get('description_body'):
        # The parent column contains the feature boxes we need to replace
        parent_col = section_title.find_parent(class_=re.compile(r'col-'))
        if parent_col:
            feature_box_wrapper = parent_col.find('div', class_='mb-40px')
            if feature_box_wrapper:
                new_p = soup.new_tag('p')
                new_p.string = content['description_body']
                feature_box_wrapper.replace_with(new_p)
                print("    - Replaced feature boxes with introduction paragraph.")

def handle_commitments(soup, content):
    """Injects content into the 'Trois engagements clés' section."""
    print("  -> Running handler for 'Trois engagements clés'")
    section_title = soup.find('h3', string=re.compile(r'The creative process behind our projects', re.IGNORECASE))
    if not section_title:
        print("  - Warning: Could not find the 'creative process' section title.")
        return

    if content.get('h2_title'):
        section_title.string = content['h2_title']
        print(f"    - Updated commitments section title to: \"{content['h2_title']}\"")

    steps = soup.select('.process-step-style-05 .process-step-item')
    titles = content.get('item_title', [])
    descriptions = content.get('item_description', [])

    for i, step in enumerate(steps):
        if i >= len(titles): break

        title_tag = step.select_one('.fs-17')
        desc_tag = step.select_one('p')

        if title_tag and i < len(titles):
            title_tag.string = titles[i]
            print(f"    - Updated commitment {i+1} title.")

        if desc_tag and i < len(descriptions):
            desc_tag.string = descriptions[i]
            print(f"    - Updated commitment {i+1} description.")

def handle_green_it(soup, content):
    """Replaces the 'counters' section with the Green IT content."""
    print("  -> Running handler for 'Notre engagement Green IT'")
    counter_section = soup.find('div', class_='counter-style-04')
    if not counter_section:
        print("  - Warning: Could not find the 'counters' section.")
        return

    section_to_replace = counter_section.find_parent('section')
    if not section_to_replace:
        print("  - Warning: Could not find parent section for counters.")
        return

    # Create a new, simpler section
    new_section = soup.new_tag('section', **{'class': 'pt-5 pb-5'})
    container = soup.new_tag('div', **{'class': 'container'})
    row = soup.new_tag('div', **{'class': 'row justify-content-center'})
    col = soup.new_tag('div', **{'class': 'col-lg-8 text-center'})

    if content.get('h2_title'):
        title_tag = soup.new_tag('h2', **{'class': 'fw-700'})
        title_tag.string = content['h2_title']
        col.append(title_tag)

    if content.get('description_body'):
        p_tag = soup.new_tag('p', **{'class': 'fs-18'})
        p_tag.string = content['description_body']
        col.append(p_tag)

    row.append(col)
    container.append(row)
    new_section.append(container)

    section_to_replace.replace_with(new_section)
    print("    - Replaced counters section with Green IT content.")

HANDLER_DISPATCH = {
    'À propos – Notre promesse': handle_about_promise,
    'Nos Expertises': handle_expertise_section,
    'Réalisations clients': handle_case_studies,
    'Méthodologie Éprouvée': handle_methodology,
    'Témoignages': handle_testimonials,
    'Contactez-nous': handle_contact_cta,
    # Handlers for about page
    'Notre Promesse - Introduction': handle_about_intro,
    'Trois engagements clés': handle_commitments,
    'Notre engagement Green IT': handle_green_it,
}

def inject_content(pages_data, html_dir):
    for page_name, sections in pages_data.items():
        file_path = os.path.join(html_dir, page_name)
        if not os.path.exists(file_path):
            print(f"Warning: Target file '{file_path}' not found.")
            continue

        print(f"\n--- Processing HTML file: {page_name} ---")
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        for section in sections:
            section_name = section.get('section_name')
            if section_name in HANDLER_DISPATCH:
                handler = HANDLER_DISPATCH[section_name]
                handler(soup, section['content'])
            else:
                print(f"  - No handler for section: '{section_name}'. Skipping.")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print(f"--- Finished processing {page_name} ---")

def main():
    docx_path = 'Contenus site Hawaii.docx'
    html_dir = '.'
    print(f"Starting content integration from '{docx_path}'...")
    structured_data = extract_content_from_docx(docx_path)
    if not structured_data:
        print("No structured data could be extracted.")
        return
    inject_content(structured_data, html_dir)
    print("\nContent integration process complete.")

if __name__ == '__main__':
    main()