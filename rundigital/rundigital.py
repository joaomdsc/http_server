# rundigital.py - web scrapping

import json
from lxml import etree, html

#-------------------------------------------------------------------------------
# get_société
#-------------------------------------------------------------------------------

def get_société(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    root = html.fromstring(content)

    sociétés = []
    for div in root.findall('.//div[@class="row sp-item"]'):
        société = {}
        # Titre de la boîte
        société['nom'] = div.find('.//div/h3').text

        # CA, Effectif, ...
        for p in div.findall('.//div/div[@class="row"]/p'):
            b = p.find('.//b')
            key = b.text
            if key.endswith(': '):
                key = key[:-2]
            key = key.strip()
            val = b.tail.strip() if b.tail else ""
            société[key] = val

        société['sections'] = []

        # Votre Entreprise
        x = div.find('.//div/div[@class="row"]/div/h5')
        p = x.getparent()
        
        # Il y a plusieurs "titres" en h5, chacun suivi de plusieurs
        # questions. Il y a parfois plusieurs réponses pour une questions, il
        # faut lire les fils de p dans l'ordre

        section = {}
        questions = {}
        for k in p:
            if k.tag == 'h5' and k.attrib['class'] == 'text-title color-event':
                if len(questions) > 0:
                    # Finish off previous question
                    questions['réponse'] = '\n'.join(rep)
                    section['questions'].append(questions)
                    questions = {}
                if len(section) > 0:
                    # Finish off previous section
                    société['sections'].append(section)
                subtitle = k.find('.//strong').text
                section = {
                    'section': subtitle,
                    'questions': [],
                } 

            if k.tag == 'h5' and k.attrib['class'] == 'text-question':
                if len(questions) > 0:
                    # Finish off previous question
                    questions['réponse'] = '\n'.join(rep)
                    section['questions'].append(questions)
                questions = {
                    'question': k.find('.//strong').text,
                }
                rep = []
                
            if k.tag == 'p' and k.attrib['class'] == 'text-memo':
                rep.append(k.text.strip())

        # Don't forget last section
        if len(questions) > 0:
            # Finish off previous question
            questions['réponse'] = '\n'.join(rep)
            section['questions'].append(questions)
        # Finish off previous section
        société['sections'].append(section)
                
        sociétés.append(société)

    return sociétés 

#-------------------------------------------------------------------------------
# dump_text
#-------------------------------------------------------------------------------

def dump_text(sociétés):
    s =''
    for société in sociétés:
        s += société['nom'] + '\n'

        # CA, Effectif, ...
        for k, v in société.items():
            if k not in ['nom', 'sections']:
                s += f'  {k}: {v}\n'

        # Sections
        for sect in société['sections']:
            s += sect['section'] + '\n'
            for q in sect['questions']:
                s += f'  {q["question"]}\n'
                s += f'  {q["réponse"]}\n'
            s += '\n'

    s += '\n'
    return s

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------

sociétés = []
for i in range(5):
    fp = rf'C:\a\rundigital\Speed Meetings - page{i+1}.html'
    sociétés.extend(get_société(fp))

filename = 'rundigital.json'
print(f'Writing {filename}')
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(sociétés, f, indent=4, ensure_ascii=False)

filename = 'rundigital.txt'
print(f'Writing {filename}')
with open(filename, 'w', encoding='utf-8') as f:
    f.write(dump_text(sociétés))
