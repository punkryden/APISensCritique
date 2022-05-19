#############################################
# Script d'extract des données SensCritique #                    
#############################################

# Librairies
import requests
import json
import csv
from datetime import datetime
import time
import random

# Constante
url = "https://apollo.senscritique.com"

# Paramètres
user = input("Utilisateur : ")
page_start = int(input("Page initiale : "))
page_end = int(input("Page finale : "))
debugInput = input("Debug : True Or False?")
if debugInput == "True" : debug = True
else : debug = False

# Init du canal avec requête options 
get = requests.options(url)

# Création du fichier csv de réception
now = datetime.now()
date = now.strftime("%m%d%Y")
csvfile = open("bibNote_"+date+".csv", "a", newline="", encoding="utf-8")
fieldnamesValue=["Titre","Artiste", "Année","Catégorie","Note"]
csvDict = csv.DictWriter(csvfile,delimiter=";",fieldnames=fieldnamesValue)

# Boucle sur les pages
for x in range(page_start, page_end+1):

    # Ajout du header
    if x == 1:
        csvDict.writeheader()

    print("Debut extract page "+str(x))

    # Calcul de l'offset
    offset = (x -1)*18

    # Payload et header de la requête post
    payload = json.dumps([
      {
        "operationName": "UserCollection",
        "variables": {
          "action": None,
          "categoryId": None,
          "gameSystemId": None,
          "genreId": None,
          "keywords": None,
          "limit": 18,
          "offset": offset,
          "order": "LAST_ACTION_DESC",
          "universe": None,
          "username": user,
          "yearDateDone": None,
          "yearDateRelease": None
        },
        "query": "query UserCollection($action: ProductAction, $categoryId: Int, $gameSystemId: Int, $genreId: Int, $isAgenda: Boolean, $keywords: String, $limit: Int, $month: Int, $offset: Int, $order: CollectionSort, $showTvAgenda: Boolean, $universe: String, $username: String!, $versus: Boolean, $year: Int, $yearDateDone: Int, $yearDateRelease: Int) {\n  user(username: $username) {\n    ...UserMinimal\n    ...ProfileStats\n    notificationSettings {\n      alertAgenda\n      __typename\n    }\n    collection(\n      action: $action\n      categoryId: $categoryId\n      gameSystemId: $gameSystemId\n      genreId: $genreId\n      isAgenda: $isAgenda\n      keywords: $keywords\n      limit: $limit\n      month: $month\n      offset: $offset\n      order: $order\n      showTvAgenda: $showTvAgenda\n      universe: $universe\n      versus: $versus\n      year: $year\n      yearDateDone: $yearDateDone\n      yearDateRelease: $yearDateRelease\n    ) {\n      total\n      filters {\n        action {\n          count\n          label\n          value\n          __typename\n        }\n        category {\n          count\n          label\n          value\n          __typename\n        }\n        gamesystem {\n          count\n          label\n          value\n          __typename\n        }\n        genre {\n          count\n          label\n          value\n          __typename\n        }\n        monthDateDone {\n          count\n          label\n          value\n          __typename\n        }\n        releaseDate {\n          count\n          label\n          value\n          __typename\n        }\n        universe {\n          count\n          label\n          value\n          __typename\n        }\n        yearDateDone {\n          count\n          label\n          value\n          __typename\n        }\n        __typename\n      }\n      products {\n        ...ProductMinimal\n        preloadedParentTvShow {\n          ...ProductMinimal\n          __typename\n        }\n        scoutsAverage {\n          average\n          count\n          __typename\n        }\n        currentUserInfos {\n          ...ProductUserInfos\n          __typename\n        }\n        otherUserInfos(username: $username) {\n          ...ProductUserInfos\n          lists {\n            id\n            label\n            listSubtype\n            url\n            __typename\n          }\n          review {\n            id\n            title\n            url\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      tvProducts {\n        infos {\n          channel {\n            id\n            label\n            __typename\n          }\n          showTimes {\n            id\n            dateEnd\n            dateStart\n            __typename\n          }\n          __typename\n        }\n        product {\n          ...ProductMinimal\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserMinimal on User {\n  ...UserNano\n  settings {\n    about\n    birthDate\n    country\n    dateLastSession\n    displayedName\n    email\n    firstName\n    gender\n    lastName\n    privacyName\n    privacyProfile\n    showAge\n    showProfileType\n    urlWebsite\n    username\n    zipCode\n    __typename\n  }\n  __typename\n}\n\nfragment UserNano on User {\n  following\n  id\n  isBlocked\n  isScout\n  name\n  reviewCount\n  url\n  username\n  medias {\n    avatar\n    backdrop\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMinimal on Product {\n  ...ProductNano\n  category\n  channel\n  dateCreation\n  dateLastUpdate\n  dateRelease\n  dateReleaseEarlyAccess\n  dateReleaseJP\n  dateReleaseOriginal\n  dateReleaseUS\n  displayedYear\n  duration\n  episodeNumber\n  frenchReleaseDate\n  listCount\n  numberOfEpisodes\n  numberOfSeasons\n  originalRun\n  originalTitle\n  parentTvShowId\n  productionStatus\n  retailReleaseDate\n  seasonId\n  seasonNumber\n  subtitle\n  synopsis\n  url\n  actors {\n    name\n    person_id\n    url\n    __typename\n  }\n  artists {\n    name\n    person_id\n    url\n    __typename\n  }\n  authors {\n    name\n    person_id\n    url\n    __typename\n  }\n  tvChannel {\n    name\n    url\n    __typename\n  }\n  countries {\n    id\n    name\n    __typename\n  }\n  creators {\n    name\n    person_id\n    url\n    __typename\n  }\n  developers {\n    name\n    person_id\n    url\n    __typename\n  }\n  directors {\n    name\n    person_id\n    url\n    __typename\n  }\n  distributors {\n    name\n    person_id\n    url\n    __typename\n  }\n  franchises {\n    id\n    label\n    slug\n    url\n    __typename\n  }\n  gameSystems {\n    id\n    label\n    __typename\n  }\n  genresInfos {\n    id\n    label\n    slug\n    url\n    __typename\n  }\n  illustrators {\n    name\n    person_id\n    url\n    __typename\n  }\n  isbn\n  medias(backdropSize: \"1200\") {\n    randomBackdrop\n    backdrop\n    picture\n    screenshot\n    videos {\n      id\n      image\n      provider\n      type\n      __typename\n    }\n    __typename\n  }\n  musicLabels {\n    name\n    person_id\n    url\n    __typename\n  }\n  pencillers {\n    name\n    person_id\n    url\n    __typename\n  }\n  producers {\n    name\n    person_id\n    url\n    __typename\n  }\n  publishers {\n    name\n    person_id\n    url\n    __typename\n  }\n  soundtracks {\n    id\n    title\n    url\n    __typename\n  }\n  stats {\n    currentCount\n    ratingCount\n    recommendCount\n    reviewCount\n    wishCount\n    __typename\n  }\n  translators {\n    name\n    person_id\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProductNano on Product {\n  id\n  rating\n  title\n  universe\n  url\n  yearOfProduction\n  medias(backdropSize: \"1200\") {\n    backdrop\n    picture\n    screenshot\n    __typename\n  }\n  __typename\n}\n\nfragment ProductUserInfos on ProductUserInfos {\n  dateDone\n  hasStartedReview\n  isCurrent\n  id\n  isDone\n  isListed\n  isRecommended\n  isRejected\n  isReviewed\n  isWished\n  productId\n  rating\n  userId\n  gameSystem {\n    id\n    label\n    __typename\n  }\n  lastEpisodeDone {\n    id\n    episodeNumber\n    __typename\n  }\n  review {\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProfileStats on User {\n  likePositiveCountStats {\n    contact\n    feed\n    list\n    paramIndex\n    review\n    total\n    __typename\n  }\n  stats {\n    collectionCount\n    diaryCount\n    listCount\n    followerCount\n    ratingCount\n    reviewCount\n    scoutCount\n    __typename\n  }\n  __typename\n}\n"
      }
    ])
    headers = {
      'Content-Type': 'application/json'
    }

    # Exécution de la requête post
    response = requests.request("POST", url, headers=headers, data=payload)

    # Récupération du json issu du body de la response
    bib = json.loads(response.text)
    
    if debug:
        j = 0

    # Boucle d'écriture des lignes dans le csv
    for i in bib[0]['data']['user']['collection']['products'] :
    
        if debug:
            j += 1
            # Génération fichier  
            f = open("test.txt", "a", encoding="utf-8")
            f.write(response.text)
            f.close()
        
        # Set du titre
        titre = i['title']
        if debug:
            print(str(j) +" - "+titre)
        
        # Set de l'année
        annee = 0000
        annee = i['yearOfProduction']
        if annee == None: 
            if i.get("dateReleaseOriginal"): annee = int(i['dateReleaseOriginal'][:4])
        if annee == None: 
            if i.get("dateRelease"): annee = i['dateRelease'][-4:]
        if annee == None: 
            if i.get("frenchReleaseDate"): annee = i['frenchReleaseDate'][:4]
        if debug:
            print(str(j) +" - "+str(annee))
        
        # Set de la catégorie
        categorie = i['category']
        if i['universe'] == 2: categorie = "Livre"
        if debug:
            print(str(j) +" - "+categorie)
        
        # Set de l'artiste
        artiste = "NULL"
        #Film
        if i['universe'] == 1: 
            if i.get("directors") : artiste = i['directors'][0]['name']
        #Livre    
        if i['universe'] == 2: 
            if i.get("authors") : artiste = i['authors'][0]['name']
        # Jeu-vidéo
        if i['universe'] == 3: 
            if i.get("developers") : artiste = i['developers'][0]['name']
        # Série
        if i['universe'] == 4: 
            if i.get("creators") : artiste = i['creators'][0]['name']
        #BD
        if i['universe'] == 6: 
            if i.get("authors") : artiste = i['authors'][0]['name']
        #Musique
        if i['universe'] == 7:
            if i.get("artists") : artiste = i['artists'][0]['name']
        if debug:
            print(str(j) +" - "+artiste)
        
        # Set de la note/statut
        note = i['otherUserInfos']['rating']
        wished = i['otherUserInfos']['isWished']
        if wished==True:note="Envie"
        current = i['otherUserInfos']['isCurrent']
        if current==True:note="En cours"
        
        # Ecriture d'une ligne
        csvDict.writerow({'Titre': titre, 'Artiste':artiste, 'Année': annee, 'Catégorie': categorie, 'Note': note})
        
    print("Fin extract page "+str(x))
    
    # Wait aléatoire
    time.sleep(random.randint(1,3))

