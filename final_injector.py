import os
import re
from bs4 import BeautifulSoup

# =================================================================================================
# CUSTOM HANDLER FUNCTIONS
# Each function is responsible for modifying a complete semantic section of a page.
# =================================================================================================

def handle_home_hero(soup, rule):
    section = soup.select_one("section.cover-background")
    if not section: return False

    title = section.select_one('h1')
    para = section.select_one('p.opacity-6')
    btn1 = section.select_one('span[data-text="Explore crafto"]')
    btn2 = section.select_one('span[data-text="Contact us"]')

    if title: title.string = "Votre avenir digital commence ici"
    if para: para.string = "Hawaii accompagne les PME dans la création d'applications métier intelligentes, évolutives et parfaitement intégrées à Microsoft Azure. De l'idée au déploiement, nous mettons l'innovation à votre portée."
    if btn1: btn1.string = "Découvrez nos expertises"
    if btn2: btn2.string = "Contactez-nous"

    return all([title, para, btn1, btn2])

def handle_home_about_promise(soup, rule):
    section = soup.find(lambda tag: tag.name == 'h3' and 'Powerful agency for corporate business' in tag.get_text())
    if not section: return False
    parent_col = section.find_parent(class_=re.compile(r'col-'))
    if not parent_col: return False

    title = parent_col.select_one('h3')
    para = parent_col.select_one('p')
    progress_div = parent_col.select_one('.progress-bar-style-02')

    if title: title.string = "Un partenaire technologique fiable depuis 2010"
    if para: para.string = "Spécialistes du développement sur-mesure, de la migration vers Azure et de l'intégration de l'IA, nous vous aidons à tirer parti de la puissance du Cloud Microsoft avec sérénité."
    if progress_div:
        list_items = [
            'Expertise Azure reconnue (Partenaire Microsoft)',
            'Orientation résultats : nous livrons des solutions fonctionnelles et à forte valeur métier',
            'Accompagnement humain : proximité, réactivité et pédagogie',
            'Engagement Green IT : nous veillons à réduire l’impact environnemental de votre infrastructure IT'
        ]
        new_ul = soup.new_tag('ul', attrs={'class': 'p-0 list-style-01 fs-16'})
        for item_text in list_items:
            li = soup.new_tag('li'); li.string = item_text; new_ul.append(li)
        progress_div.replace_with(new_ul)

    return all([title, para, progress_div])

def handle_home_expertise(soup, rule):
    section = soup.find(lambda tag: tag.name == 'h3' and 'Understanding the business services' in tag.get_text())
    if not section: return False
    section.string = 'Nos Expertises'
    parent_section = section.find_parent('section')
    if not parent_section: return False

    slides = parent_section.select('.swiper-slide')
    titles = ["Développement & Azure (HaaS)", "Migration & Infrastructure Azure", "IA & Innovation", "Data & Power BI", "Cybersécurité", "Power Platform"]
    descs = [
        "Applications métier sur-mesure, hébergées sur Azure en mode HaaS (Hawaii as a Service).",
        "• Migration 1 pour 1\n• Refonte PaaS\n• Création d'infrastructure Azure\n• FinOps",
        "Intégrer l’intelligence artificielle pour automatiser et optimiser vos processus métier.",
        "Visualisez, analysez et exploitez efficacement vos données métier grâce à Power BI.",
        "Protégez efficacement votre entreprise grâce aux solutions de sécurité avancées de Microsoft.",
        "Accélérez votre transformation digitale avec Microsoft Power Platform."
    ]

    for i, slide in enumerate(slides):
        if i >= len(titles): slide.decompose(); continue
        title_tag, p_tag = slide.select_one('a.fs-18'), slide.select_one('p')
        if title_tag: title_tag.string = titles[i]
        if p_tag:
            desc = descs[i]
            if '•' in desc:
                new_ul = soup.new_tag('ul', attrs={'class': 'p-0 list-style-01 fs-16 text-start'})
                for item in desc.split('•'):
                    if item.strip():
                        li = soup.new_tag('li'); li.string = item.strip(); new_ul.append(li)
                p_tag.replace_with(new_ul)
            else:
                p_tag.string = desc
    return True

