# ENONCE DU T.P
# L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion 
# en Ile de France, PACA et Aquitaine. 
#
# Vous utiliserez leboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes : 
#   - version ( il y en a 3) (ZEN, LIFE, INTENS)
#   - année
#   - kilométrage
#   - prix
#   - téléphone du propriétaire
#   - est ce que la voiture est vendue par un professionnel ou un particulier.
#
# Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site 
# http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.
# 
# Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
# Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.
#

# THIS TIME TEST THREAD INSTEAD MULTIPROCESSING
# TODO : TO IMPROVE THE PROGRAM : SET A CACHE FOR ARGUS
# TODO : EXTRACT ALL PAGES
#


from threading import Thread
import requests
import bs4
import logging
import re
import json
import pandas as pd

class MyThread(Thread):

    infos = {'Modèle':'alpha', 'Année-modèle':'num', 'Kilométrage':'num', 'Prix':'num'}

    def __init__(self, val, region):
        ''' Constructor. '''
        Thread.__init__(self)
        self.val = val
        self.region = region
        self.results = []

    def parseInfo(self, parser, info, typeof_info):
        spaninfo = parser.find("span", text=info)
        text = spaninfo.parent.find("span", attrs={"class":"value"}).text
        
        if(typeof_info == 'num'):
            return int(''.join(re.findall("\d+", text)))
        elif(typeof_info == 'alpha'):
            return ''.join(re.findall("\w+", text))
    
        return ''


    def extractArgus(self, version, annee):
        url = 'https://www.lacentrale.fr/cote-auto-renault-zoe-'+version+'-'+str(annee)+'.html'
        response = getContent(url)
        parser = bs4.BeautifulSoup(response, 'html.parser')
        jsRefinedQuot = parser.find(attrs={"class":"jsRefinedQuot"}).text
        argus = int(''.join(re.findall("\d+", jsRefinedQuot)))
        return argus


    def extractInformation(self, url):
        response = getContent(url)
        parser = bs4.BeautifulSoup(response, 'html.parser')    
        return {info: self.parseInfo(parser,info, typeof_info) for info, typeof_info in self.infos.items()}
    
    def extractAllInformation(self, annonce):
        result = {}
        href = 'http:'+annonce.get('href')
        result['ID'] = re.findall(r"\d+", href)[0]
        result['Region'] = self.region
        result['Type'] = json.loads(annonce.get('data-info'))['ad_offres']
        result['Title'] = annonce.get('title')
        versions = re.findall("(zen|intens|life){1}", result['Title'].lower())
        version = 'intens'
        if(len(versions)) :
            version = versions[0]
        result['Version'] = version
        #
        result.update(self.extractInformation(href))
        # Get Argus
        result['Argus'] = self.extractArgus(result['Version'], result['Année-modèle'])
        return result


    def run(self):
        response = getContent('https://www.leboncoin.fr/voitures/offres/'+self.region+'/?th=2&brd=Renault&mdl=Zoe')
    
        parser = bs4.BeautifulSoup(response, 'html.parser')
    
        annonces = parser.find_all(attrs={"class":"list_item clearfix trackable"})
        self.results = [self.extractAllInformation(annonce) for annonce in annonces]
    

#phonenumber_url = 'https://api.leboncoin.fr/api/utils/phonenumber.json'
#def getPhoneNumber(apiKey, url):
#    headers = {}
#    headers['Origin'] = 'https://www.leboncoin.fr'
#    headers['Accept-Encoding'] = 'gzip, deflate, br'
#    headers['Accept-Language'] = 'en-US,en;q=0.8,fr;q=0.6'
#    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
#    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
#    headers['Accept'] = '_/_'
#    headers['Referer'] = url
#    headers['Connection'] = 'keep-alive'
# 
#    data = {'list_id':'1319136873', 'app_id':'leboncoin_web_utils', 'key':'54bb0281238b45a03f0ee695f73e704f', 'text':'1'}
#    response = requests.post(phonenumber_url, headers=headers, data=data)
#    phonenumber = json.loads(response.content)
#    print(phonenumber)

def getContent(url, headers=None):
    r"""Sends an HTTP GET request with headers
    :param url: request's URL
    :type url: str
    :param headers: headers HTTP
    :type headers: list
    :return: Content response (empty if error occurred)
    :rtype: str
    """
    try:
        response = requests.get(url, headers=headers)

        if(response.status_code != 200):
            logging.error("Invalid Status_Code[%s] for URL: %s", response.status_code, url)
            return ''

    except requests.exceptions.ConnectionError as e:
        logging.error("HTTP connexion error or Invalid URL: %s", url)
        return ''
    
    return response.content




def main():
    
    regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']

    # Démarre tous les threads
    threads = []
    for i in range(0, len(regions)):
       thread = MyThread(i, regions[i])
       thread.start()
       threads.append(thread)
    
    # Attends que tout les threads ont terminés
    for thread in threads:
       thread.join()
       
    # Récupére l'ensemble des résultats
    results = []
    for thread in threads:
       results += thread.results

    dataframe = pd.DataFrame().from_dict(results)
    
    print(dataframe)
    dataframe.to_csv('/home/nazha/tmp/lbc.csv', index=False, columns=['ID', 'Region', 'Type', 'Année-modèle','Kilométrage','Modèle','Prix','Argus', 'Version', 'Title'])

    return 
    
    
if __name__ == '__main__':
    main()