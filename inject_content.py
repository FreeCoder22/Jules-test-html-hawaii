import json
import os
from bs4 import BeautifulSoup, Doctype
import re

# --- HTML Component Templates ---

def create_hero_section(section_data):
    """Creates a hero banner section."""
    title = section_data.get('title', 'Welcome')
    content = section_data.get('content', '')
    content_lines = content.split('\n')
    subtitle = content_lines[0] if content_lines else ''

    buttons_text = re.findall(r'\[(.*?)\]', content)

    button_html = ''
    if len(buttons_text) > 0:
        button_html += f'<a href="#" class="btn btn-extra-large btn-switch-text btn-gradient-purple-pink btn-rounded me-10px ls-0px mt-15px"><span><span class="btn-double-text" data-text="{buttons_text[0]}">{buttons_text[0]}</span></span></a>'
    if len(buttons_text) > 1:
        button_html += f'<a href="#" class="btn btn-extra-large btn-switch-text btn-transparent-white-light btn-rounded border-1 ls-0px mt-15px"><span><span class="btn-double-text" data-text="{buttons_text[1]}">{buttons_text[1]}</span></span></a>'


    return f"""
    <section class="cover-background full-screen ipad-top-space-margin py-0 md-h-750px sm-h-650px" style="background-image:url('https://placehold.co/1920x1080');">
        <div class="opacity-very-light bg-black"></div>
        <div class="container h-100">
            <div class="row align-items-center h-100">
                <div class="col-xl-6 col-lg-8 col-md-10 position-relative z-index-1">
                    <span class="ps-25px pe-25px pt-5px pb-5px mb-25px text-uppercase text-white fs-12 ls-1px fw-600 border-radius-100px bg-gradient-dark-gray-transparent d-flex w-70 sm-w-100"><i class="bi bi-megaphone text-white icon-small me-10px"></i>{title}</span>
                    <h1 class="text-white fw-600 ls-minus-2px mb-25px">{subtitle}</h1>
                    {button_html}
                </div>
            </div>
        </div>
    </section>
    """

def create_about_section(section_data):
    """Creates a text-with-image about section."""
    title = section_data.get('title', '')
    content_lines = section_data.get('content', '').split('\n')
    heading = content_lines[0] if content_lines else ''
    paragraphs = '<br/>'.join(content_lines[1:]) if len(content_lines) > 1 else ''

    return f"""
    <section>
        <div class="container">
            <div class="row mb-10 align-items-center">
                <div class="col-lg-5 position-relative md-mb-20">
                    <div class="w-70 xs-w-80">
                        <img src="https://placehold.co/640x784" alt="" class="border-radius-8px w-100">
                    </div>
                    <div class="w-60 overflow-hidden position-absolute right-minus-15px xs-right-15px xs-w-60 bottom-minus-50px">
                        <img src="https://placehold.co/640x784" alt="" class="border-radius-8px w-100 box-shadow-quadruple-large" />
                    </div>
                </div>
                <div class="col-xl-5 col-lg-6 offset-lg-1">
                    <span class="ps-25px pe-25px mb-20px text-uppercase text-base-color fs-12 lh-40 fw-700 border-radius-100px bg-gradient-very-light-gray-transparent d-inline-flex">{title}</span>
                    <h3 class="text-dark-gray fs-40 fw-700 ls-minus-2px">{heading}</h3>
                    <p class="mb-40px sm-mb-25px">{paragraphs}</p>
                </div>
            </div>
        </div>
    </section>
    """

