"""Réaliser par:
-BOUKERRAS Hanny
-DJENKI Nabil 
"""
#BIBLIOTHEQUE################################
from bottle import route, run, view,get  
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from html.entities import codepoint2name 
#############################################

"""La fonction qui nous permet de gérer les accents, elle a était adapté a l'url de dblp""" 

def htmlCoding(stringToCode):     
    return ''.join( '=%s=' % codepoint2name[ord(oneChar)]                    
                  if ord(oneChar) in codepoint2name                    
                  else oneChar for oneChar in stringToCode) 
"""    
-1. /authors/{name} : 
Cette route prend le name sous cette forme "nom:prénom" avec la premiére lettre du nom et du prémon en majuscle 
"""
@route('/authors/<name>')
@view("API_2019.tpl")

def authors(name):
    try:  
    #Pour ne prendre que la premiere lettre du nom
        name=name.replace(" ",":")
        PrLet = name[0]
    #Rendre la lettre en minuscule
        PrLet = PrLet.lower()
        
    #Pour gerer les accents on utilise htmlCoding pour code le name
        NameAccent=htmlCoding(name)
    #Lien pour recupere le fichier Xml correspondant a  chaque auteur  
        URL = 'http://dblp.uni-trier.de/pers/xx/'+PrLet+'/'+NameAccent    
    #Telechargement du fichier xml apartir de l'URL precedent  
        DBZ = requests.get(URL)
    #Analyse le fichier XML a partir d'une constante de chaine
        xmlFile = ET.fromstring(DBZ.content)
    #Calculer le nombre des balise r ce qui va nous donne le Nombre de publications et le Nombre de co-auteurs
        nbrp = len(xmlFile.findall('r'))
        nbrc = int(xmlFile.find('coauthors').attrib['n'])
    #URL de la page dblp de l'auteur
        URL = 'http://dblp.uni-trier.de/pers/hd/'+PrLet+'/'+NameAccent
    #Retourner les valeurs au API_2019.tpl  
        return {"a":name.replace(":","-"),"b":nbrp,"e":nbrc,"c":URL }
    except:
        Tab='<h1 align="center">Error: 404 Not Found</h1><h2>URL erreur</h2>'+'<table border="1" cellpadding="10" cellspacing="1" width="100%"><tr><th>La route</th><th>Solution</th>' 
        Tab+='<tr><td>localhost:8080/authors/Nom Prenom</td><td>Le name s ecrit : le nom avec la premiere lettre en majucule apres espace ou deux point ":" ensuite ecrire le prenom avec la premiere lettre en majuscule</td></tr>'
                
        return '<html><body>'+'<BODY BGCOLOR="#FF0000">'+Tab+'</body></html>' 

#********************************************************************************
"""
-2. /authors/{name}/publications : cette route avec name le nom d'un auteur, ell liste les publications d'un auteur
"""
@get('/authors/<name>/publications')
def publications(name):
    try:
    #Initialisela variable qui va recevoir les titres des publications
        name=name.replace(" ",":")
        Titre = ""
        PrLet = name[0]
        PrLet = PrLet.lower()
        NameAccent=htmlCoding(name)
    #Lien pour recuperer le fichier Xml correspondant a chaque auteur  
        URL = 'http://dblp.uni-trier.de/pers/xx/'+PrLet+'/'+NameAccent
    #Telecharger le fichier xml et lire son contenue
        fichier = requests.get(URL)
    #Parser le fichier xml
        xml_res = ET.fromstring(fichier.content)
    #Afficher le fichier
    #Rechcher dans le fichier la balise 'r' 
        resultat = []
        Tabp='<table border="1" cellpadding="10" cellspacing="1" width="100%">'
        for i in xml_res.findall('r'):
            i=i[0]
            publication = []
    #Chercher 'title' et 'year' et concation leurs valeurs dans publications 
            publication.append(i.find('title').text)
            publication.append(i.find('year').text)
            authors = []
    #Boucler i avec le mot cle 'author'
    #Checher 'journal' 
            for author in i.iter('author'):
                authors.append(author.text)
            publication.append(authors)
            resultat.append(publication)
        for j in resultat:
            Titre+='<tr><td>'
            for x in j:
                Titre+='- '+str(x)
                Titre+='</br>'
            Titre+='</tr></td>'
        Tabp+=Titre+'</table>'
        return '<BODY BGCOLOR="#C0C0C0">'+'<h1 align="center">Les publications :</h1>'+Tabp
    except:
        Tab='<h1 align="center">Error: 404 Not Found</h1><h2>URL erreur</h2>'+'<table border="1" cellpadding="10" cellspacing="1" width="100%"><tr><th>La route</th><th>Solution</th>' 
        Tab+='<tr><td>localhost:8080/authors/Nom Prenom/publications</td><td>Le name s ecrit : le nom avec la premiere lettre en majucule apres espace ou deux point ":" ensuite ecrire le prenom avec la premiere lettre en majuscule</td></tr>'         
        return '<html><body>'+'<BODY BGCOLOR="#FF0000">'+Tab+'</body></html>'  

