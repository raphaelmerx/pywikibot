# coding: utf-8
import csv
import re

import pywikibot
from pywikibot import pagegenerators


sr2010_ref = '<ref name="SR2010">[http://dne.mof.gov.tl/published/2010%20and%202011%20Publications/Pub%204%20Eng%20web/Publication%204%20ENGLISH%20Final_website.pdf Direcção Nacional de Estatística: Suco Report Volume 4 (englisch)] (PDF; 9,8 MB)</ref>'
sr2015_ref = '<ref name="SR2015">{{webarchive |url=https://web.archive.org/web/20161231161557/http://www.statistics.gov.tl/wp-content/uploads/2016/11/1_2015-V4-Households-Population-by-5-year-age-group.xls |date=2016-12-31 | title=Timor-Leste Population And Housing Census 2015}}</ref>'

population_re = re.compile(r'align="center" \|\d+ <small>\(2010\)</small><ref name="SR2010">')
paragraph_re = re.compile(r'Populasaun \d+ \(iha tinan 2010\)')
portuguese_title_re = re.compile(r'\(iha \[\[lia-portugés\]\]: \'\'([\w -\']+)\'\'\)')
portuguese_title_re_2 = re.compile(r'\(port. \'\'([\w -\']+)\'\'\)')

population_by_suco = {}
# build the dict suco_name -> population. Ignore duplicates
with open('suco_population/suco_population.csv') as f:
    reader = csv.reader(f)
    next(reader)
    duplicates = set()
    for line in reader:
        suco_name = line[2]
        if suco_name in duplicates:
            continue
        if suco_name in population_by_suco:
            duplicates.add(suco_name)
            population_by_suco.pop(suco_name)
            continue
        population_by_suco[suco_name] = line[3]


def get_population(page):
    suco_name = page.title()

    if suco_name in population_by_suco:
        return population_by_suco[suco_name]

    suco_name = get_portuguese_name(page.text)
    if suco_name is None:
        return None
    return population_by_suco.pop(suco_name, None)


def get_portuguese_name(text):
    match = portuguese_title_re.search(text)
    if match is None:
        match = portuguese_title_re_2.search(text)

    if match is not None:
        return match.groups()[0]
    return None


site = pywikibot.Site('tet', 'wikipedia')
sucos = pywikibot.Category(site, 'Kategoria:Suku Timór Lorosa\'e nian')
pages = list(sucos.articles())

# for page in [pywikibot.Page(site, 'Mauabu')]:
for page in pagegenerators.PreloadingGenerator(pages, 50):
    if 'SR2010' not in page.text:
        # already has updated information
        continue

    population = get_population(page)
    if population is None:
        print('WARNING: Could not find population for ', page.title())
        continue
    population = int(float(population))

    page.text = population_re.sub(
        r'align="center" |{} <small>(tinan 2015)</small><ref name="SR2010">'.format(population),
        page.text)
    page.text = paragraph_re.sub(
        r'Iha tinan 2015 total populasaun hamutuk {}'.format(population),
        page.text
    )

    page.text = page.text.replace(sr2010_ref, sr2015_ref)
    page.text = page.text.replace('SR2010', 'SR2015')

    page.save('Populasaun update ba sensus tinan 2015')
