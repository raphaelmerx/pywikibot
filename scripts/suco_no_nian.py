# coding: utf-8

import pywikibot
from pywikibot import pagegenerators

site = pywikibot.Site('tet', 'wikipedia')

sucos = pywikibot.Category(site,'Kategoria:Suku Timór Lorosa\'e nian')
pages = list(sucos.articles())

for page in pagegenerators.PreloadingGenerator(pages, 50):
    if 'suku ida iha [[Timór Lorosa\'e]] nian' in page.text:
        page.text = page.text.replace('suku ida iha [[Timór Lorosa\'e]] nian', 'suku ida iha [[Timór Lorosa\'e]]')
        page.save('Hadia Tetun: hasai "nian"')