#********************************************************************************
"""
3. /authors/{name}/coauthors : cette route avec name le nom d'un auteur, elle liste les co-auteurs d'un auteur.
"""
@get('/authors/<name>/coauthors')

def coauthors(name):
    try:
        name=name.replace(" ",":")
        string = ""
        PrLet = name[0]
        PrLet = PrLet.lower()
        NameAccent=htmlCoding(name)
    	#definir le lien du fichier
        URL = 'http://dblp.uni-trier.de/pers/xx/'+PrLet+'/'+NameAccent
    	#telecharger le fichier xml et lire son contenue
        fichier = requests.get(URL)
    	#parser le fichier xml
        DBZ = ET.fromstring(fichier.content)
    	#afficher le fichier
        coauthors = DBZ.find('coauthors')
        resultat = []
        for coau in coauthors.findall('co'):
            resultat.append(coau.find('na').text)
            resultat = sorted(resultat, key=lambda name: name[0])
        for i in resultat:
            string+='-'+i
            string+="</br>"
        
        return '<BODY BGCOLOR="#C0C0C0">'+'<h1>Les co-auteurs :</h1>'+string
    except:
        Tab='<h1 align="center">Error: 404 Not Found</h1><h2>URL erreur</h2>'+'<table border="1" cellpadding="10" cellspacing="1" width="100%"><tr><th>La route</th><th>Solution</th>' 
        Tab+='<tr><td>localhost:8080/authors/Nom Prenom/coauthors</td><td>Le name s ecrit : le nom avec la premiere lettre en majucule apres espace ou deux point ":" ensuite ecrire le prenom avec la premiere lettre en majuscule</td></tr>'
                 
        return '<html><body>'+'<BODY BGCOLOR="#FF0000">'+Tab+'</body></html>'

#********************************************************************************
"""
4. /authors/{name}/synthesis : cette route avec name le nom d'un auteur, 
Elle retourne le nom d'un auteur, un tableau pour les conférences et un tableau pour les journaux. 
accepte les parametres start(la page est un nombre naturel positif) et count le nombre de publications a afficher (naturel positif)
accepte order=name pour trier alphabetiquement les publications, ou order=date pour trier par date
"""
@get('/authors/<name>/synthesis')

