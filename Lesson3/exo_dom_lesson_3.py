# ENONCE DU T.P:
#
#- Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075 
#- En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users le nombre moyens de stars des repositories qui leur appartiennent. 
#  Pour finir classer ces 256 contributors par leur note moyenne.﻿
#

import multiprocessing as mp
import requests
import bs4
import json
import logging
import numpy as np

file = open("/home/nazha/secret.txt", "r") 
basic_auth = file.read().rstrip('\n')

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


def extractMostActiveGitHubUsers():
    r"""Extract the most 256 active GitHub users. Scrawling from https://gist.github.com/paulmillr/2657075
    :return: List of the GitHub users
    :rtype: list
    """
    url = 'https://gist.github.com/paulmillr/2657075'

    try:
        response = getContent(url)
        parser = bs4.BeautifulSoup(response, 'html.parser')
        ths = parser.find_all('th', attrs={"scope":"row"})
        return [th.parent.td.a.text for th in ths]

    except Exception as e:
        logging.error("An unexpected exception occurred:: %s", e)
        raise e
    

def extractStargazersCount(username):
    r"""Extract for a user, all stargazer count for his repositories.
        API REST - https://api.github.com/users/:username/repos
    :param username: github username
    :type username: str
    :return: username and starcount's list 
    :rtype: list
    """
    url = 'https://api.github.com/users/'+username+'/repos'
    starsCount = [0]
    try:
        response = getContent(url, headers = {'Authorization': 'Basic '+basic_auth})
        if(response):
            repos = json.loads(response)
            if(len(repos) > 0):
                starsCount = [repo['stargazers_count'] for repo in repos]

    except json.JSONDecodeError as e:
        logging.error("JSON not valid - %s : %s", e, response)
    except Exception as e:
        logging.error("An unexpected exception occurred:: %s", e)
        raise e
        
    return (username, starsCount)

def main():    
    users = extractMostActiveGitHubUsers()
    if(len(users) > 0):
        pool = mp.Pool(processes=15)
        results = pool.map(extractStargazersCount, users)
        results_bymean = {result[0]:np.mean(result[1]) for result in results}
        sorted_results = sorted(results_bymean.items(), key=lambda result: result[1], reverse=True)
        for result in sorted_results:
            print('{} : {}'.format(result[0], result[1]))

if __name__ == '__main__':
    main()


