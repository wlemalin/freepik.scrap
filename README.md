# Objectif

Ce projet vise à simplifier le processus d'entraînement d'un réseau de neurones convolutifs (CNN) sans nécessiter de compétences en programmation. L'objectif est de permettre aux utilisateurs d’entraîner un CNN en suivant quelques étapes simples, sans écrire une seule ligne de code.


## Étapes


1. **Recherche d'images** : Utilisation de Selenium pour scraper Google Images, charger la page et récupérer le HTML. Parsing du HTML avec BeautifulSoup (bs4) pour générer une liste contenant les liens des images ou les données en base 64.

2. **Sélection et suppression des images** : Affichage des liens des images scrappées à l'aide de Jinja. Les utilisateurs peuvent sélectionner et supprimer les images non pertinentes en utilisant JavaScript, créant ainsi un album qui sera enregistré sur le serveur, une image permettant de représenter l’album est aussi créée grâce à Pillow .

3. **Entraînement du modèle** Les noms des classes sont récupérés via JavaScript pour l'entraînement, les albums correspondants sont récupérés et on y applique de l’augmentation de données puis l'entraînement est réalisé en utilisant TensorFlow et Keras. Le modèle est ensuite enregistré sur le serveur.

4. **Téléchargement du modèle** La précision du modèle est affichée et les utilisateurs ont la possibilité de télécharger le modèle entraîné à l'aide de Flask.

## Structure du Projet

```
project
│   README.md
│   app.py
│   app2.py
│   requirements.txt
│
└───cnn
│   │   model_building.py
│   │
│  
└───utils
│   │   folder_creation.py
│   │   
│  
└───scraping
│   │   googple.py
│   │   freepik.py
│   │
│
└───templates
│   │   search_form.html
│   │   train_form.html
│   │   train_result.html
│   │   album_form.html
│   
└───static
│   │
│   └───css
│   │   │   search.css
│   │   │   train.css
│   │   │   album.css
│   │   │
│   │
│   └───js
│   │   │   search.js
│   │   │   train.js
│   │   │   album.js
│   │   │   
│   │
│   └───models
│   │    
│   └───font
│   │   Georgia.ttf    
│   │
│   └───images
│   	│   blank_class.png
│   	│   
│   	└───album
│   	│   
│   	└───tags
│
└───web


```

## Détails des principaux Packages

**Flask + Jinja **: Flask est un micro-framework web pour Python qui facilite la création d'applications web. Jinja est un moteur de template pour Python, utilisé avec Flask pour générer des pages HTML dynamiques. Ensemble, ils permettent de construire et de rendre dynamique l'interface utilisateur de l'application.

**TensorFlow + Keras **: TensorFlow est une bibliothèque open-source pour le calcul numérique, qui permet la construction et l'entraînement de réseaux de neurones pour la détection et la décryption de patterns dans les données. Keras est une interface pour TensorFlow qui simplifie la création de modèles de deep learning avec une approche plus intuitive.

**BeautifulSoup **: Une bibliothèque qui permet de parser des documents HTML. Elle est utilisée pour le web scraping, permettant d'extraire facilement les données nécessaires à partir de pages web.

**Selenium **: Un package pour l'automatisation des navigateurs web. Il permet d'effectuer des actions dans le navigateur, comme si c'était un utilisateur réel qui les effectuait. Dans le contexte de ce projet, Selenium est utilisé pour simuler la navigation sur Google Images et récupérer le contenu nécessaire pour le scraping.

**Pillow + Base64 **: Pillow est une bibliothèque de traitement d'images pour Python, permettant d'ouvrir, de manipuler et de sauvegarder de nombreux formats d'images différents. Base64 est un schéma d'encodage qui permet de convertir des données binaires en chaînes de caractères ASCII, utilisées dans ce projet pour gérer les images encodées en base64 obtenues lors du scraping. Ensemble, ces outils facilitent le travail avec les images récupérées, leur prétraitement avant l'entraînement des modèles et leur affichage dans l'interface web.


## Installation

Pour exécuter ce projet localement, suivez ces étapes :

1. Pull ce dépôt sur votre machine.
2. Installez les dépendances en exécutant :

pip install -r requirements.txt

3. Lancez l'application Flask :

python app2.py

**Note:** Assurez vous d’avoir une version de Tensorflow compatible avec vôtre machine.
