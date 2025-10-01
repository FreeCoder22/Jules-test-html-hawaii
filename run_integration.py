import os
import re
from bs4 import BeautifulSoup

# =================================================================================================
# FINAL, ROBUST, AND UNIFIED CONTENT INTEGRATION SCRIPT
# =================================================================================================

# 1. Hardcoded Content
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
            'list_items': ['Expertise Azure reconnue (Partenaire Microsoft)', 'Orientation résultats : nous livrons des solutions fonctionnelles et à forte valeur métier', 'Accompagnement humain : proximité, réactivité et pédagogie', 'Engagement Green IT : nous veillons à réduire l’impact environnemental de votre infrastructure IT']
        },
        'expertise': {
            'title': 'Nos Expertises',
            'slides': [
                {'title': 'Développement & Azure (HaaS)', 'desc': 'Applications métier sur-mesure, hébergées sur Azure en mode HaaS (Hawaii as a Service).'},
                {'title': 'Migration & Infrastructure Azure', 'desc': "• Migration 1 pour 1 : Transférez facilement vos infrastructures actuelles vers Azure.\n• Refonte PaaS : Profitez pleinement des avantages du Cloud Azure.\n• Création d'infrastructure Azure : Conception et déploiement d'infrastructures cloud robustes.\n• FinOps : Optimisation proactive et continue de vos coûts cloud."},
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
        'page_title': 'Notre Promesse',
        'intro': {
            'title': 'Pourquoi nous faire confiance ?',
            'para': 'Chez Hawaii, nous croyons que la technologie doit être un levier puissant au service de vos ambitions métier. Notre engagement est simple : vous permettre de bénéficier des meilleures technologies Microsoft Azure pour accélérer votre croissance et renforcer votre compétitivité.'
        },
        'commitments': {
            'title': 'Trois engagements clés',
            'items': [
                {'title': 'Expertise & maîtrise technologique', 'desc': "En tant que partenaire officiel de Microsoft depuis 2010, nous disposons d'une expertise certifiée et constamment actualisée."},
                {'title': 'Innovation pragmatique', 'desc': "L'innovation doit servir un objectif précis : le vôtre. Nous intégrons des technologies avancées de manière pertinente."},
                {'title': 'Proximité & accompagnement humain', 'desc': "Nous privilégions des relations solides, humaines et transparentes avec chacun de nos clients."}
            ]
        },
        'green_it': {
            'title': 'Notre engagement Green IT',
            'para': 'Hawaii s’engage activement pour un numérique plus responsable et durable. Nous intégrons systématiquement une réflexion autour de l’impact environnemental dans nos choix techniques et nos architectures Cloud, afin de réduire l’empreinte écologique de vos infrastructures.'
        }
    }
}

def process_home_page(soup, data):
    # Hero Section
    section = soup.select_one('section.cover-background')
    if section:
        content = data['hero']
        h1 = section.select_one('h1'); p = section.select_one('p.opacity-6')
        btn1 = section.select_one('span[data-text="Explore crafto"]'); btn2 = section.select_one('span[data-text="Contact us"]')
        if h1: h1.string = content['title']
        if p: p.string = content['para']
        if btn1: btn1.string = content['buttons'][0]
        if btn2: btn2.string = content['buttons'][1]
        section['data-injected'] = 'true'

    # About Promise Section
    span_anchor = soup.find('span', string=lambda t: t and 'Creative approach' in t)
    if span_anchor:
        section = span_anchor.find_parent('section')
        if section:
            content = data['about_promise']
            h3 = section.select_one('h3'); p = section.select_one('p')
            if h3: h3.string = content['title']
            if p: p.string = content['para']
            progress_div = section.select_one('.progress-bar-style-02')
            if progress_div:
                ul = soup.new_tag('ul', **{'class': 'p-0 list-style-01 fs-16'})
                for item in content['list_items']:
                    li = soup.new_tag('li'); li.string = item; ul.append(li)
                progress_div.replace_with(ul)
            section['data-injected'] = 'true'

    # Expertise
    h3 = soup.find('h3', string=lambda t: t and 'Understanding the business services' in t)
    if h3:
        section = h3.find_parent('section')
        if section:
            content = data['expertise']
            h3.string = content['title']
            slides = section.find_all('div', class_='swiper-slide')
            for i, slide in enumerate(slides):
                if i < len(content['slides']):
                    slide_data = content['slides'][i]; title_tag, p_tag = slide.find('a', class_='fs-18'), slide.find('p')
                    if title_tag: title_tag.string = slide_data['title']
                    if p_tag:
                        if '•' in slide_data['desc']:
                            ul = soup.new_tag('ul', **{'class': 'p-0 list-style-01 fs-16 text-start'})
                            for item in slide_data['desc'].split('•'):
                                if item.strip(): ul.append(soup.new_tag('li', string=item.strip()))
                            p_tag.replace_with(ul)
                        else: p_tag.string = slide_data['desc']
                else: slide.decompose()
            section['data-injected'] = 'true'

    # Methodology
    h3 = soup.find('h3', string=lambda t: t and 'Serving our clients' in t)
    if h3:
        section = h3.find_parent('section')
        if section:
            content = data['methodology']
            section.clear(); section['class'] = 'bg-dark-gray py-5'
            html = f'<div class="container"><div class="row justify-content-center mb-4"><div class="col-lg-8 text-center"><h2 class="text-white">{content["title"]}</h2><p class="text-white opacity-6">{content["para"]}</p></div></div><div class="row row-cols-1 row-cols-lg-4 row-cols-md-2 justify-content-center">'
            for i, step in enumerate(content['steps']):
                html += f'<div class="col mt-4"><div class="feature-box p-4 bg-dark-slate-blue border-radius-6px"><h4 class="text-white">0{i+1}</h4><p class="text-white opacity-6">{step}</p></div></div>'
            section.append(BeautifulSoup(html + '</div></div>', 'html.parser'))
            section['data-injected'] = 'true'

    # Case Studies
    h3_case = soup.find(lambda tag: tag.name == 'h3' and 'Recent case studies' in tag.get_text(strip=True))
    if h3_case:
        section = h3_case.find_parent('section')
        if section:
            content = data['case_studies']
            h3_case.string = content['title']
            p = soup.new_tag('p', **{'class': 'w-80 md-w-100 mt-20px'}); p.string = content['para']
            h3_case.find_parent('div').append(p)
            section['data-injected'] = 'true'
            # Also remove the filter navigation
            filter_nav = section.select_one('.portfolio-filter')
            if filter_nav: filter_nav.decompose()
            # And the portfolio grid itself
            portfolio_grid = section.select_one('.portfolio-wrapper')
            if portfolio_grid: portfolio_grid.decompose()

    # Testimonials
    h3_test = soup.find(lambda tag: tag.name == 'h3' and 'Trusted by the world' in tag.get_text(strip=True))
    if h3_test:
        section = h3_test.find_parent('section')
        if section:
            content = data['testimonials']
            h3_test.string = content['title']
            p = soup.new_tag('p', **{'class': 'fs-18 mt-20px'}); p.string = content['para']
            h3_test.find_parent('div').append(p)
            # Remove the old testimonials slider and partner logos below it
            slider = section.select_one('.testimonials-style-06')
            if slider: slider.decompose()
            logos = section.select_one('.row-cols-md-3.justify-content-center')
            if logos: logos.decompose()
            section['data-injected'] = 'true'

    # Final CTA
    h1 = soup.find('h1', string=lambda t: t and 'We make the creative solutions' in t)
    if h1:
        section = h1.find_parent('section')
        if section:
            content = data['final_cta']
            h1.string = content['title']
            teaser = h1.find_previous_sibling('span')
            if teaser:
                icon = teaser.find('i')
                teaser.string = content['para'];
                if icon: teaser.insert(0, icon)
            # Decompose the button
            button = section.find('a', class_='btn')
            if button: button.decompose()
            section['data-injected'] = 'true'

