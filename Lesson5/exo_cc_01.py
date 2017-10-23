import requests
import logging
import re
import json
import pandas as pd


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


def getMedicaments(medicament):

    result = []
    i =0
    while(True):
        i += 1
        url = 'https://www.open-medicaments.fr/api/v1/medicaments?query='+str(medicament)+'&page='+str(i)+'&limit=50'
        response = getContent(url)
        lst_medicament = json.loads(response)
        print(url)
        print(len(lst_medicament))
        if(len(lst_medicament) > 0):
            result.extend(getMedicament(medicament['codeCIS']) for medicament in lst_medicament)
        else:
            break
    
    return result


def getMedicament(id):
    url = 'https://www.open-medicaments.fr/api/v1/medicaments/'+ str(id)

    medicament = {}

    response = getContent(url)
    infos = json.loads(response)
    
    medicament['id'] = infos['codeCIS']
    medicament['composition'] = ''.join(re.findall("\d+", infos["denomination"]))
    medicament['formePharmaceutique'] = infos['formePharmaceutique']
    medicament['homeopathie'] = infos['homeopathie']
    medicament['titulaires'] = infos['titulaires'][0]
    medicament['dateAMM'] = infos['dateAMM']
    
    return medicament
    

def main():
    results = getMedicaments("ibuprofene")
    
    dataframe = pd.DataFrame().from_dict(results)

    dataframe.to_csv('/home/nazha/tmp/medicament.csv', index=False)

    
if __name__ == '__main__':
    main()