def handle_home_methodology(soup, rule):
    section_tag = soup.find(lambda tag: tag.name == 'h3' and 'Serving our clients' in tag.get_text())
    if not section_tag: return False
    section = section_tag.find_parent('section')
    if not section: return False
    section.clear()
    section['class'] = 'bg-dark-gray'
    html = """<div class="container"><div class="row justify-content-center mb-4"><div class="col-lg-8 text-center"><h2 class="text-white">Méthodologie éprouvée</h2><p class="text-white opacity-6">Une démarche claire, simple et efficace en 4 étapes :</p></div></div><div class="row row-cols-1 row-cols-lg-4 row-cols-md-2 justify-content-center"><div class="col mt-4"><div class="feature-box p-4 bg-dark-slate-blue border-radius-6px"><h4 class="text-white">01</h4><p class="text-white opacity-6">Analyse métier</p></div></div><div class="col mt-4"><div class="feature-box p-4 bg-dark-slate-blue border-radius-6px"><h4 class="text-white">02</h4><p class="text-white opacity-6">Conception UX/UI</p></div></div><div class="col mt-4"><div class="feature-box p-4 bg-dark-slate-blue border-radius-6px"><h4 class="text-white">03</h4><p class="text-white opacity-6">Développement Agile</p></div></div><div class="col mt-4"><div class="feature-box p-4 bg-dark-slate-blue border-radius-6px"><h4 class="text-white">04</h4><p class="text-white opacity-6">Déploiement & Run</p></div></div></div></div>"""
    section.append(BeautifulSoup(html, 'html.parser'))
    return True

def handle_home_case_studies(soup, rule):
    section = soup.find(lambda tag: tag.name == 'h3' and 'Recent case studies' in tag.get_text())
    if not section: return False
    section.string = 'Réalisations clients'
    new_p = soup.new_tag('p', attrs={'class': 'w-80 md-w-100 mt-20px'})
    new_p.string = 'Découvrez comment nous avons aidé des PME à transformer leur quotidien grâce à des applications métier modernes et puissantes sur Azure.'
    section.insert_after(new_p)
    return True

def handle_home_testimonials(soup, rule):
    section = soup.find(lambda tag: tag.name == 'h3' and 'Trusted by the world' in tag.get_text())
    if not section: return False
    section.string = 'Témoignages'
    parent_div = section.find_parent('div')
    if not parent_div: return False
    new_p = soup.new_tag('p', attrs={'class': 'fs-18 mt-20px'})
    new_p.string = 'Ils nous font confiance : ce que disent nos clients de notre accompagnement.'
    parent_div.append(new_p)
    return True

def handle_home_final_cta(soup, rule):
    section = soup.find(lambda tag: tag.name == 'h1' and 'We make the creative solutions' in tag.get_text())
    if not section: return False
    section.string = 'Contactez-nous'
    teaser_span = section.find_previous_sibling('span')
    if teaser_span:
        icon_tag = teaser_span.find('i')
        teaser_span.string = 'Prêt à démarrer votre projet ou simplement curieux d’en savoir plus ?'
        if icon_tag: teaser_span.insert(0, icon_tag)
    return True

def handle_about_title(soup, rule):
    title = soup.find(lambda tag: tag.name == 'h1' and 'About crafto' in tag.get_text())
    if title: title.string = 'Notre Promesse'
    return True

def handle_about_intro(soup, rule):
    section = soup.find(lambda tag: tag.name == 'h3' and 'Provide advanced business solutions' in tag.get_text())
    if not section: return False
    section.string = 'Pourquoi nous faire confiance ?'
    wrapper = soup.find('div', class_='mb-40px')
    if wrapper:
        new_p = soup.new_tag('p'); new_p.string = 'Chez Hawaii, nous croyons que la technologie doit être un levier puissant au service de vos ambitions métier. Notre engagement est simple : vous permettre de bénéficier des meilleures technologies Microsoft Azure pour accélérer votre croissance et renforcer votre compétitivité.'
        wrapper.replace_with(new_p)
    return True

