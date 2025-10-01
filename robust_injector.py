import os
from bs4 import BeautifulSoup, NavigableString

# =================================================================================================
# FINAL, ROBUST CONTENT INJECTION SCRIPT
# This script uses a structural, index-based approach to avoid brittle selectors.
# =================================================================================================

CONTENT_DATA = {
    'demo-it-business.html': {
        'hero': {
            'title': 'Votre avenir digital commence ici',
            'para': "Hawaii accompagne les PME dans la création d'applications métier intelligentes, évolutives et parfaitement intégrées à Microsoft Azure. De l'idée au déploiement, nous mettons l'innovation à votre portée.",
            'buttons': ['Découvrez nos expertises', 'Contactez-nous']
        },
        'about_promise': {
            'title': 'Un partenaire technologique fiable depuis 2010',
            'para': "Spécialistes du développement sur-mesure, de la migration vers Azure et de l'intégration de l'IA, nous vous aidons à tirer parti de la puissance du Cloud Microsoft avec sérénité.",
            'list_items': ['Expertise Azure reconnue (Partenaire Microsoft)', 'Orientation résultats', 'Accompagnement humain', 'Engagement Green IT']
        },
        'expertise': {
            'title': 'Nos Expertises',
            'slides': [
                {'title': 'Développement & Azure (HaaS)', 'desc': 'Applications métier sur-mesure, hébergées sur Azure en mode HaaS (Hawaii as a Service).'},
                {'title': 'Migration & Infrastructure Azure', 'desc': "• Migration 1 pour 1\n• Refonte PaaS\n• Création d'infrastructure Azure\n• FinOps"},
                {'title': 'IA & Innovation', 'desc': 'Intégrer l’intelligence artificielle pour automatiser et optimiser vos processus métier.'},
                {'title': 'Data & Power BI', 'desc': 'Visualisez, analysez et exploitez efficacement vos données métier grâce à Power BI.'},
                {'title': 'Cybersécurité', 'desc': 'Protégez efficacement votre entreprise grâce aux solutions de sécurité avancées de Microsoft.'},
                {'title': 'Power Platform', 'desc': 'Accélérez votre transformation digitale avec Microsoft Power Platform.'}
            ]
        },
        'methodology': {
            'title': 'Méthodologie éprouvée',
            'para': 'Une démarche claire, simple et efficace en 4 étapes :',
            'steps': ['Analyse métier', 'Conception UX/UI', 'Développement Agile', 'Déploiement & Run']
        },
        'case_studies': {
            'title': 'Réalisations clients',
            'para': 'Découvrez comment nous avons aidé des PME à transformer leur quotidien grâce à des applications métier modernes et puissantes sur Azure.'
        },
        'testimonials': {
            'title': 'Témoignages',
            'para': 'Ils nous font confiance : ce que disent nos clients de notre accompagnement.'
        },
        'final_cta': {
            'title': 'Contactez-nous',
            'para': 'Prêt à démarrer votre projet ou simplement curieux d’en savoir plus ?'
        }
    },
    'demo-it-business-about.html': {
        'title': {'main': 'Notre Promesse'},
        'intro': {
            'title': 'Pourquoi nous faire confiance ?',
            'para': 'Chez Hawaii, nous croyons que la technologie doit être un levier puissant au service de vos ambitions métier. Notre engagement est simple : vous permettre de bénéficier des meilleures technologies Microsoft Azure pour accélérer votre croissance et renforcer votre compétitivité.'
        },
        'commitments': {
            'title': 'Trois engagements clés',
            'items': [
                {'title': 'Expertise & maîtrise technologique', 'desc': "En tant que partenaire officiel de Microsoft depuis 2010, nous disposons d'une expertise certifiée et constamment actualisée..."},
                {'title': 'Innovation pragmatique', 'desc': "L'innovation doit servir un objectif précis : le vôtre. Nous intégrons des technologies avancées de manière pertinente..."},
                {'title': 'Proximité & accompagnement humain', 'desc': "Nous privilégions des relations solides, humaines et transparentes avec chacun de nos clients pour une tranquillité d'esprit totale."}
            ]
        },
        'green_it': {
            'title': 'Notre engagement Green IT',
            'para': 'Hawaii s’engage activement pour un numérique plus responsable et durable. Nous intégrons systématiquement une réflexion autour de l’impact environnemental dans nos choix techniques et nos architectures Cloud, afin de réduire l’empreinte écologique de vos infrastructures.'
        }
    }
}

