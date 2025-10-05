import json
import os
from bs4 import BeautifulSoup
import re

# --- Component Templates ---

def create_hero_section(section_data):
    title = section_data.get('title', 'Welcome')
    content = section_data.get('content', '')
    content_lines = content.split('\n')
    subtitle = content_lines[0] if content_lines else ''
    buttons_text = re.findall(r'\[(.*?)\]', content)

    button_html = ''
    if buttons_text:
        button_html += f'<a href="#" class="btn btn-extra-large btn-switch-text btn-gradient-purple-pink btn-rounded me-10px ls-0px mt-15px"><span><span class="btn-double-text" data-text="{buttons_text[0]}">{buttons_text[0]}</span></span></a>'
    if len(buttons_text) > 1:
        button_html += f'<a href="#" class="btn btn-extra-large btn-switch-text btn-transparent-white-light btn-rounded border-1 ls-0px mt-15px"><span><span class="btn-double-text" data-text="{buttons_text[1]}">{buttons_text[1]}</span></span></a>'

    return f"""
    <section class="cover-background full-screen ipad-top-space-margin py-0" style="background-image:url('https://placehold.co/1920x1080');">
        <div class="opacity-very-light bg-black"></div>
        <div class="container h-100">
            <div class="row align-items-center h-100">
                <div class="col-xl-7 col-lg-8 col-md-10 position-relative z-index-1">
                    <span class="ps-25px pe-25px pt-5px pb-5px mb-25px text-uppercase text-white fs-12 ls-1px fw-600 border-radius-100px bg-gradient-dark-gray-transparent d-inline-flex align-items-center"><i class="bi bi-megaphone text-white icon-small me-10px"></i>{title}</span>
                    <h1 class="text-white fw-600 ls-minus-2px mb-25px">{subtitle}</h1>
                    <p class="w-85 sm-w-95 text-white opacity-7 fs-18">{"<br/>".join(content_lines[1:-1] if buttons_text else content_lines[1:])}</p>
                    {button_html}
                </div>
            </div>
        </div>
    </section>
    """

def create_page_title_section(section_data):
    title = section_data.get('title', 'Page Title')
    content_lines = section_data.get('content', '').split('\n')
    subtitle = content_lines[0] if content_lines else ''

    return f"""
    <section class="pt-0 cover-background ipad-top-space-margin sm-pb-0" style="background-image:url('https://placehold.co/1920x530');">
        <div class="container">
            <div class="row align-items-center justify-content-center h-500px sm-h-300px">
                <div class="col-12 col-xl-8 col-lg-10 position-relative text-center page-title-extra-large d-flex flex-wrap flex-column align-items-center justify-content-center">
                    <span class="ps-25px pe-25px pt-5px pb-5px mb-15px text-uppercase text-dark-gray fs-12 ls-1px fw-600 border-radius-100px bg-white d-inline-block">{title}</span>
                    <h1 class="mb-20px text-dark-gray fw-700 ls-minus-1px">{subtitle}</h1>
                </div>
            </div>
        </div>
    </section>
    """

def create_about_section_with_image(section_data):
    title = section_data.get('title', '')
    content_lines = section_data.get('content', '').split('\n')
    heading = content_lines[0]
    paragraphs = "<br/>".join(content_lines[1:])

    return f"""
    <section>
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 md-mb-50px">
                    <img src="https://placehold.co/800x866" alt="" class="border-radius-8px">
                </div>
                <div class="col-xl-5 offset-xl-1 col-lg-6">
                    <h3 class="text-dark-gray fw-700 ls-minus-1px">{heading}</h3>
                    <p>{paragraphs}</p>
                </div>
            </div>
        </div>
    </section>
    """

def create_icon_features_section(section_data):
    title = section_data.get('title', '')
    content_lines = section_data.get('content', '').split('\n')

    feature_html = ""
    icons = ["line-icon-Medal-2", "line-icon-Knight", "line-icon-Gear", "line-icon-Management"]
    for i, line in enumerate(content_lines):
        if not line.strip(): continue
        icon = icons[i % len(icons)]
        feature_html += f"""
        <div class="col">
            <div class="p-10 lg-p-8 text-center border-color-extra-medium-gray bg-white text-center last-paragraph-no-margin">
                <i class="{icon} icon-extra-large text-base-color mb-15px d-block"></i>
                <span class="fs-14 fw-700 text-dark-gray text-uppercase lh-20 d-inline-block">{line}</span>
            </div>
        </div>
        """

    return f"""
    <section class="position-relative pt-3 sm-pt-50px">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8 text-center mb-4">
                    <h3 class="text-dark-gray fw-700 ls-minus-2px">{title}</h3>
                </div>
            </div>
            <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 justify-content-center">
                {feature_html}
            </div>
        </div>
    </section>
    """

