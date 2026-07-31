# JobMatch AI

Application permettant d'analyser un profil candidat et de recommander des offres d'alternance pertinentes.

## Objectif

La recherche d'une alternance demande beaucoup de temps : consultation des offres, comparaison des compétences demandées et suivi des candidatures.

JobMatch AI aura pour objectif de :

- centraliser des offres d'alternance ;
- analyser les compétences présentes dans un CV ;
- comparer un profil candidat avec les offres disponibles ;
- calculer un score de compatibilité ;
- expliquer les compétences présentes et manquantes ;
- suivre l'avancement des candidatures.

## Fonctionnalités prévues

- Import d'offres depuis un fichier CSV
- Nettoyage et validation des données
- Stockage des offres dans PostgreSQL
- Création d'une API avec FastAPI
- Recherche et filtrage des offres
- Analyse d'un CV
- Recommandation d'offres avec du machine learning
- Interface utilisateur
- Tests automatisés
- Conteneurisation avec Docker
- Pipeline CI/CD avec GitHub Actions
- Déploiement de l'application

## Technologies prévues

- Python
- Pandas
- FastAPI
- PostgreSQL
- SQLAlchemy
- scikit-learn
- Streamlit
- pytest
- Docker
- GitHub Actions

## Architecture prévue

```text
Données des offres
        ↓
Pipeline Python
        ↓
Nettoyage et validation
        ↓
Base de données PostgreSQL
        ↓
Moteur de recommandation
        ↓
API FastAPI
        ↓
Interface Streamlit