# =================================================================================================
# HANDLER FUNCTIONS
# =================================================================================================

def handle_home_s0_hero(section, data):
    content = data['hero']
    title = section.select_one('h1'); para = section.select_one('p');
    btn1 = section.select_one('span[data-text="Explore crafto"]'); btn2 = section.select_one('span[data-text="Contact us"]')
    if title: title.string = content['title']
    if para: para.string = content['para']
    if btn1: btn1.string = content['buttons'][0]
    if btn2: btn2.string = content['buttons'][1]
    return True

def handle_home_s1_about(section, data):
    content = data['about_promise']
    title = section.select_one('h3'); para = section.select_one('p');
    progress_div = section.select_one('.progress-bar-style-02')
    if title: title.string = content['title']
    if para: para.string = content['para']
    if progress_div:
        new_ul = BeautifulSoup('<ul class="p-0 list-style-01 fs-16"></ul>', 'html.parser').ul
        for item_text in content['list_items']:
            li = BeautifulSoup(f'<li>{item_text}</li>', 'html.parser').li
            new_ul.append(li)
        progress_div.replace_with(new_ul)
    return True

def handle_home_s2_expertise(section, data):
    content = data['expertise']
    title = section.select_one('h3');
    if title: title.string = content['title']
    slides = section.select('.swiper-slide')
    for i, slide in enumerate(slides):
        if i >= len(content['slides']): slide.decompose(); continue
        slide_content = content['slides'][i]
        title_tag, p_tag = slide.select_one('a.fs-18'), slide.select_one('p')
        if title_tag: title_tag.string = slide_content['title']
        if p_tag:
            if '•' in slide_content['desc']:
                new_ul = BeautifulSoup('<ul class="p-0 list-style-01 fs-16 text-start"></ul>', 'html.parser').ul
                for item in slide_content['desc'].split('•'):
                    if item.strip(): new_ul.append(BeautifulSoup(f'<li>{item.strip()}</li>', 'html.parser').li)
                p_tag.replace_with(new_ul)
            else:
                p_tag.string = slide_content['desc']
    return True

def handle_home_s3_methodology(section, data):
    content = data['methodology']
    section.clear(); section['class'] = 'bg-dark-gray'
    html = f'<div class="container"><div class="row justify-content-center mb-4"><div class="col-lg-8 text-center"><h2 class="text-white">{content["title"]}</h2><p class="text-white opacity-6">{content["para"]}</p></div></div><div class="row row-cols-1 row-cols-lg-4 row-cols-md-2 justify-content-center">'
    for i, step in enumerate(content['steps']):
        html += f'<div class="col mt-4"><div class="feature-box p-4 bg-dark-slate-blue border-radius-6px"><h4 class="text-white">0{i+1}</h4><p class="text-white opacity-6">{step}</p></div></div>'
    html += '</div></div>'
    section.append(BeautifulSoup(html, 'html.parser'))
    return True

def handle_home_s5_case_studies(section, data):
    content = data['case_studies']
    title = section.select_one('h3')
    if title: title.string = content['title']
    new_p = BeautifulSoup(f'<p class="w-80 md-w-100 mt-20px">{content["para"]}</p>', 'html.parser').p
    title.find_parent('div').append(new_p)
    return True

def handle_home_s6_testimonials(section, data):
    content = data['testimonials']
    title = section.select_one('h3')
    if title: title.string = content['title']
    new_p = BeautifulSoup(f'<p class="fs-18 mt-20px">{content["para"]}</p>', 'html.parser').p
    title.find_parent('div').append(new_p)
    return True

