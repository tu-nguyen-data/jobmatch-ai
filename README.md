# JobMatch AI

[![CI](https://github.com/tu-nguyen-data/jobmatch-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/tu-nguyen-data/jobmatch-ai/actions/workflows/ci.yml)

Application de recommandation d'offres d'alternance basée sur Python, FastAPI, PostgreSQL et le NLP.

JobMatch AI permet d'importer des offres, de les stocker dans PostgreSQL et de les classer selon leur pertinence par rapport au profil d'un candidat grâce à un moteur de matching basé sur TF-IDF et la similarité cosinus.

> 🚧 Projet en cours de développement — version actuelle : Matching v1

## Fonctionnalités

- Création, consultation, modification et suppression d'offres via une API REST
- Stockage des offres dans PostgreSQL avec SQLAlchemy
- Import d'offres depuis un fichier CSV avec Pandas
- Validation des données avec Pydantic
- Détection des doublons lors de l'import
- Matching candidat ↔ offres avec TF-IDF et similarité cosinus
- Classement automatique des offres par score de pertinence
- Tests automatisés avec Pytest
- Intégration continue avec GitHub Actions
- Conteneurisation avec Docker et Docker Compose

## Architecture

```text
jobmatch-ai/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   └── services/
├── data/
│   └── offers_sample.csv
├── scripts/
│   └── import_offers.py
├── tests/
├── .github/
│   └── workflows/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### Flux principal

```text
Profil candidat
      ↓
POST /match
      ↓
FastAPI
      ↓
PostgreSQL → récupération des offres
      ↓
TF-IDF + similarité cosinus
      ↓
Score de pertinence
      ↓
Classement des offres
```

## Objectif

La recherche d'une alternance demande beaucoup de temps : consultation des offres, comparaison des compétences demandées et suivi des candidatures.

JobMatch AI vise à :

- centraliser des offres d'alternance ;
- analyser le profil d'un candidat ;
- comparer ce profil avec les offres disponibles ;
- calculer un score de pertinence ;
- recommander les offres les plus adaptées.

## Technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pandas
- Pydantic
- scikit-learn
- Pytest
- Docker
- Docker Compose
- GitHub Actions

## Tests

Le projet contient des tests automatisés pour :

- la validation des données ;
- les endpoints de l'API ;
- les opérations CRUD ;
- le moteur de matching.

Les tests sont exécutés automatiquement avec GitHub Actions à chaque push.

## Roadmap

- [x] API REST avec FastAPI
- [x] Base de données PostgreSQL
- [x] Import CSV avec Pandas
- [x] Tests automatisés
- [x] CI avec GitHub Actions
- [x] Docker et Docker Compose
- [x] Matching v1 avec TF-IDF et similarité cosinus
- [ ] Matching sémantique avec embeddings
- [ ] Analyse de CV
- [ ] Interface utilisateur avec Streamlit
- [ ] Déploiement en ligne