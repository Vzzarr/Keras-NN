import requests
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import codecs
import re

linksRssMessaggero = [
    'http://www.ilmessaggero.it/rss/sport.xml|sport',
    'http://www.ilmessaggero.it/rss/tecnologia.xml|scienza&tecnologia',
    'http://www.ilmessaggero.it/rss/societa.xml|societa',
    'http://www.ilmessaggero.it/rss/economia.xml|economia',
    'http://www.ilmessaggero.it/rss/cultura.xml|cultura',
    'http://www.ilmessaggero.it/rss/spettacoli.xml|cultura',
 ]


def scrapeMessaggero() :
    for link_category in linksRssMessaggero:
        pageRss = requests.get(link_category.split("|")[0])
        category = link_category.split("|")[1]
        xmlfile = ET.fromstring(pageRss.content)

        numberLinks = 0

        #for links in xmlfile.iter('link'):
          #  numberLinks += 1
        #trainigPercent = (numberLinks * 80) / 100
        #testPercent = numberLinks - trainigPercent

        count = 0

        #print (numberLinks)
        #print (trainigPercent)

        for links in xmlfile.iter('link'):

            #if count < trainigPercent:
            path = "/home/nicholas/Documenti/Keras-NN/mario/training/" + category
            if not os.path.exists(path):
                os.makedirs(path)
            #else:
            #    path = "/home/nicholas/Documenti/Keras-NN/messaggero/test/" + category
            #    if not os.path.exists(path):
            #        os.makedirs(path)

            if count > 0:
                page = requests.get(links.text).content
                corpo_content = '<div class="corpo-content">' in page
                testo_nero14_testodim = '<div class="testo nero14 testodim"' in page
                corpo = '<div class="corpo">' in page
                if corpo_content or testo_nero14_testodim or corpo :
                    if corpo_content :
                        text = BeautifulSoup(page, 'html.parser').find_all(class_="corpo-content")[0].find_all('p')
                    elif testo_nero14_testodim :
                        text = BeautifulSoup(page, 'html.parser').find_all(class_="testo nero14 testodim")
                    elif corpo :
                        text = BeautifulSoup(page, 'html.parser').find_all(class_="corpo")
                    name1 = re.sub("http(.*/)+", "", links.text)
                    name2 = re.sub(r'[^\w]+', "", name1)
                    if len(text) > 0:
                        textArticle = text[0].get_text()
                        filePath = os.path.join(path, name2)
                        print(textArticle)
                        if not os.path.isfile(filePath):
                            file = codecs.open(filePath, 'a', encoding='utf8')
                            file.write(textArticle)
                            file.close()
            count += 1

        print (category)

scrapeMessaggero()