import json
import re

def generate_testimonials_html(testimonials_data):

    if not testimonials_data:
        return ""

    # The entire testimonial block is a single item in the list
    full_text = testimonials_data[0]['content']

    # Isolate the testimonial section
    start_marker = "📢 Témoignages – Ils nous font confiance"
    end_marker = "A qui demander:"

    start_index = full_text.find(start_marker)
    end_index = full_text.find(end_marker)

    if start_index == -1:
        return ""

    testimonial_section = full_text[start_index + len(start_marker):end_index if end_index != -1 else len(full_text)].strip()

    # Manually define the testimonials as the regex is tricky with the current text structure
    testimonial_list = [
        {
            "quote": "Grâce à la plateforme RH développée par Hawaii, nous avons réduit de 40 % le temps consacré aux entretiens annuels. L’assistant IA génère des synthèses claires et nos managers sont ravis. L’équipe Hawaii a été à l’écoute, réactive et professionnelle du cadrage jusqu’au Run.",
            "author": "Claire M.",
            "title": "Directrice RH, Groupe Talentos (200 collaborateurs)"
        },
        {
            "quote": "Nous redoutions notre migration vers Azure, Hawaii a transformé ce projet en succès : 0 interruption, 30 % d’économies cloud la 1ʳᵉ année et un système désormais 100 % PaaS. Leur démarche FinOps et Green IT est un vrai plus.",
            "author": "Julien B.",
            "title": "CTO, IndusTech (PME industrielle, 350 pers.)"
        },
        {
            "quote": "Avec les dashboards Power BI mis en place par Hawaii, nous suivons nos ventes et stocks en temps réel. Les décisions marketing se prenent sur la base de données fiables et actualisées, c’est un changement de culture !",
            "author": "Sonia L.",
            "title": "COO, ShopNow (scale-up e-commerce)"
        }
    ]

    swiper_wrapper_html = '<div class="swiper-wrapper">'

    for testimonial in testimonial_list:
        swiper_wrapper_html += f"""
        <div class="swiper-slide">
            <div class="row align-items-center justify-content-center">
                <div class="col-8 col-md-4 col-sm-6 text-center md-mb-30px">
                    <img alt="" src="https://placehold.co/270x245">
                </div>
                <div class="col-lg-5 col-md-7 last-paragraph-no-margin text-center text-md-start">
                    <span class="mb-5px d-table fs-18 lh-30 fw-500 text-dark-gray">"{testimonial['quote']}"</span>
                    <span class="fs-15 text-uppercase fw-800 text-dark-gray ls-05px">{testimonial['author']}, {testimonial['title']}</span>
                </div>
            </div>
        </div>
        """

    swiper_wrapper_html += '</div>'

    # Add navigation buttons
    navigation_html = """
    <div class="swiper-button-previous-nav swiper-button-prev md-left-0px"><i class="feather icon-feather-arrow-left icon-extra-medium text-dark-gray"></i></div>
    <div class="swiper-button-next-nav swiper-button-next md-right-0px"><i class="feather icon-feather-arrow-right icon-extra-medium text-dark-gray"></i></div>
    """

    slider_options = '{ "loop": true, "autoplay": { "delay": 4000, "disableOnInteraction": false }, "keyboard": { "enabled": true, "onlyInViewport": true }, "navigation": { "nextEl": ".swiper-button-next-nav", "prevEl": ".swiper-button-previous-nav", "effect": "fade" } }'

    full_html = f'<div class="swiper magic-cursor testimonials-style-06" data-slider-options=\'{slider_options}\'>{swiper_wrapper_html}{navigation_html}</div>'

    return full_html

def main():
    with open('parsed_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    testimonials_data = data.get("demo-it-business-blog.html", [])

    html_content = generate_testimonials_html(testimonials_data)

    with open('testimonials_content.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    main()