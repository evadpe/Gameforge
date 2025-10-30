# Gameforge# 🎮 Gameforge

> **Générateur de concepts de jeux vidéo alimenté par l'IA**

Gameforge est une plateforme web innovante qui utilise l'intelligence artificielle (Mistral AI) pour générer automatiquement des concepts complets de jeux vidéo, incluant l'univers, le scénario, les personnages, les lieux et même des concept arts.

![Django](https://img.shields.io/badge/Django-5.2.7-092E20?logo=django)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-Powered-FF6B35)

---

## ✨ Fonctionnalités

### 🤖 Génération IA Complète
- **Titre du jeu** : Génération créative basée sur le genre et l'ambiance
- **Univers** : Description détaillée avec style graphique et type de monde
- **Scénario en 3 actes** : Structure narrative complète avec twist optionnel
- **Personnages** : 3 personnages détaillés avec background et gameplay
- **Lieux emblématiques** : 4 locations uniques avec descriptions
- **Concept Arts** : Génération d'images via Mistral AI (bêta)

### 👤 Gestion Utilisateur
- Système d'authentification (inscription/connexion)
- Tableau de bord personnel
- Limite de générations quotidiennes personnalisable (5 par défaut)
- Gestion de jeux publics/privés

### ❤️ Fonctionnalités Sociales
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
- (Optionnel) Virtualenv

### 1. Cloner le dépôt

```bash
git clone https://github.com/evadpe/Gameforge.git
cd Gameforge/Gameforge
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
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

## 🔑 Configuration Avancée

### Variables d'environnement

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `MISTRAL_API_KEY` | Clé API Mistral AI pour génération de texte et images | ✅ Oui |
| `HUGGINGFACE_API_KEY` | (Déprécié) Anciennement utilisé pour les images | ❌ Non |
| `DEBUG` | Mode debug Django | ❌ Non (True par défaut) |
| `SECRET_KEY` | Clé secrète Django | ⚠️ À changer en production |

### Personnalisation des limites

Dans l'admin Django (`/admin`), vous pouvez :
- Modifier la limite quotidienne pour un utilisateur spécifique
- Réinitialiser manuellement les compteurs
- Voir l'historique des générations

### Choix des modèles IA

Dans `ai_service.py`, vous pouvez modifier :
- `self.model = "mistral-small-latest"` → Modèle de génération de texte
- `model="mistral-medium-latest"` → Modèle de l'agent d'images

Modèles disponibles :
- `mistral-small-latest` (rapide, économique)
- `mistral-medium-latest` (équilibré)
- `mistral-large-latest` (plus puissant, plus coûteux)

---

## 🛠️ Technologies Utilisées

### Backend
- **Django 5.2.7** : Framework web Python
- **SQLite** : Base de données (configurable pour PostgreSQL/MySQL)
- **Mistral AI SDK** : Génération de texte et images
- **python-dotenv** : Gestion des variables d'environnement

### Frontend
- **HTML5/CSS3** : Templates Django
- **Bootstrap** (présumé) : Framework CSS
- **Django Template Language** : Moteur de templates

### IA & Machine Learning
- **Mistral AI** : Modèles LLM pour génération de contenu
- **Mistral Agents** : Génération d'images (fonctionnalité bêta)

---

## 🎯 Roadmap

### En cours
- [ ] Amélioration de la génération d'images
- [ ] Export des projets en PDF/JSON
- [ ] Système de commentaires

### Futur
- [ ] Partage sur les réseaux sociaux
- [ ] Génération de musique d'ambiance (Mistral Audio)
- [ ] Mode collaboratif multi-utilisateurs
- [ ] API REST pour intégrations tierces
- [ ] Support multilingue (actuellement en français)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Guidelines
- Respectez les conventions PEP 8 pour Python
- Ajoutez des tests unitaires pour les nouvelles fonctionnalités
- Documentez le code avec des docstrings
- Mettez à jour le README si nécessaire

---

## 🐛 Problèmes Connus

- **Mode démo sans API** : Si aucune clé Mistral n'est fournie, l'app génère du contenu mock
- **Génération d'images** : Fonctionnalité en bêta, peut échouer (fallback sur texte uniquement)
- **Performance** : La première génération peut prendre 10-15 secondes

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Auteurs

- **evadpe** - *Créateur initial* - [GitHub](https://github.com/evadpe)

---

## 🙏 Remerciements

- [Mistral AI](https://mistral.ai/) pour leur API puissante
- La communauté Django pour le framework
- Tous les contributeurs du projet

---

## 📞 Support

Pour toute question ou problème :
- Ouvrez une [issue GitHub](https://github.com/evadpe/Gameforge/issues)
- Consultez la documentation Django : [docs.djangoproject.com](https://docs.djangoproject.com/)
- Documentation Mistral AI : [docs.mistral.ai](https://docs.mistral.ai/)

---

**Fait avec ❤️ et IA par evadpe**