def create_faq_section(section_data):
    title = section_data.get('title', 'FAQ')
    faq_items = re.split(r'\n\n', section_data.get('content', ''))

    accordion_html = ""
    for i, item in enumerate(faq_items):
        parts = item.split('\n')
        question = parts[0]
        answer = " ".join(parts[1:])
        accordion_html += f"""
        <div class="accordion-item">
            <h2 class="accordion-header" id="heading-{i}">
                <button class="accordion-button {'collapsed' if i > 0 else ''}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-{i}" aria-expanded="{'true' if i == 0 else 'false'}">
                    {question}
                </button>
            </h2>
            <div id="collapse-{i}" class="accordion-collapse collapse {'show' if i == 0 else ''}" data-bs-parent="#accordion-style-01">
                <div class="accordion-body">
                    <p>{answer}</p>
                </div>
            </div>
        </div>
        """

    return f"""
    <section>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8 text-center mb-4">
                     <h3 class="text-dark-gray fw-700 ls-minus-2px">{title}</h3>
                </div>
            </div>
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="accordion accordion-style-01" id="accordion-style-01">
                        {accordion_html}
                    </div>
                </div>
            </div>
        </div>
    </section>
    """

def create_testimonial_slider(section_data):
    title = section_data.get('title', '')
    content_lines = re.split(r'\n\n', section_data.get('content', ''))

    slides_html = ""
    for item in content_lines:
        parts = item.split('\n')
        if len(parts) < 2: continue
        quote = parts[0]
        author = parts[1]
        slides_html += f"""
        <div class="swiper-slide">
            <div class="row align-items-center justify-content-center">
                <div class="col-8 col-md-4 col-sm-6 text-center md-mb-30px">
                    <img alt="" src="https://placehold.co/270x245">
                </div>
                <div class="col-lg-5 col-md-7 last-paragraph-no-margin text-center text-md-start">
                    <span class="mb-5px d-table fs-18 lh-30 fw-500 text-dark-gray">{quote}</span>
                    <span class="fs-15 text-uppercase fw-800 text-dark-gray ls-05px">{author}</span>
                </div>
            </div>
        </div>
        """

    return f"""
    <section>
        <div class="container">
             <div class="row justify-content-center mb-2">
                <div class="col-xxl-6 col-lg-8 col-md-9 text-center">
                    <h3 class="text-dark-gray fw-700 ls-minus-2px">{title}</h3>
                </div>
            </div>
            <div class="row justify-content-center align-items-center">
                <div class="col-xl-10 position-relative">
                    <div class="swiper magic-cursor testimonials-style-06" data-slider-options='{{ "loop": true, "autoplay": {{ "delay": 4000, "disableOnInteraction": false }} }}'>
                        <div class="swiper-wrapper">
                            {slides_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """

def create_default_section(section_data):
    title = section_data.get('title', '')
    content = section_data.get('content', '').replace('\n', '<br/>')
    return f"""
    <section class="pt-5 pb-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-10">
                    <h4 class="text-dark-gray fw-600">{title}</h4>
                    <p>{content}</p>
                </div>
            </div>
        </div>
    </section>
    """

def get_component_for_section(section_data, index, page_filename):
    title = section_data['title'].lower()

    if index == 0:
        return create_page_title_section(section_data) if page_filename != 'demo-it-business.html' else create_hero_section(section_data)

    if 'faq' in title:
        return create_faq_section(section_data)
    if 'témoignages' in title:
        return create_testimonial_slider(section_data)
    if 'engagements' in title or 'pourquoi' in title or 'signifie' in title or 'services inclus' in title:
        return create_icon_features_section(section_data)
    if 'propos' in title or 'promesse' in title or 'confiance' in title or 'transition' in title:
        return create_about_section_with_image(section_data)
    if 'expertises' in title or 'services' in title:
        return create_icon_features_section(section_data)
    if 'contactez-nous' in title or 'parlons' in title or 'projet' in title:
        return create_page_title_section(section_data)

    return create_default_section(section_data)

def main():
    with open('parsed_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for page_filename, sections in data.items():
        if not sections:
            print(f"No sections found for {page_filename}, skipping.")
            continue

        if not os.path.exists(page_filename):
            print(f"File not found: {page_filename}, skipping.")
            continue

        print(f"Processing {page_filename}...")

        with open(page_filename, 'r', encoding='utf-8-sig') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Identify the main content area to replace.
        # This is more robust than just looking for <section> tags.
        main_content_area = soup.find('header').find_next_sibling()

        if not main_content_area:
             print(f"Could not find a main content area in {page_filename}")
             continue

        # Clear existing content more carefully
        while main_content_area and main_content_area.name != 'footer':
            next_sibling = main_content_area.find_next_sibling()
            main_content_area.decompose()
            main_content_area = next_sibling

        header = soup.find('header')
        new_content_soup = BeautifulSoup('<div></div>', 'html.parser')
        for i, section_data in enumerate(sections):
            component_html = get_component_for_section(section_data, i, page_filename)
            new_section = BeautifulSoup(component_html, 'html.parser')
            new_content_soup.div.append(new_section)

        for element in reversed(list(new_content_soup.div.contents)):
            header.insert_after(element)

        with open(page_filename, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

        print(f"Successfully updated {page_filename}")

if __name__ == "__main__":
    main()