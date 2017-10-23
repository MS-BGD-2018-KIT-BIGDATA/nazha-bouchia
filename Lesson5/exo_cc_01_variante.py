import threading 
import queue 
import requests
import logging
import re
import json
import pandas as pd


#
# TESTING QUEUE
# 
#



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


class Consumer(threading.Thread): 
    def __init__(self, i, queue): 
        threading.Thread.__init__(self)
        self._i = i
        self._queue = queue 
        self._result = []

    def getMedicament(self, id):
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
        self._result.append(medicament)

    def run(self):
        while True: 
            msg = self._queue.get() 
            if msg is None:
                break
            self.getMedicament(msg)


def Producer():

    tqueue = queue.Queue()
  
    threads = []
    for i in range(0, 10):
        thread = Consumer(i, tqueue)
        thread.start()
        threads.append(thread)

    #i = 0
    for i in range(0,2):
        #i += 1
        url = 'https://www.open-medicaments.fr/api/v1/medicaments?query=ibuprofene&page='+str(i)+'&limit=50'
        response = getContent(url)
        lst_medicament = json.loads(response)
        print(i)
        if(len(lst_medicament) > 0):
            for medicament in lst_medicament:
                tqueue.put(medicament['codeCIS'])
        else:
            break

    for thread in threads:
        tqueue.put(None)
        print("STOP")

    for thread in threads:
        thread.join()
        
    # Récupére l'ensemble des résultats
    results = []
    for thread in threads:
       results.extend(thread._result)

    dataframe = pd.DataFrame().from_dict(results)
    dataframe.to_csv('/home/nazha/tmp/medicament-ibuprofene.csv', index=False)

if __name__ == '__main__':
    Producer()