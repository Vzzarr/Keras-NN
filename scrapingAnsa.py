import requests
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import codecs
import re

linksRssAnsa = [
    'http://www.ansa.it/sito/notizie/politica/politica_rss.xml|politica',
    'http://www.ansa.it/sito/notizie/mondo/mondo_rss.xml|mondo',
    'http://www.ansa.it/sito/notizie/economia/economia_rss.xml|economia',
    'http://www.ansa.it/sito/notizie/sport/calcio/calcio_rss.xml|sport',
    'http://www.ansa.it/sito/notizie/sport/sport_rss.xml|sport',
    'http://www.ansa.it/sito/notizie/cultura/cinema/cinema_rss.xml|cultura',
    'http://www.ansa.it/sito/notizie/cultura/cultura_rss.xml|cultura',
    'http://www.ansa.it/sito/notizie/tecnologia/tecnologia_rss.xml|scienza&tecnologia',
    'http://www.ansa.it/sito/notizie/cronaca/cronaca_rss.xml|cronaca', ]


def scrapeAnsa() :
    for link_category in linksRssAnsa:
        pageRss = requests.get(link_category.split("|")[0])
        category = link_category.split("|")[1]
        xmlfile = ET.fromstring(pageRss.content)

        #numberLinks = 0

        #for links in xmlfile.iter('link'):
        #    numberLinks += 1
        #trainigPercent = (numberLinks * 80) / 100
        #testPercent = numberLinks - trainigPercent

        count = 0

        #print (numberLinks)
        #print (trainigPercent)

        for links in xmlfile.iter('link'):

            #if count < trainigPercent:
            #    path = "/home/nicholas/Documenti/Keras-NN/ansa/training/" + category
            #    if not os.path.exists(path):
            #        os.makedirs(path)
            #else:
            path = "/home/nicholas/Documenti/Keras-NN/mario/test/" + category
            if not os.path.exists(path):
                os.makedirs(path)

            if count > 0:
                page = requests.get(links.text)
                text = BeautifulSoup(page.content, 'html.parser').find_all(class_="news-txt")[0].find_all('p')
                name1 = re.sub("http(.*/)+", "", links.text)
                # textArticle = ''
                name2 = re.sub(r'[^\w]+', "", name1)
                if len(text) > 0:
                    textArticle = text[0].get_text()
                    filePath = os.path.join(path, name2)
                    if not os.path.isfile(filePath):
                        file = codecs.open(filePath, 'a', encoding='utf8')
                        file.write(textArticle)
                        file.close()
            count += 1

        print (category)

scrapeAnsa()