def create_services_section(section_data):
    """Creates a services section with cards."""
    title = section_data.get('title', '')
    content_lines = section_data.get('content', '').split('\n\n') # Split by double newline for each service

    cards_html = ''
    for service in content_lines:
        service_parts = service.split('\n')
        service_title = service_parts[0]
        service_desc = service_parts[1] if len(service_parts) > 1 else ''
        cards_html += f"""
        <div class="swiper-slide">
            <div class="services-box-style-03 last-paragraph-no-margin border-radius-6px overflow-hidden">
                <div class="position-relative">
                    <a href="#"><img src="https://placehold.co/600x440" alt=""></a>
                </div>
                <div class="bg-white">
                    <div class="ps-65px pe-65px pt-30px pb-30px text-center">
                        <a href="#" class="d-inline-block fs-18 fw-700 text-dark-gray mb-5px">{service_title}</a>
                        <p>{service_desc}</p>
                    </div>
                </div>
            </div>
        </div>
        """

    return f"""
    <section class="overflow-hidden bg-very-light-gray position-relative">
        <div class="container">
            <div class="row align-items-center mb-5 sm-mb-30px text-center text-lg-start">
                <div class="col-lg-8 md-mb-30px">
                    <h3 class="text-dark-gray fw-700 ls-minus-2px mb-0">{title}</h3>
                </div>
            </div>
            <div class="row align-items-center">
                <div class="col-12">
                    <div class="outside-box-right-20 sm-outside-box-right-0">
                        <div class="swiper magic-cursor slider-one-slide" data-slider-options='{{ "slidesPerView": 1, "spaceBetween": 30, "loop": true, "autoplay": {{ "delay": 4000, "disableOnInteraction": false }}, "keyboard": {{ "enabled": true, "onlyInViewport": true }}, "breakpoints": {{ "1200": {{ "slidesPerView": 4 }}, "992": {{ "slidesPerView": 3 }}, "768": {{ "slidesPerView": 2 }}, "320": {{ "slidesPerView": 1 }} }} }}'>
                            <div class="swiper-wrapper">
                                {cards_html}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """

def create_methodology_section(section_data):
    """Creates a methodology/process section."""
    title = section_data.get('title', '')
    content_lines = section_data.get('content', '').split('\n')
    heading = content_lines[0] if content_lines else ''

    steps_html = ''
    for i, step in enumerate(content_lines[1:]):
        steps_html += f"""
        <div class="col-12 process-step-style-05 position-relative hover-box">
            <div class="process-step-item d-flex">
                <div class="process-step-icon-wrap position-relative">
                    <div class="process-step-icon d-flex justify-content-center align-items-center mx-auto rounded-circle h-60px w-60px fs-14 bg-white position-relative box-shadow-bottom">
                        <span class="number position-relative z-index-1 text-dark-gray fw-600">0{i+1}</span>
                    </div>
                    <span class="progress-step-separator bg-dark-gray opacity-1"></span>
                </div>
                <div class="process-content ps-35px sm-ps-25px last-paragraph-no-margin mb-40px">
                    <span class="d-block fw-600 text-dark-gray fs-17 mb-5px">{step}</span>
                </div>
            </div>
        </div>
        """

    return f"""
    <section class="bg-very-light-gray">
        <div class="container">
            <div class="row align-items-center justify-content-center">
                <div class="col-xl-6 col-lg-8 text-center mb-4">
                     <h3 class="text-dark-gray fw-700 ls-minus-2px">{title}</h3>
                     <p>{heading}</p>
                </div>
            </div>
            <div class="row justify-content-center">
                 <div class="col-lg-8">
                    {steps_html}
                 </div>
            </div>
        </div>
    </section>
    """

def create_testimonial_section(section_data):
    """Creates a testimonial section."""
    title = section_data.get('title', '')
    content = section_data.get('content', '')

    return f"""
    <section>
        <div class="container">
             <div class="row justify-content-center mb-2">
                <div class="col-xxl-6 col-lg-8 col-md-9 text-center">
                    <h3 class="text-dark-gray fw-700 ls-minus-2px">{title}</h3>
                    <p>{content}</p>
                </div>
            </div>
        </div>
    </section>
    """

