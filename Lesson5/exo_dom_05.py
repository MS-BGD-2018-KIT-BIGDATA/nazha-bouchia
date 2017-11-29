# ENONCE DU T.P
# 
# Peut-on établir un lien entre la densité de médecins par spécialité et par territoire et la pratique du dépassement d'honoraires ? 
# Est-ce dans les territoires où la densité est la plus forte que les médecins  pratiquent le moins les dépassement d'honoraires ? 
# Est ce que la densité de certains médecins / praticiens est corrélé à la densité de population pour certaines classes d'ages 
# (bebe/pediatre, personnes agées / infirmiers etc...) ?
#
# C'est un sujet assez ouvert pris du Hackathon "données de santé" de Etalab. 
# Il y a un github qui contient une partie des données dont vous aurez besoin. 
# Vous pouvez compléter ça avec de l'INSEE et des données sur la démographie des médecins.
#

import pandas as pd
import pygal 
import re
#from pygal.maps.fr import aggregate_regions


def display_densite_medecin():
    densite_medecin = pd.read_csv("data_medical/TCRD_068-2.csv", sep=',');
    
    densite_medecin['Ensemble des médecins'] = densite_medecin['Ensemble des médecins'].apply(lambda x: re.sub("[^0-9]", "", x))
    densite_medecin['Numéro département']
    densite_medecin_by_dep = dict([(b,int(a)) for b, a in zip(densite_medecin['Numéro département'], densite_medecin['Ensemble des médecins'])])
    
    fr_chart = pygal.maps.fr.Departments(human_readable=True)
    fr_chart.title = 'Densité des médecins par département'
    fr_chart.add('En 2016', densite_medecin_by_dep)
    fr_chart.render_to_png('img/densite_medecins_par_departement.png')
    

def main():
    display_densite_medecin()


if __name__ == '__main__':
    main()
