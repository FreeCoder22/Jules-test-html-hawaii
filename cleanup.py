import os
from bs4 import BeautifulSoup

def cleanup_page(page_path):
    """Reads an HTML file, removes specified demo sections, and saves it."""
    if not os.path.exists(page_path):
        print(f"  - File not found: {page_path}")
        return

    print(f"--- Cleaning up {page_path} ---")
    with open(page_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    selectors_to_remove = []
    if 'demo-it-business.html' in page_path:
        selectors_to_remove = [
            '.row.row-cols-1.row-cols-lg-3.row-cols-md-2.justify-content-center.mb-7', # Top 3 feature boxes
            '.clients-style-06', # Client logo scroller
            'section.p-0.bg-midnight-blue', # "Save your precious time" section
            '.portfolio-wrapper' # The grid of portfolio items
        ]
    elif 'demo-it-business-about.html' in page_path:
        selectors_to_remove = [
            '.d-flex.flex-column.box-shadow-quadruple-large', # The 4-box grid with icons
            'section.bg-very-light-gray', # The section containing the image scroller and counters
            '.clients-style-06', # The final client logo scroller
        ]

    for selector in selectors_to_remove:
        elements = soup.select(selector)
        for element in elements:
            # We find the parent <section> or <div class="row"> to remove the whole block
            parent_to_remove = element.find_parent('section') or element.find_parent(class_='row')
            if parent_to_remove:
                parent_to_remove.decompose()
                print(f"  - Removed element (or its parent section/row) matching: {selector}")
            else:
                element.decompose()
                print(f"  - Removed element matching: {selector}")


    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

def main():
    print("Starting cleanup of unused demo sections...")
    cleanup_page('demo-it-business.html')
    cleanup_page('demo-it-business-about.html')
    print("\nCleanup complete.")

if __name__ == '__main__':
    main()