def create_contact_section(section_data):
    """Creates a call-to-action/contact section."""
    title = section_data.get('title', '')
    content_lines = section_data.get('content', '').split('\n')
    heading = content_lines[0] if content_lines else ''
    button_text = content_lines[1].strip('[]') if len(content_lines) > 1 else 'Contact Us'

    return f"""
    <section class="cover-background" style="background-image:url('https://placehold.co/1920x760');">
        <div class="opacity-extra-medium bg-dark-gray"></div>
        <div class="container">
            <div class="row align-items-center justify-content-center h-100">
                <div class="col-xl-8 col-lg-10 position-relative z-index-1 text-center">
                    <span class="ps-25px pe-25px pt-5px pb-5px mb-25px text-uppercase text-white fs-12 ls-1px fw-600 border-radius-100px bg-gradient-dark-gray-transparent d-inline-flex align-items-center text-start sm-lh-20">{title}</span>
                    <h2 class="text-white fw-600 ls-minus-2px mb-50px">{heading}</h2>
                    <a href="#" class="btn btn-extra-large btn-switch-text btn-gradient-purple-pink btn-rounded">
                        <span>
                            <span class="btn-double-text" data-text="{button_text}">{button_text}</span>
                        </span>
                    </a>
                </div>
            </div>
        </div>
    </section>
    """

def create_default_section(section_data):
    """Creates a default text section."""
    title = section_data.get('title', '')
    content = section_data.get('content', '').replace('\n', '<br/>')
    return f"""
    <section class="pt-5 pb-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-10 text-center">
                    <h4 class="text-dark-gray fw-600">{title}</h4>
                    <p>{content}</p>
                </div>
            </div>
        </div>
    </section>
    """

def create_page_title_section(section_data):
    """Creates a page title section for inner pages."""
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

def get_component_for_section(section_data, index, page_filename):
    """Selects a component based on section title, index, and page."""
    title = section_data['title'].lower()

    if index == 0:
        if page_filename == 'demo-it-business.html':
            return create_hero_section(section_data)
        else:
            return create_page_title_section(section_data)

    if 'propos' in title or 'promesse' in title or 'confiance' in title:
        return create_about_section(section_data)
    if 'expertises' in title or 'services' in title:
        return create_services_section(section_data)
    if 'méthodologie' in title or 'processus' in title:
        return create_methodology_section(section_data)
    if 'témoignages' in title:
        return create_testimonial_section(section_data)
    if 'contactez-nous' in title or 'parlons' in title or 'projet' in title:
        return create_contact_section(section_data)

    return create_default_section(section_data)

def main():
    # Load the parsed content
    with open('parsed_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Process each page
    for page_filename, sections in data.items():
        if not os.path.exists(page_filename):
            print(f"File not found: {page_filename}, skipping.")
            continue

        print(f"Processing {page_filename}...")

        # Read the original HTML template, handling BOM
        with open(page_filename, 'r', encoding='utf-8-sig') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find the main content area to replace - everything between header and footer
        header = soup.find('header')
        footer = soup.find('footer')

        if not header or not footer:
            print(f"Could not find header or footer in {page_filename}. Skipping content injection.")
            continue

        # Remove existing content between header and footer
        next_element = header.find_next_sibling()
        while next_element and next_element != footer:
            # Move to the next sibling before decomposing the current one
            next_sibling = next_element.find_next_sibling()
            next_element.decompose()
            next_element = next_sibling

        # Generate and add new sections
        new_content_soup = BeautifulSoup('<div></div>', 'html.parser')
        for i, section_data in enumerate(sections):
            component_html = get_component_for_section(section_data, i, page_filename)
            new_section = BeautifulSoup(component_html, 'html.parser')
            new_content_soup.div.append(new_section)

        # Insert new sections after the header
        # We need to extract the elements from the div, in reverse order to maintain correct order
        for element in reversed(list(new_content_soup.div.contents)):
            header.insert_after(element)

        # Save the modified HTML to a new file
        output_filename = page_filename
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Prettify the output for better readability
            html_content = soup.prettify()
            f.write(html_content)

        print(f"Successfully updated {output_filename}")


if __name__ == "__main__":
    main()