# Fermeture fichier
csvfile.close()

#############################################
# Outil Debugging                           #                    
#############################################

if debug:

    ## Tests titre
    j = 0
    for i in bib[0]['data']['user']['collection']['products'] :
        titre = i['title']
        j = j + 1
        print(titre+" - "+ str(j))
     
    # Test catégorie 
    j = 0
    for i in bib[0]['data']['user']['collection']['products'] :
        categorie = i['category']
        if i['universe'] == 2: categorie = "Livre"
        j = j + 1
        print(categorie+" - "+ str(j))

    # Test artiste     
    j = 0
    for i in bib[0]['data']['user']['collection']['products'] :
        i['universe']
        artiste = "NULL"
        #Film
        if i['universe'] == 1: 
            if i.get("directors") : artiste = i['directors'][0]['name']
        #Livre    
        if i['universe'] == 2: 
            if i.get("authors") : artiste = i['authors'][0]['name']
        # Jeu-vidéo
        if i['universe'] == 3: 
            if i.get("developers") : artiste = i['developers'][0]['name']
        # Série
        if i['universe'] == 4: 
            if i.get("creators") : artiste = i['creators'][0]['name']
        #BD
        if i['universe'] == 6: 
            if i.get("authors") : artiste = i['authors'][0]['name']
        #Musique
        if i['universe'] == 7:
            if i.get("artists") : artiste = i['artists'][0]['name']
        j = j + 1
        print(artiste+" - "+ str(j))

    # Test annee  
    j = 0
    for i in bib[0]['data']['user']['collection']['products'] :
        annee = "0000"
        annee = i['yearOfProduction']
        if annee == None: 
            if i.get("dateReleaseOriginal"): annee = int(i['dateReleaseOriginal'][:4])
        if annee == None: 
            if i.get("dateRelease"): annee = i['dateRelease'][-4:]
        if annee == None: 
            if i.get("frenchReleaseDate"): annee = i['frenchReleaseDate'][:4]
        j = j + 1
        print(str(annee)+" - "+ str(j))

    