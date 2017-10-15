import requests
import json
import numpy as np
import pandas as pd
import logging


base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
apikey = ' AIzaSyBDe3r0NT7mXnvTiYi6eOBhLpanhhVNp6U '

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


def getBiggestTown(n):
    return ['Lyon', 'Paris', 'Bordeaux', 'Marseille', 'Toulouse']

# Test chain function
#
#

def getDistanceMatrix(towns):
    url = base_url + '|'.join(towns) + '&destinations=' + '|'.join(towns) + '&key='+apikey

    result = []
    try:
        response = getContent(url)
    
        if(response):
            jresponse = json.loads(response)
            rows = jresponse['rows']

#            list(map (x,y): ([x,y]))
            
            return [[x['distance']['value'] for x in element['elements']] for element in rows]
        
    except json.JSONDecodeError as e:
        logging.error("JSON not valid - %s : %s", e, response)
    except Exception as e:
        logging.error("An unexpected exception occurred:: %s", e)
        raise e

    return np.array(result)

def extractDistance(element):
    return element['distance']['value']

def main():
    
    towns = getBiggestTown(4)
    matrix = getDistanceMatrix(towns)
    
    df = pd.DataFrame(matrix, columns = towns)
    df.to_csv("/home/nazha/tmp/lesson3.csv")

    
if __name__ == '__main__':
    main()

