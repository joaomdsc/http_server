# rundigital_societe.py - web scrapping

import os
import json
import urllib.request
from lxml import etree, html

#-------------------------------------------------------------------------------
# get_société
#-------------------------------------------------------------------------------

def get_société(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    root = html.fromstring(content)

    # Le root ici est directement la société (une société par fichier)
    société = {}
    # Titre de la boîte
    société['nom'] = root.find('.//div[@class="pmo-stat"]/h2').text

    # Logo
    x = root.find('.//div[@class="p-relative"]/a/img')
    logo_url = x.attrib['src']
    société['logo'] = logo_url

    # # Download the logo image to a local file
    # dirpath = r'C:\a\rundigital\logos'
    # suffix = logo_url.rsplit('.', maxsplit=1)[1]
    # with urllib.request.urlopen(logo_url) as f:
    #     data = f.read()
    # filepath = os.path.join(dirpath, f'{société["nom"]}.{suffix}')
    # print(f'Writing file "{filepath}"')
    # with open(filepath, 'wb') as f:
    #     f.write(data)

    # Adresse
    x = root.find('.//div[@class="pmo-block pmo-contact  "]/ul/li/address')
    # FIXME ici il faut tout le texte sous tous les sous-éléments
    société['adresse'] = x.text.strip()
    
    # Téléphones
    tels = []
    for x in root.findall('.//div[@class="pmo-block pmo-contact  "]/ul/li/i[@class="zmdi zmdi-phone"]'):
        tels.append(x.tail.strip())
    société['tels'] = tels

    # # Adresse web
    # x = root.find('.//div[@class="pmo-block pmo-contact  "]/ul/li/i[@class="zmdi zmdi-globe"]')
    # # FIXME je veux le frère <a> du noeud <i>
    # x = x.getparent()
    # société['url'] = x.text.strip()

    # FIXME Les contacts (nom, fonction, etc) sont en texte non structuré sous
    # l'élément div[@class="pmbb-view"], à côté du pmo-contact
    
    # Panels
    panels = []
    for x in root.findall('.//div[@class="panel-group"]/div[@class="panel panel-collapse"]'):
        param = x.find('.//div/h4/a').text.strip()
        value = x.find('.//div/div/p').text.strip()
        panels.append((param, value))
    société['panels'] = panels

    return société

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
for i in range(40):
    fp = rf'C:\a\rundigital\catalogue\contact{i}.html'
    sociétés.append(get_société(fp))

filename = 'rundigital_societe.json'
print(f'Writing {filename}')
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(sociétés, f, indent=4, ensure_ascii=False)
