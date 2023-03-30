# Exemple of test to get news 

Ce scraper utilise Scrapy pour extraire des articles de BBC News et les stocker dans un bucket Google Cloud Storage et dans une base de données PostgreSQL sur Google Cloud SQL.

## Configuration

### Environnement
Assurez-vous d'avoir une installation fonctionnelle de Python 3 et pip.
Activez un environnement virtuel ou directment en local, installez les dépendances avec ```pip install -r requirements.txt```

### Clé d'API Google Cloud Platform
La base de données PostgreSQL est déjà créée sur GCP, pour utiliser ce scraper, vous devez d'abord configurer la clé google credential en format json. 
Pour cela, il fallait demander au owner du projet.
Ensuite configurez les variables d'environnement suivantes dans votre terminal ou votre environnement :
GOOGLE_APPLICATION_CREDENTIALS: avec le chemin vers le fichier de la clé d'API JSON téléchargé précédemment

## Exécution du scraper
Dans votre terminal, exécutez la commande ```scrapy crawl movies``` pour démarrer le scraper. Les articles de BBC News seront extraits et stockés dans un csv en local et upload vers la base de données.
La base de données sur GCP est déjà connectée à BigQuery, ce qui vous permet d'effectuer des requêtes directement dans BigQuery, à condition que vous avez un compte GCP et les autorisations nécessaires pour accéder au projet.