def synthesis(name):
    try:
        name=name.replace(" ",":")
    	#prendre la priemiere lettre du nom
        PrLet = name[0]
    	#la rendre minuscule (pour le lien car il prendre la premiere lettre)
        PrLet = PrLet.lower()
        NameAccent=htmlCoding(name)
    	#definir le lien du fichier
        URL = 'http://dblp.uni-trier.de/pers/xx/'+PrLet+'/'+NameAccent
        fichier = requests.get(URL)
    	#parser le fichier xml
        journaux = []
        conferences = []
        root = ET.fromstring(fichier.content)
        for publication in root.findall('r'):
            publication = publication[0]
            cle = publication.attrib['key']
            cle = cle.split('/')
            if cle[0] == 'conf':
                conferences.append([publication.find('title').text,publication.find('year').text,publication.find('booktitle').text])
            else:
                if type(publication.find('journal')) == ET.Element:    
                    journaux.append([publication.find('title').text,publication.find('year').text,publication.find('journal').text])
                else:
                    journaux.append([publication.find('title').text,publication.find('year').text,'None'])
                    
        #Aller parser l'html du lien core affin de recupérer le classement core
        TabJ = '<h1 align="center">Les journaux :</h1>'
        TabJ+='<table border="1" cellpadding="10" cellspacing="1" width="100%"><tr><th>Titre</th><th>annee</th><th>Classement CORE</th>'
        for i in journaux:         
            URL_CORE='http://portal.core.edu.au/jnl-ranks/?search='+i[2]+'&by=all&source=ERA2010%0D%0A&sort=atitle&page=1'
            r =requests.get(URL_CORE)
            soup = BeautifulSoup(r.content, "html.parser")
            div1 = soup.find_all('div',attrs={'id':'search'})[0]
            ttt=div1.text.replace('\n','').strip().find('0 Results found')    
        #si il le trouve c'est que elle a un classement CORE sinon en va retourner 'none' (elle n'est pa classé)   
            if ttt == -1:
                tt = div1.find('table')
                tr= tt.find('tr',attrs={'class':'evenrow'})
                td= tr.find_all('td')[3]
                y=td.text.replace('\n','')
                z=y.strip()
            else:
                z='None'
                 
            TabJ+='<tr><td>'+i[0]+'</td><td>'+i[1]+'</td><td>'+z+'</td></tr>'
        TabJ+='</table>'  
    
        #Aller parser l'html du lien core affin de recupérer le classement core
        TabC='<h1 align="center">Les conferences :</h1>'
        TabC+='<table border="1" cellpadding="10" cellspacing="1" width="100%"><tr><th>Titre</th><th>annee</th><th>Classement CORE</th>' 
        for i in conferences:
            URL_CORE='http://portal.core.edu.au/conf-ranks/?search='+i[2]+'&by=all&source=CORE2018&sort=atitle&page=1'
            r =requests.get(URL_CORE)
            soup = BeautifulSoup(r.content, "html.parser")
            div1 = soup.find_all('div',attrs={'id':'search'})[0]
            ttt=div1.text.replace('\n','').strip().find('0 Results found')    
            tt = div1.find('table')
        #si il le trouve c'est que elle a un classement CORE sinon en va retourner 'none' (elle n'est pa classé)  
        
            if ttt == -1:
                tr= tt.find('tr',attrs={'class':'evenrow'})
                td= tr.find_all('td')[3]
                y=td.text.replace('\n','')
                z=y.strip()
            
            else:
                z='None'
                
            TabC+='<tr><td>'+i[0]+'</td><td>'+i[1]+'</td><td>'+z+'</td></tr>'
        TabC+='</table>'
                
        return '<BODY BGCOLOR="#C0C0C0">',TabJ,TabC
    except:
        Tab='<h1 align="center">Error: 404 Not Found</h1><h2>URL erreur</h2>'+'<table border="1" cellpadding="10" cellspacing="1" width="100%"><tr><th>La route</th><th>Solution</th>' 
        Tab+='<tr><td>localhost:8080/authors/Nom Prenom/synthesis</td><td>Le name s ecrit : le nom avec la premiere lettre en majucule apres espace ou deux point ":" ensuite ecrire le prenom avec la premiere lettre en majuscule</td></tr>'
               
        return '<html><body>'+'<BODY BGCOLOR="#FF0000">'+Tab+'</body></html>'
    

run(host='localhost', port=8080,reloader=True)
