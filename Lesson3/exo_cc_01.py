#
# ACER vs DELL sur CDiscount
#
#
#

import requests
import bs4
import logging

base_url = "https://www.cdiscount.com/search/10/"


def extractProducts(product):
    try:

        url = base_url + product + '.html'
        response = requests.get(url)
        hrefs = []

        if(response.status_code != 200):
            logging.error("Invalid Status_Code[%s] for URL: %s", response.status_code, url)
            return []

        parser = bs4.BeautifulSoup(response.content, 'html.parser')
        prdtBlocs = parser.find_all("div", attrs={"class": "prdtBloc"})
        for prdtBloc in prdtBlocs:
            hrefs.append(prdtBloc.a['href'])

    except requests.exceptions.ConnectionError as e:
        logging.error("HTTP connexion error or Invalid URL: %s", url)
        return []

    return hrefs

    
def extractPrices(url):
    try:
        print(url)

        response = requests.get(url)

        if(response.status_code != 200):
            logging.error("Invalid Status_Code[%s] for URL: %s", response.status_code, url)
            return []

        parser = bs4.BeautifulSoup(response.content, 'html.parser')

        fpBlocPrice = parser.find_all("div", attrs={"id": "fpBlocPrice"})
        
        prdtBZPrices = fpBlocPrice[0].find("span", attrs={"class": "fpPrice", "itemprop": "price"})
        fpStriked = prdtBZPrices.parent.find(attrs={"class": "fpStriked"})
        if(fpStriked):
            print("(Price, Striked Price):", (prdtBZPrices.get('content'), fpStriked.text.rstrip(' €*')))
        else:
            print("(Price, No Striked Price):", prdtBZPrices.get('content'))

    except requests.exceptions.ConnectionError as e:
        logging.error("HTTP connexion error or Invalid URL: %s", url)
        return []
    

def main():
    hrefs = extractProducts("dell")
    for href in hrefs:
        extractPrices(href)

if __name__ == '__main__':
    main()