def process_about_page(soup, data):
    # Page Title
    h1 = soup.find('h1', string=lambda t: t and 'About crafto' in t)
    if h1:
        section = h1.find_parent('section')
        if section:
            h1.string = data['page_title']
            section['data-injected'] = 'true'

    # Intro
    span_anchor = soup.find('span', string=lambda t: t and 'Creative approach' in t)
    if span_anchor:
        section = span_anchor.find_parent('section')
        if section:
            content = data['intro']
            h3 = section.select_one('h3');
            if h3: h3.string = content['title']
            wrapper = section.select_one('div.mb-40px')
            if wrapper:
                wrapper.clear(); wrapper.append(soup.new_tag('p', string=content['para']))
            # Remove buttons
            for btn in section.select('a.btn'): btn.decompose()
            section['data-injected'] = 'true'

    # Commitments
    h3_commit = soup.find('h3', string=lambda t: t and 'The creative process' in t)
    if h3_commit:
        section = h3_commit.find_parent('section')
        if section:
            content = data['commitments']
            h3_commit.string = content['title']
            steps = section.select('.process-step-style-05')
            for i, step in enumerate(steps):
                if i < len(content['items']):
                    item = content['items'][i]
                    title, desc = step.select_one('.fs-17'), step.select_one('p')
                    if title: title.string = item['title']
                    if desc: desc.string = item['desc']
                else: step.decompose()
            section['data-injected'] = 'true'

    # Green IT
    counter_div = soup.find('div', class_='counter-style-04')
    if counter_div:
        section = counter_div.find_parent('section')
        if section:
            section.clear(); section['class'] = 'py-5'
            html = f'<div class="container"><div class="row justify-content-center"><div class="col-lg-8 text-center"><h2 class="fw-700">{data["green_it"]["title"]}</h2><p class="fs-18">{data["green_it"]["para"]}</p></div></div></div>'
            section.append(BeautifulSoup(html, 'html.parser'))
            section['data-injected'] = 'true'

# 3. Cleanup Logic
def cleanup_page(soup):
    for section in soup.body.find_all('section', recursive=False):
        if not section.has_attr('data-injected'):
            section.decompose()

# 4. Main Execution
def main():
    PAGE_HANDLERS = {
        'demo-it-business.html': process_home_page,
        'demo-it-business-about.html': process_about_page,
    }
    print("Starting unified content integration process...")
    for page_name in PAGE_HANDLERS.keys():
        os.system(f'git restore {page_name}')

    for page_name, handler in PAGE_HANDLERS.items():
        page_path = os.path.join('.', page_name)
        if not os.path.exists(page_path): continue
        print(f"\n--- Processing: {page_name} ---")
        with open(page_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        handler(soup, CONTENT_DATA[page_name])
        print(f"  - Content injection complete.")

        cleanup_page(soup)
        print(f"  - Cleanup complete.")

        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print(f"  - Saved modified file.")
    print("\n\nIntegration process complete.")

if __name__ == '__main__':
    main()