# Project_LITReview

**Description** 

Ce projet consiste à crer une application web permettant de partager des avis et des critiques sur des livres.

**Prérequis**

Il est nécessaire d'avoir Python 3.7 et Git installé sur le PC.

**Installation**

1. Dans la console Git, choissisez l'emplacement où vous voulez cloner le projet
2. Exécuter  ``` git clone https://github.com/jaikko/Project_LITReview.git ```
3. Ensuite, se rendre dans le projet avec ``` cd Project_LITReview ```
4. Installer l'environnement virtuel en éxécutant ``` virtualenv -p python3 venv ```
5. Activer le avec la commande   ``` source venv/Scripts/activate ```
6. Installer les modules avec  ```pip install -r requirements.txt ```
7. Lancez le serveur avec la commande ```python manage.py runserver```
8. Se rendre à l'adresse suivante http://127.0.0.1:8000/ pour accéder au site 

**Utilisation**

Une fois que vous êtes sur la page d'accueil, vous pouvez vous connectez. Si vous n'êtes pas enregistré, 
cliquez sur le bouton "s'incrire". 

Dès que vous êtes connectés, vous accéder à vos flux. Sur cette page, il est possible de répondre à un ticket, 
créer un ticket et créer une critique. On peut avoir accès aux autres pages:

- "Post" qui permet de voir, modifier ou supprimer nos avis et ticket
- "Abonnement" qui a pour but de suivre des personnes et voir les personnnes qui nous suivent
- "Flux" qui affiche vos flux
- "Se déconnecter" pour se déconnecter du site
