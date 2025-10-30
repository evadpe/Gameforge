# Gameforge# 🎮 Gameforge

> **Générateur de concepts de jeux vidéo alimenté par l'IA**

Gameforge est une plateforme web innovante qui utilise l'intelligence artificielle (Mistral AI et Hugging Face) pour générer automatiquement des concepts complets de jeux vidéo, incluant l'univers, le scénario, les personnages, les lieux et même des concept arts.

![Django](https://img.shields.io/badge/Django-5.2.7-092E20?logo=django)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-Powered-FF6B35)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-Powered-FFD21E?logo=huggingface&logoColor=white)

---

## Fonctionnalités

### Génération IA Complète
- **Titre du jeu** : Génération créative basée sur le genre et l'ambiance
- **Univers** : Description détaillée avec style graphique et type de monde
- **Scénario en 3 actes** : Structure narrative complète avec twist optionnel
- **Personnages** : 3 personnages détaillés avec background et gameplay
- **Lieux emblématiques** : 4 locations uniques avec descriptions
- **Concept Arts** : Génération d'images via Mistral AI (bêta)

### Gestion Utilisateur
- Système d'authentification (inscription/connexion)
- Tableau de bord personnel
- Limite de générations quotidiennes personnalisable (5 par défaut)
- Gestion de jeux publics/privés

### Fonctionnalités Sociales
- Système de favoris/likes
- Exploration des créations de la communauté
- Recherche par titre, genre ou mots-clés
- Partage de créations publiques

---

## 🏗️ Architecture

Le projet suit une architecture Django MVC classique :

```
Gameforge/
├── gameforge_project/          # Configuration Django principale
│   ├── settings.py            # Configuration (API keys, DB, etc.)
│   ├── urls.py                # Routage principal
│   └── wsgi.py                # Point d'entrée WSGI
│
├── games/                      # Application principale
│   ├── models.py              # 8 modèles de données
│   ├── views.py               # Logique métier
│   ├── forms.py               # Formulaires Django
│   ├── ai_service.py          # Service d'intégration Mistral AI
│   ├── urls.py                # Routes de l'app
│   ├── templates/games/       # Templates HTML
│   └── migrations/            # Migrations de base de données
│
├── manage.py                   # CLI Django
└── requirements.txt            # Dépendances Python
```

### 📊 Modèles de Données

| Modèle | Description |
|--------|-------------|
| `Game` | Jeu principal avec métadonnées (titre, genre, ambiance) |
| `Universe` | Univers du jeu (description, style graphique, type de monde) |
| `Scenario` | Scénario en 3 actes avec twist |
| `Character` | Personnages avec classe, rôle et background |
| `Location` | Lieux emblématiques |
| `ConceptArt` | Images générées par l'IA |
| `Favorite` | Système de likes/favoris |
| `GenerationLimit` | Gestion des limites quotidiennes par utilisateur |

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- pip

### 1. Cloner le dépôt

```bash
git clone https://github.com/evadpe/Gameforge.git
cd Gameforge/Gameforge
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate 

# Sur Windows: 
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les principales dépendances sont :
- Django 5.2.7
- mistralai (SDK officiel)
- python-dotenv (gestion des variables d'environnement)
- Pillow (traitement d'images)

### 4. Configuration

Créez un fichier `.env` à la racine du dossier `Gameforge/` :

```env
MISTRAL_API_KEY=votre_cle_api_mistral
```

> **Note** : Obtenez votre clé API sur [console.mistral.ai](https://console.mistral.ai/)

### 5. Migrations de base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. (Optionnel) Créer un super-utilisateur

```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible sur `http://127.0.0.1:8000/`

---

## 📖 Utilisation

### Première connexion

1. Créez un compte via `/register`
2. Connectez-vous via `/login`
3. Accédez à votre tableau de bord `/dashboard`

### Créer un jeu

#### Méthode 1 : Génération guidée

1. Cliquez sur "Créer un nouveau jeu"
2. Sélectionnez un **genre** (RPG, Action, Aventure, etc.)
3. Choisissez une **ambiance** (Sombre, Joyeux, Mystérieux, etc.)
4. Ajoutez des **mots-clés** (séparés par des virgules)
5. (Optionnel) Ajoutez des **références culturelles**
6. Choisissez la visibilité (Public/Privé)
7. Cliquez sur "Générer"

#### Méthode 2 : Génération aléatoire

1. Cliquez sur "Surprise-moi !" dans le dashboard
2. Le système génère un jeu complètement aléatoire

### Explorer les créations

- **Page d'accueil** : Découvrez tous les jeux publics
- **Barre de recherche** : Recherchez par titre, genre ou mots-clés
- **Favoris** : Accédez à vos jeux préférés via `/favorites`

### Limites de génération

- Par défaut : **5 générations par jour**
- Le compteur se réinitialise automatiquement à minuit
- Les superutilisateurs peuvent modifier les limites via l'admin Django


---

## 🛠️ Technologies Utilisées

- **Django** 
- **SQLite** 
- **python-dotenv** 
- **HTML5/CSS3** 
- **Mistral AI** 
- **Hugging Face** 

---

## 👥 Auteurs

- **Eva Depaepe** 
- **Mathis Ponsson**
- **Romain Roche**
- **Emilie Delrue**

[GitHub](https://github.com/evadpe)

---