def handle_about_commitments(soup, rule):
    section = soup.find(lambda tag: tag.name == 'h3' and 'The creative process behind our projects' in tag.get_text())
    if not section: return False
    section.string = 'Trois engagements clés'
    steps = soup.select('.process-step-style-05 .process-step-item')
    titles = ["Expertise & maîtrise technologique", "Innovation pragmatique", "Proximité & accompagnement humain"]
    descs = [
        "En tant que partenaire officiel de Microsoft depuis 2010, nous disposons d'une expertise certifiée et constamment actualisée...",
        "L'innovation doit servir un objectif précis : le vôtre. Nous intégrons des technologies avancées de manière pertinente...",
        "Nous privilégions des relations solides, humaines et transparentes avec chacun de nos clients pour une tranquillité d'esprit totale."
    ]
    for i, step in enumerate(steps):
        if i >= len(titles): step.decompose(); continue
        title_tag, desc_tag = step.select_one('.fs-17'), step.select_one('p')
        if title_tag: title_tag.string = titles[i]
        if desc_tag: desc_tag.string = descs[i]
    return True

def handle_about_green_it(soup, rule):
    section = soup.find('div', class_='counter-style-04')
    if not section: return False
    parent_section = section.find_parent('section')
    if not parent_section: return False
    parent_section.clear()
    parent_section['class'] = 'pt-5 pb-5'
    html = """<div class="container"><div class="row justify-content-center"><div class="col-lg-8 text-center"><h2 class="fw-700">Notre engagement Green IT</h2><p class="fs-18">Hawaii s’engage activement pour un numérique plus responsable et durable. Nous intégrons systématiquement une réflexion autour de l’impact environnemental dans nos choix techniques et nos architectures Cloud, afin de réduire l’empreinte écologique de vos infrastructures.</p></div></div></div>"""
    parent_section.append(BeautifulSoup(html, 'html.parser'))
    return True

REPLACEMENT_RULES = [
    {'page': 'demo-it-business.html', 'handler': handle_home_hero},
    {'page': 'demo-it-business.html', 'handler': handle_home_about_promise},
    {'page': 'demo-it-business.html', 'handler': handle_home_expertise},
    {'page': 'demo-it-business.html', 'handler': handle_home_methodology},
    {'page': 'demo-it-business.html', 'handler': handle_home_case_studies},
    {'page': 'demo-it-business.html', 'handler': handle_home_testimonials},
    {'page': 'demo-it-business.html', 'handler': handle_home_final_cta},
    {'page': 'demo-it-business-about.html', 'handler': handle_about_title},
    {'page': 'demo-it-business-about.html', 'handler': handle_about_intro},
    {'page': 'demo-it-business-about.html', 'handler': handle_about_commitments},
    {'page': 'demo-it-business-about.html', 'handler': handle_about_green_it},
]

def apply_replacements(rules, html_dir):
    pages_to_process = sorted(list(set(rule['page'] for rule in rules)))
    for page_name in pages_to_process:
        page_path = os.path.join(html_dir, page_name)
        if not os.path.exists(page_path): continue
        print(f"\n--- Processing page: {page_name} ---")
        with open(page_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        page_rules = [r for r in rules if r['page'] == page_name]
        for rule in page_rules:
            if rule['handler'](soup, rule):
                print(f"  - SUCCESS: Ran handler '{rule['handler'].__name__}'")
            else:
                print(f"  - FAILURE: Handler '{rule['handler'].__name__}' failed to find its target.")
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))

def main():
    html_dir = '.'
    print("Starting final injection process...")
    for page in {rule['page'] for rule in REPLACEMENT_RULES}:
        os.system(f'git restore {os.path.join(html_dir, page)}')
        print(f"Restored {page} to original state.")
    apply_replacements(REPLACEMENT_RULES, html_dir)
    print("\nInjection process complete.")

if __name__ == '__main__':
    main()