def handle_home_s7_final_cta(section, data):
    content = data['final_cta']
    title = section.select_one('h1'); teaser = section.select_one('span.bg-gradient-dark-gray-transparent')
    if title: title.string = content['title']
    if teaser:
        icon_tag = teaser.find('i')
        teaser.string = content['para']
        if icon_tag: teaser.insert(0, icon_tag)
    return True

def handle_about_s0_title(section, data):
    content = data['title']
    title = section.select_one('h1')
    if title: title.string = content['main']
    return True

def handle_about_s1_intro_and_commitments(section, data):
    # Intro Part
    intro_content = data['intro']
    intro_title = section.find('h3', string=lambda t: 'Provide advanced business solutions' in t)
    if intro_title:
        intro_title.string = intro_content['title']
        wrapper = intro_title.find_parent().find('div', class_='mb-40px')
        if wrapper:
            wrapper.clear()
            wrapper.append(BeautifulSoup(f'<p>{intro_content["para"]}</p>', 'html.parser').p)

    # Commitments Part
    commit_content = data['commitments']
    commit_title = section.find('h3', string=lambda t: 'The creative process' in t)
    if commit_title:
        commit_title.string = commit_content['title']
        steps = section.select('.process-step-style-05 .process-step-item')
        for i, step in enumerate(steps):
            if i >= len(commit_content['items']): step.decompose(); continue
            item = commit_content['items'][i]
            s_title = step.select_one('.fs-17'); s_desc = step.select_one('p')
            if s_title: s_title.string = item['title']
            if s_desc: s_desc.string = item['desc']
    return True

def handle_about_s3_green_it(section, data):
    content = data['green_it']
    # This section originally contains counters, we replace it entirely.
    section.clear()
    section['class'] = 'pt-5 pb-5 bg-very-light-gray'
    html = f'<div class="container"><div class="row justify-content-center"><div class="col-lg-8 text-center"><h2 class="fw-700">{content["title"]}</h2><p class="fs-18">{content["para"]}</p></div></div></div>'
    section.append(BeautifulSoup(html, 'html.parser'))
    return True

# =================================================================================================
# MAIN PROCESSING LOGIC
# =================================================================================================

def process_html_file(page_name, page_content, handlers):
    soup = BeautifulSoup(page_content, 'html.parser')
    main_content = soup.find('body')
    if not main_content: return ""

    sections = main_content.find_all('section', recursive=False)
    print(f"  - Found {len(sections)} top-level sections in {page_name}")

    for i, section in enumerate(sections):
        handler = handlers.get(i)
        if handler:
            if handler(section, CONTENT_DATA[page_name]):
                 print(f"    - SUCCESS: Ran handler '{handler.__name__}' for section {i}.")
            else:
                 print(f"    - FAILURE: Handler '{handler.__name__}' failed for section {i}.")

    return str(soup.prettify())

def main():
    html_dir = '.'
    PAGE_HANDLERS = {
        'demo-it-business.html': {
            0: handle_home_s0_hero, 1: handle_home_s1_about, 2: handle_home_s2_expertise,
            3: handle_home_s3_methodology, 5: handle_home_s5_case_studies,
            6: handle_home_s6_testimonials, 7: handle_home_s7_final_cta,
        },
        'demo-it-business-about.html': {
            0: handle_about_s0_title, 1: handle_about_s1_intro_and_commitments,
            3: handle_about_s3_green_it,
        }
    }

    print("Starting robust, sequential injection process...")
    for page_name, handlers in PAGE_HANDLERS.items():
        page_path = os.path.join(html_dir, page_name)
        if not os.path.exists(page_path): continue
        print(f"\n--- Processing page: {page_name} ---")
        with open(page_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        modified_content = process_html_file(page_name, original_content, handlers)
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)
    print("\nInjection process complete.")

if __name__ == '__main__':
    main()