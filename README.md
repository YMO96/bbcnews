# Exemple of test to get news 

Ce scraper utilise Scrapy pour extraire des articles de BBC News et les stocker dans un bucket Google Cloud Storage et dans une base de données PostgreSQL sur Google Cloud SQL.

## Configuration

### Environnement
Assurez-vous d'avoir une installation fonctionnelle de Python 3 et pip. 

### Clé d'API Google Cloud Platform
La base de données PostgreSQL est déjà créée sur GCP, pour utiliser ce scraper, vous devez d'abord configurer la clé google credential en format json. 
Pour cela, demander
