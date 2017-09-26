# From purepeople's web site:
#   search for the last ten press article for a person, and for each article extract the shared count
#
# Result is a dictionary with key:person and value:list of shared count
# 
# Articles are obtained by calling one of the two URL :
# http://www.purepeople.com/rechercher/q/%SEARCHED_PERSON%/cat/article/np/1
# or
# http://www.purepeople.com/rechercher/?q=toto (GET OR POST)
#


import requests
import bs4
import logging

base_url = 'http://www.purepeople.com'
search_url = base_url + '/rechercher/'

people = {'Toto', 'Angelina', 'Jennyfer', 'Shy''m', 'Mika'}

def extractSharedCountForTheLast10Views(person):
    """
    :param person: Person
    :type person: string
    :return: dictionary with person and last 10 shared count
    :rtype: dict
    """

    try:    
        # Step1: search the last 10 views
        response = requests.post(search_url, params={'q':person})
        if(response.status_code != 200):
            logging.error("Invalid Status_Code[%s] for URL: %s", response.status_code, search_url)
            return []
        
        # Step2: For each views find his shared count
        sharedCounts = []
        parser = bs4.BeautifulSoup(response.content, 'html.parser')
        articles = parser.find_all(attrs={"data-type": "article"})
        for article in articles:
            a= article.find('a', href=True, text=True)
            href = a.get('href')
            sharedCounts.append(getSharedCount(base_url+href))
            
        return sharedCounts

    except requests.exceptions.ConnectionError as e:
        logging.error("HTTP connexion error or Invalid URL: %s", search_url)


def getSharedCount(articleURL):
    """ Return the shared count for an article from purepeople.com
    :param articleURL: URL's article
    :type articleURL: string
    :return: the shared count for the article
    :rtype: int
    """
    try:
        response = requests.get(articleURL)
        if(response.status_code != 200):
            return
    
        parser = bs4.BeautifulSoup(response.content, 'html.parser')
        sharedcount = parser.find("span", attrs={"class": "c-sharebox__stats-number count"}).text.strip()
        return (convert(sharedcount.replace(',','.')))
    except requests.exceptions.ConnectionError:
        logging.error("HTTP connexion error or Invalid URL: %s", articleURL)
        return 0

def convert(val):
    lookup = {'K': 1000, 'M': 1000000}
    unit = val[-1].upper()
        
    if unit in lookup:
        return int(lookup[unit] * float(val[:-1]))
    return int(val)


def main():
    result = {}
    for person in people:
        sharedCounts = extractSharedCountForTheLast10Views(person)
        result[person] = sharedCounts
    print(result)

if __name__ == '__main__':
    main()