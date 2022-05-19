###############################################
# Script d'extract des critiques SensCritique #                    
###############################################

# Librairies
import requests
import json
import csv
from datetime import datetime
import time
import random
import re

# Constante
url = "https://apollo.senscritique.com"
url2 = "https://www.senscritique.com/"

# Paramètres
user = input("Utilisateur : ")
page_start = int(input("Page initiale : "))
page_end = int(input("Page finale : "))
debugInput = input("Debug : True Or False?")
if debugInput == "True" : debug = True
else : debug = False

# Construction préfixe URL de critique
url3 =url2+user+"/critiques"
get0 = requests.get(url3)
pattern = "_buildManifest.js(.*?)_ssgManifest.js"
codeQuiChangeToutLeTemps = re.search(pattern, get0.text).group(1)
pattern = "static/(.*?)/"
codeQuiChangeToutLeTemps = re.search(pattern, codeQuiChangeToutLeTemps).group(1)
urlPrefix = url2+"_next/data/"+codeQuiChangeToutLeTemps+"/fr/universe/"

# Init du canal avec requête options 
get = requests.options(url)

# Création du fichier csv de réception
now = datetime.now()
date = now.strftime("%m%d%Y")
csvfile = open("bibCritique_"+date+".csv", "a", newline="")
fieldnamesValue=["Titre","Lien", "Critique"]
csvDict = csv.DictWriter(csvfile,delimiter=";",fieldnames=fieldnamesValue)

# Boucle sur les pages
for x in range(page_start, page_end+1):

    # Ajout du header
    if x == 1:
        csvDict.writeheader()

    print("Debut extract page "+str(x))

    # Calcul de l'offset
    offset = (x -1)*6

    # Payload et header de la requête post
    payload = json.dumps([
      {
        "operationName": "UserReviews",
        "variables": {
          "limit": 6,
          "offset": offset,
          "order": "DATE_EDIT_DESC",
          "showLiked": False,
          "status": "PUBLISHED",
          "universe": None,
          "username": user
        },
        "query": "query UserReviews($username: String!, $offset: Int, $limit: Int, $order: UserReviewsSort, $showLiked: Boolean, $status: ReviewStatus, $universe: String) {\n  user(username: $username) {\n    ...UserMinimal\n    ...ProfileStats\n    reviewCount\n    reviewsCreated(\n      limit: $limit\n      offset: $offset\n      order: $order\n      showLiked: $showLiked\n      status: $status\n      universe: $universe\n    ) {\n      total\n      items {\n        author {\n          name\n          username\n          __typename\n        }\n        bodyShort\n        commentCount\n        dateCreation\n        id\n        likeCount\n        product {\n          id\n          title\n          medias {\n            picture\n            __typename\n          }\n          universe\n          url\n          yearOfProduction\n          __typename\n        }\n        rating\n        title\n        url\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserMinimal on User {\n  ...UserNano\n  settings {\n    about\n    birthDate\n    country\n    dateLastSession\n    displayedName\n    email\n    firstName\n    gender\n    lastName\n    privacyName\n    privacyProfile\n    showAge\n    showProfileType\n    urlWebsite\n    username\n    zipCode\n    __typename\n  }\n  __typename\n}\n\nfragment UserNano on User {\n  following\n  id\n  isBlocked\n  isScout\n  name\n  reviewCount\n  url\n  username\n  medias {\n    avatar\n    backdrop\n    __typename\n  }\n  __typename\n}\n\nfragment ProfileStats on User {\n  likePositiveCountStats {\n    contact\n    feed\n    list\n    paramIndex\n    review\n    total\n    __typename\n  }\n  stats {\n    collectionCount\n    diaryCount\n    listCount\n    followerCount\n    ratingCount\n    reviewCount\n    scoutCount\n    __typename\n  }\n  __typename\n}\n"
      }
    ])
    headers = {
      'Content-Type': 'application/json'
    }

    # Exécution de la requête post
    response = requests.request("POST", url, headers=headers, data=payload)

    # Récupération du json issu du body de la response
    bib = json.loads(response.text)
       
    j = 0

    # Boucle d'écriture des lignes dans le csv
    for i in bib[0]['data']['user']['reviewsCreated']['items'] :
    
        j += 1
        if debug: 
            # Génération fichier  
            f = open("test.txt", "a", encoding="utf-8")
            f.write(response.text)
            f.close()
   
        print("Début extract critique "+str(j))
        
        # Set du titre
        titre = i['title']
        if debug:
            print(str(j) +" - "+titre)
        
        # Set du lien
        lien = i['url']
        if debug:
            print(str(j) +" - "+lien)
        
        # Set de l'id               
        idcritique = i['id']
        if debug:
            print(str(j) +" - "+str(idcritique))
        
        # Set du slug       
        m = re.split(r'(\W+)', lien)
        slug = m[4]
        if debug:
            print(str(j) +" - "+slug)
            
        # Call lien
        get2 = requests.get(urlPrefix+slug+"/critique/"+str(idcritique)+".json")
        
        # Récupération du json issu du body de la response
        bib2 = json.loads(get2.text)
        critique = bib2['pageProps']['__APOLLO_STATE__']['Review:'+str(idcritique)]['bodyText']
        critique = critique.replace('&#39;', '\'')
        critique = critique.replace('&quot;', '"')
        critique = critique.replace('</p><p>', ' ')
        critique = critique.replace('<p>', '')
        critique = critique.replace('</p>', '')
        if debug:
            print(str(j) +" - "+critique)
             
        # Ecriture d'une ligne
        csvDict.writerow({'Titre': titre, 'Lien':lien, 'Critique': critique})
        
        # Wait aléatoire
        time.sleep(random.randint(1,3))
        
        print("Fin extract critique "+str(j))
        
        
    print("Fin extract page "+str(x))
    
    # Wait aléatoire
    time.sleep(random.randint(1,3))

# Fermeture fichier
csvfile.close()