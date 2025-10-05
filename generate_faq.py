import json

def main():
    with open('parsed_content.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    faq_content_raw = data.get("demo-it-business-blog.html", [])

    if not faq_content_raw:
        print("No FAQ content found in JSON.")
        return

    full_faq_text = faq_content_raw[0]['content']

    faq_list = []

    questions = [
        "Qu’est-ce que le modèle HaaS ?",
        "Quelle différence entre les formules Basic et Premium ?",
        "Est-ce que la consommation Azure est incluse dans le prix ?",
        "Quels délais pour un projet type ?",
        "Qui possède le code source ?",
        "Comment gérez-vous la sécurité ?",
        "Et si notre trafic explose ?",
        "Avez-vous une démarche FinOps / Green IT ?",
        "Pouvez-vous intégrer des outils non-Microsoft ?",
        "Comment se passe le support au quotidien ?",
        "Proposez-vous des formations ?",
        "Quelle est votre zone d’intervention ?",
        "Comment démarrer ?"
    ]

    content = full_faq_text

    for i, q in enumerate(questions):
        start = content.find(q)
        if start == -1:
            continue

        end = -1
        if i + 1 < len(questions):
            end = content.find(questions[i+1])

        if end != -1:
            answer = content[start + len(q):end].strip()
        else:
            real_end = content.find('Résultats obtenus chez nos clients')
            if real_end != -1:
                 answer = content[start + len(q):real_end].strip()
            else:
                 answer = content[start + len(q):].strip()

        answer_lines = answer.split('\n')
        cleaned_answer = ""
        for line in answer_lines:
            line = line.strip()
            if not line:
                continue
            cleaned_answer += f"<p>{line.replace('•', '').strip()}</p>"

        faq_list.append({"title": q, "content": cleaned_answer})

    final_html = ""
    for i, item in enumerate(faq_list):
        active_class = " active-accordion" if i == 0 else ""
        show_class = " show" if i == 0 else ""
        aria_expanded = "true" if i == 0 else "false"
        icon = "icon-feather-minus" if i == 0 else "icon-feather-plus"

        final_html += f'''
        <div class="accordion-item{active_class}">
            <div class="accordion-header border-bottom border-color-transparent-dark-very-light">
                <a href="#" data-bs-toggle="collapse" data-bs-target="#accordion-style-02-faq-{i+1}" aria-expanded="{aria_expanded}" data-bs-parent="#accordion-faq">
                    <div class="accordion-title mb-0 position-relative text-dark-gray pe-30px">
                        <i class="feather {icon} fs-20"></i><span class="fs-17 fw-500">{item['title']}</span>
                    </div>
                </a>
            </div>
            <div id="accordion-style-02-faq-{i+1}" class="accordion-collapse collapse{show_class}" data-bs-parent="#accordion-faq">
                <div class="accordion-body last-paragraph-no-margin border-bottom border-color-transparent-dark-very-light">
                    {item['content']}
                </div>
            </div>
        </div>
        '''

    with open('faq_content.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    main()