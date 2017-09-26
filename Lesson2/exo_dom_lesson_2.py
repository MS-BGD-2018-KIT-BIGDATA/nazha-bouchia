# Charles Miglietti 's order:
# Comme exercice pour la semaine prochaine je vous demande de crawler le résultat des comptes de la ville 
# de Paris pour les exercices 2010 à 2015.
# Voici par exemple les comptes pour 2013 (http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013)  . 
# Je vous demande de récupérer les données A,B,C et D sur les colonnes Euros par habitant et par strate.
#
#
# Personal steps and notes:
# STEP1: Make a program that return a result for paris and years 2010-2015 [DONE]
# STEP2: Improve the program:  parametrizing years and paris [TODO]
# STEP3: Improve the program: manage and log errors [TODO]
# STEP4: Improve the program: parallelize extract_ABDC_Indicators (one thread by year) [TODO]
#

import requests
import bs4
import logging

base_url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='


def extract_ABDC_Indicators(year):
    """
    :param year: year
    :type year: int
    :return: list that contains the indicators A,B,C,D by habitant and by strate
    [A_By_Habitant, A_By_Strate, B_By_Habitant, B_By_Strate, C_By_Habitant, C_By_Strate, D_By_Habitant, D_By_Strate]
    :rtype: list
    """
    try:

        url = base_url+str(year)
        response = requests.get(url)

        if(response.status_code != 200):
            logging.error("Invalid Status_Code[%s] for URL: %s", response.status_code, url)
            return []

        parser = bs4.BeautifulSoup(response.content, 'html.parser')
        findAllTotalMontant = parser.find_all(attrs={"class": "montantpetit G"})

        return list(map(lambda i: extractMontant(findAllTotalMontant, i), [1, 2, 4, 5, 10, 11, 13, 14]))

    except requests.exceptions.ConnectionError as e:
        logging.error("HTTP connexion error or Invalid URL: %s", url)
        return []

def extractMontant(montants, index):
    return int(montants[index].string.replace(' ', ''))


def main():
    result = {year: extract_ABDC_Indicators(year) for year in range(2010,2016)}
    print(result)

if __name__ == '__main__':
    main()
