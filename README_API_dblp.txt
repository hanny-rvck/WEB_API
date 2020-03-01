************************************************************************************************
                                      API WEB pour le site dblp
************************************************************************************************

C'est une API-Web cod� en python r�alis� par 
des �tudiants M1 informatique sp�cialit� R�seaux a Sorbonne Universit�,
dans le cadre de l'UE PROGRES. 

Pr�requis :
===========
-python 3.O ou version ult�rieur 
-Les Biblioth�que n�cessaire :
          * bottel
          * requests
          * xml.etree.ElementTree
          * bs4
          * html.entities 


Les routes de l'API :
=====================

     1) /authors/{name} 
Avec name le nom d'un auteur, 
elle retourne les informations concernant un auteur (nombres de publications, nombre de co-auteurs).

     2) /authors/{name}/publications
Avec name le nom d'un auteur, elle liste les publications d'un auteur.

     3) /authors/{name}/coauthors
Avec name le nom d'un auteur, elle liste les co-auteurs d'un auteur.

     4) /authors/{name}/synthesis : 
Avec name le nom d'un auteur, elle retourne le nom d'un auteur, 
-Un tableau pour les conf�rences avec leurs ann�es d'apparition et leurs classement CORE
-Un tableau pour les journaux avec leurs ann�es d'apparition et leurs classement CORE 

**Toutes les routes on le m�me format d'erreur :
         Error: 404 Not Found


Les liens d'acc�s :
=================

     1) localhost:8080/authors/{name}
     2) localhost:8080/authors/{name}/publications
     3) localhost:8080/authors/{name}/coauthors
     4) localhost:8080/authors/{name}/synthesis

**name 
Le name s'ecrit : 
le nom avec la premiere lettre en majucule apres espace " " ou deux point ":" 
ensuite ecrire le prenom avec la premiere lettre en majuscule.
     


***********************************************************************************************
R�aliser par :
==============
   -BOUKERRAS Hanny
   -DJENKI Nabil 