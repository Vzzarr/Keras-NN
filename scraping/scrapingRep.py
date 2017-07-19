import requests
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import codecs
import re

linksRss = [
    'http://www.repubblica.it/rss/politica/rss2.0.xml|politica',
    'http://www.repubblica.it/rss/esteri/rss2.0.xml|mondo',
    'http://www.repubblica.it/rss/economia/rss2.0.xml|economia',
    'http://www.repubblica.it/rss/sport/calcio/rss2.0.xml|sport',
    'http://www.repubblica.it/rss/sport/rss2.0.xml|sport',
    'http://www.repubblica.it/rss/sport/rugby/rss2.0.xml|sport',
    'http://www.repubblica.it/rss/sport/formulauno/rss2.0.xml|sport',
    'http://www.repubblica.it/rss/sport/motogp/rss2.0.xml|sport',
    'http://www.repubblica.it/rss/sport/ciclismo/rss2.0.xml|sport',
    'http://www.repubblica.it/rss/sport/basket/rss2.0.xml|sport',
    'http://www.repubblica.it/rss/spettacoli_e_cultura/rss2.0.xml|cultura',
    'http://www.repubblica.it/rss/speciali/arte/rss2.0.xml|cultura',
    'http://www.repubblica.it/rss/tecnologia/rss2.0.xml|scienza&tecnologia',
    'http://www.repubblica.it/rss/scienze/rss2.0.xml|scienza&tecnologia',
    'http://www.repubblica.it/rss/cronaca/rss2.0.xml|cronaca',
    'http://www.repubblica.it/rss/ambiente/rss2.0.xml|ambiente']

for link_category in linksRss:
    pageRss = requests.get(link_category.split("|")[0])
    category = link_category.split("|")[1]
    xmlfile = ET.fromstring(pageRss.content)

    count = 0

    for links in xmlfile.iter('link'):

        path = "/home/nicholas/Documenti/Keras-NN/mario/training/" + category
        if not os.path.exists(path):
            os.makedirs(path)
        if count > 1:
            name = re.sub(r'\/\?rss', "", links.text)
            name1 = re.sub("http(.*/)+", "", name)
            name2 = re.sub(r'[_-]+', "", name1)
            filePath = os.path.join(path, name2)

            if not os.path.isfile(filePath):
                page = requests.get(links.text)
                try:
                    text = BeautifulSoup(page.content, 'html.parser').find_all(class_="body-text")[0].find_all(
                        itemprop="articleBody")
                except IndexError:
                    pass
                try:
                    text = BeautifulSoup(page.content, 'html.parser').find_all(itemprop="description")
                except IndexError:
                    pass
                try:
                    text = BeautifulSoup(page.content, 'html.parser').find_all(class_="content")[0].find_all('p')
                except:
                    pass
                try:
                    text = BeautifulSoup(page.content, 'html.parser').find_all(class_="body-text")
                except:
                    pass

                if len(text) > 0:
                    testo = text[0]
                    [s.extract() for s in testo('script')]
                    [s.extract() for s in testo('style')]
                    [s.extract() for s in testo('footer')]
                    [s.extract() for s in testo('aside')]
                    [s.extract() for s in testo(class_="gs-share-count-text")]
                    [s.extract() for s in testo(class_="Tweet-body e-entry-content")]

                    textArticle = testo.get_text()
                    file = codecs.open(filePath, 'a', encoding='utf8')
                    file.write(textArticle)
                    file.close()
        count += 1
    print (category)