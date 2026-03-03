<div align="center">

<img src="https://www.simplon.ma/images/Simplon_Maghreb_Rouge.png" alt="Simplon Maghreb Logo" width="280"/>

<br/><br/>

<h1>⚡ HR-Pulse</h1>
<h3>Pipeline IA de Recrutement Intelligente</h3>

<p><em>Data Engineering · Azure AI NER · Prédiction Salariale · Microservices · Observabilité Distribuée</em></p>

<br/>

![Next.js](https://img.shields.io/badge/-Next.js%2015-black?style=for-the-badge&logo=nextdotjs&logoColor=white&color=000000)
![FastAPI](https://img.shields.io/badge/-FastAPI-black?style=for-the-badge&logo=fastapi&logoColor=white&color=009688)
![Azure AI](https://img.shields.io/badge/-Azure%20AI-black?style=for-the-badge&logo=microsoftazure&logoColor=white&color=0089D6)
![Docker](https://img.shields.io/badge/-Docker-black?style=for-the-badge&logo=docker&logoColor=white&color=2496ED)
![Terraform](https://img.shields.io/badge/-Terraform-black?style=for-the-badge&logo=terraform&logoColor=white&color=7B42BC)
![Jaeger](https://img.shields.io/badge/-Jaeger-black?style=for-the-badge&logo=jaeger&logoColor=white&color=60D051)
![Python](https://img.shields.io/badge/-Python%203.12-black?style=for-the-badge&logo=python&logoColor=white&color=3776AB)

<br/><br/>

</div>

---

## 📋 Table des Matières

- [Introduction](#-introduction)
- [Architecture](#-architecture)
- [Fonctionnalités](#-fonctionnalités)
- [API Reference](#-api-reference)
- [Stack Technologique](#-stack-technologique)
- [Démarrage Rapide](#-démarrage-rapide)
- [Structure du Projet](#-structure-du-projet)
- [CI/CD](#-cicd)

---

## 🚀 Introduction

**HR-Pulse** est une solution de **Data Engineering et d'IA** conçue pour moderniser le processus de recrutement. Son objectif : transformer une masse de données textuelles brutes (offres d'emploi) en une base de connaissances structurée et exploitable.

Le pipeline ingère un fichier `jobs.csv`, extrait automatiquement les compétences clés via **Azure AI Language (NER)**, prédit les fourchettes salariales grâce à un modèle de régression, et expose l'ensemble via une API FastAPI consommée par une interface Next.js.

> **Projet Jury Blanc** · Simplon Maghreb · Février 2026

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP
┌───────────────────────────▼─────────────────────────────────────┐
│                  FRONTEND — Next.js 15                          │
│              Tailwind CSS · Lucide React                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API
┌───────────────────────────▼─────────────────────────────────────┐
│                  BACKEND — FastAPI                              │
│         SQLAlchemy · OpenTelemetry SDK · Pydantic               │
│                                                                 │
│    ┌──────────────┐   ┌─────────────────┐   ┌──────────────┐   │
│    │  NER Extract │   │ Salary Predictor│   │  Jobs CRUD   │   │
│    └──────┬───────┘   └────────┬────────┘   └──────┬───────┘   │
└───────────┼────────────────────┼────────────────────┼──────────┘
            │                    │                    │
┌───────────▼────────────────────▼────────────────────▼──────────┐
│                        AZURE CLOUD                              │
│      Azure AI Language (NER)   ·   Azure SQL Database          │
└─────────────────────────────────────────────────────────────────┘
                            │ OTLP
┌───────────────────────────▼─────────────────────────────────────┐
│                    JAEGER — Distributed Tracing                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Fonctionnalités

### 🧠 Data Engineering & IA

| Fonctionnalité | Description |
|---|---|
| **Ingestion & Nettoyage** | Traitement du fichier `jobs.csv` : normalisation des titres de poste et nettoyage des données brutes |
| **Extraction de compétences (NER)** | Connexion à Azure AI Language pour identifier automatiquement les compétences clés dans chaque description de poste |
| **Prédiction Salariale** | Modèle de régression ML qui convertit une fourchette brute (ex. `$137K-$171K`) en valeur numérique moyenne prédite |
| **Persistance Azure SQL** | Stockage structuré des offres avec `id`, `job_title`, et `skills_extracted` au format JSON |

### ⚙️ DevOps & Infrastructure

- **CI/CD** : Pipeline GitHub Actions — Linting (Ruff), Tests (Pytest), puis Build des images Docker
- **Conteneurisation** : Images Docker multi-stage optimisées pour le Frontend et le Backend
- **Infrastructure as Code** : Provisionnement d'Azure SQL et Azure AI Language via Terraform, avec backend distant (`azurerm`) pour la gestion du `.tfstate`
- **Gestion des secrets** : Variables d'environnement isolées via `.env`, ignorées par Git

### 👁️ Observabilité (Jaeger)

- **Tracing distribué** : Suivi d'une requête du clic client jusqu'à la réponse base de données
- **Monitoring IA** : Mesure du temps de réponse des appels Azure AI Language
- **Latence SQL** : Mesure des temps de requête Azure SQL
- **Visualisation des erreurs** : Détection des erreurs HTTP 500 directement dans l'interface Jaeger UI

---

## 📡 API Reference

| Endpoint | Méthode | Description |
|---|---|---|
| `/jobs` | `GET` | Liste des offres d'emploi depuis Azure SQL |
| `/jobs/search` | `GET` | Recherche d'offres par compétences |
| `/predict-salary` | `POST` | Inférence ML pour estimation salariale |
| `/docs` | `GET` | Documentation Swagger UI interactive |

> La documentation Swagger complète est accessible sur `http://localhost:8000/docs` après démarrage.

---

## 🛠️ Stack Technologique

| Couche | Technologies |
|---|---|
| **Frontend** | Next.js 15, Tailwind CSS, Lucide React |
| **Backend** | FastAPI, SQLAlchemy, Pydantic, Python 3.12, `uv` |
| **IA / ML** | Azure AI Language (NER), Scikit-learn (Régression) |
| **Cloud** | Azure SQL Database (Serverless), Azure AI Language |
| **Infra** | Terraform (Remote Backend azurerm), Docker, Docker Compose |
| **Observabilité** | Jaeger, OpenTelemetry SDK, OTLP Exporter |
| **Qualité** | Pytest, Ruff, GitHub Actions |

> ⚠️ Ce projet utilise **`uv`** comme gestionnaire de paquets Python en remplacement de `pip`.

---

## ⚡ Démarrage Rapide

### Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et en cours d'exécution
- [uv](https://github.com/astral-sh/uv) installé
- Un fichier `infra/.env` configuré avec vos secrets Azure

### Variables d'environnement

Créez le fichier `infra/.env` :

```env
DATABASE_URL=mssql+pyodbc://<username>:<password>@<server>.database.windows.net/<database>?driver=ODBC+Driver+18+for+SQL+Server
AZURE_AI_KEY=your_azure_ai_key
AZURE_AI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
```

### 1. Provisionner l'infrastructure Azure

```bash
cd infra/
terraform init
terraform apply
```

### 2. Lancer toute la stack

```bash
docker-compose up --build -d
```

Cela démarre automatiquement les trois services : **Frontend**, **Backend**, et **Jaeger**.

### 3. Initialiser et injecter les données

> À effectuer uniquement lors du **premier lancement**.

```bash
docker exec -it hr_pulse_backend python update_db.py
```

### 4. Accéder aux interfaces

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API Backend | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Jaeger UI | http://localhost:16686 |

---

## 📁 Structure du Projet

```
hr-pulse/
│
├── backend/                  # API FastAPI (Python 3.12)
│   ├── routers/              # Endpoints organisés par domaine
│   ├── services/             # Logique métier & appels Azure AI
│   │   ├── ner_service.py    # Extraction NER via Azure AI Language
│   │   └── salary_model.py   # Modèle de régression salariale
│   ├── models/               # Modèles SQLAlchemy
│   ├── tests/                # Tests unitaires & d'intégration (Pytest)
│   ├── update_db.py          # Script d'ingestion et d'initialisation
│   └── Dockerfile            # Image Backend multi-stage
│
├── frontend/                 # Interface Next.js (Node 20)
│   ├── app/                  # App Router Next.js 15
│   ├── components/           # Composants React réutilisables
│   └── Dockerfile            # Image Frontend multi-stage
│
├── infra/                    # Infrastructure as Code
│   ├── main.tf               # Ressources Terraform (Azure SQL + Azure AI)
│   ├── variables.tf          # Déclaration des variables
│   └── .env                  # Secrets locaux (ignoré par Git)
│
├── data/
│   └── jobs.csv              # Dataset source des offres d'emploi
│
├── .github/
│   └── workflows/            # Pipelines CI/CD GitHub Actions
│
└── docker-compose.yml        # Orchestration complète de la stack
```

---

## 🔄 CI/CD

Le pipeline GitHub Actions se déclenche automatiquement à chaque push :

```
Push → Lint (Ruff) → Tests (Pytest) → Build Docker Images
```

**Job 1 — Linting (Ruff)** : Vérifie la conformité du code Python. La pipeline échoue si les standards ne sont pas respectés.

**Job 2 — Tests (Pytest)** : Exécute les tests unitaires et d'intégration.

**Job 3 — Build Docker** : Construit les images Frontend et Backend pour valider l'absence d'erreurs de dépendances.

---

<div align="center">

<br/>

Développé avec ❤️ par **OclaZ**


<br/>

</div>
