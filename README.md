# 🎮 Gameforge
 
> **Générateur de concepts de jeux vidéo alimenté par l'IA**
 
Gameforge est une plateforme web innovante qui utilise l'intelligence artificielle (Mistral AI pour le texte, FLUX.1-schnell pour les images) pour générer automatiquement des concepts complets de jeux vidéo, incluant l'univers, le scénario, les personnages, les lieux et même des concept arts.
 
![Django](https://img.shields.io/badge/Django-5.2.7-092E20?logo=django)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-Powered-FF6B35)
![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-FLUX.1--schnell-FFD21E)
 
---
 
## Table des matières
 
- [Présentation du projet](#-présentation-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture & Flux de données](#️-architecture--flux-de-données)
- [Modèles de données](#-modèles-de-données)
- [Installation](#-installation)
- [Technologies utilisées](#️-technologies-utilisées)
- [Screenshots](#-screenshots)
- [Bonus implémentés](#-bonus-implémentés)
- [Tests & Expérimentations](#-tests--expérimentations)
- [Limites & Améliorations futures](#-limites--améliorations-futures)
- [Équipe](#-équipe)
 
---
 
## Présentation du projet
 
### Contexte
 
Gameforge est né d'une volonté de démocratiser la création de concepts de jeux vidéo en utilisant l'intelligence artificielle. L'objectif est de permettre à n'importe qui (game designers, développeurs indépendants, passionnés) de générer rapidement des idées de jeux complètes et cohérentes.
 
### Objectifs
 
- Générer automatiquement des concepts de jeux vidéo complets
- Utiliser plusieurs modèles d'IA (Mistral AI pour le texte, tentatives avec Hugging Face)
- Créer une interface web intuitive et responsive
- Gérer une communauté d'utilisateurs avec système de favoris
- Limiter les abus avec un système de quotas quotidiens
 
### Fonctionnement général
 
1. L'utilisateur choisit des paramètres (genre, ambiance, mots-clés)
2. Le backend appelle l'API Mistral AI via le service `ai_service.py`
3. L'IA génère séquentiellement :
   - Un titre accrocheur
   - Un univers détaillé
   - Un scénario en 3 actes
   - 3 personnages principaux
   - 4 lieux emblématiques
   - (Optionnel) Une image de concept art
4. Les données sont sauvegardées dans la base de données SQLite
5. L'utilisateur peut consulter, partager et liker les créations
 
---
 
## Fonctionnalités
 
### Génération IA Complète
 
- **Titre du jeu** : Génération créative basée sur le genre et l'ambiance
- **Univers** : Description détaillée avec style graphique (réaliste, cartoon, pixel art, anime, low poly) et type de monde (open world, linéaire, hub, arène)
- **Scénario en 3 actes** : Structure narrative complète (introduction, développement, climax) avec twist optionnel
- **Personnages** : 3 personnages détaillés avec :
  - Nom et classe (guerrier, mage, voleur, archer, healer, tank, support)
  - Rôle (héros, antagoniste, allié, mentor, neutre)
  - Background complet
  - Description du gameplay
- **Lieux emblématiques** : 4 locations uniques avec descriptions immersives
- **Concept Arts** : Génération d'images via Mistral AI (fonctionnalité bêta)
 
### Gestion Utilisateur
 
- Système d'authentification complet (inscription/connexion/déconnexion)
- Tableau de bord personnel avec vue sur ses créations
- Limite de générations quotidiennes personnalisable (5 par défaut)
- Gestion de la visibilité (jeux publics/privés)
- Interface d'administration Django pour les superutilisateurs
 
### Fonctionnalités Sociales
 
- Système de favoris/likes avec compteur
- Exploration des créations de la communauté
- Recherche avancée par titre, genre ou mots-clés
- Page dédiée aux favoris
- Partage de créations publiques
 
### Génération Aléatoire
 
- Bouton "Génération Aléatoire" pour générer un jeu avec paramètres aléatoires
- Permet de découvrir des combinaisons inattendues
- **Code** : Fonction `create_random_game()` dans `views.py` + `generate_random_game_params()` dans `ai_service.py`
 
---
 
## Architecture & Flux de données
 
### Structure du projet
 
```
Gameforge/
├── gameforge_project/          # Configuration Django principale
│   ├── settings.py            # Configuration (API keys, DB, middlewares)
│   ├── urls.py                # Routage principal
│   ├── wsgi.py                # Point d'entrée WSGI
│   └── asgi.py                # Point d'entrée ASGI
│
├── games/                      # Application principale
│   ├── models.py              # 8 modèles de données
│   ├── views.py               # 11 vues (home, register, login, dashboard, etc.)
│   ├── forms.py               # Formulaire de création de jeu
│   ├── ai_service.py          # Service d'intégration Mistral AI (554 lignes)
│   ├── urls.py                # Routes de l'application games
│   ├── admin.py               # Configuration interface admin
│   ├── apps.py                # Configuration de l'app
│   ├── templates/games/       # 9 templates HTML
│   │   ├── base.html          # Template de base
│   │   ├── home.html          # Page d'accueil
│   │   ├── register.html      # Inscription
│   │   ├── login.html         # Connexion
│   │   ├── dashboard.html     # Tableau de bord
│   │   ├── create_game.html   # Formulaire de création
│   │   ├── game_detail.html   # Détails d'un jeu
│   │   ├── favorites.html     # Page des favoris
│   │   └── confirm_delete.html # Confirmation de suppression
│   └── migrations/            # Migrations de base de données
│       ├── 0001_initial.py
│       ├── 0002_alter_generationlimit_max_daily.py
│       └── 0003_remove_generationlimit_max_daily_and_more.py
│
├── media/                      # Dossier pour les concept arts générés
│   └── concept_arts/
│
├── manage.py                   # CLI Django
├── requirements.txt            # Dépendances Python
└── .env                        # Variables d'environnement (non versionné)
```
 
### Schéma du flux de données
 
```
┌─────────────────────────────────────────────────────────────────┐
│                        UTILISATEUR                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   INTERFACE WEB (Templates HTML)                 │
│  • Formulaire de création (genre, ambiance, mots-clés)          │
│  • Bouton "Surprise-moi !"                                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VIEWS.PY (Logique métier)                     │
│  • create_game() : Validation du formulaire                      │
│  • create_random_game() : Paramètres aléatoires                  │
│  • Vérification des limites quotidiennes                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               AI_SERVICE.PY (Service d'IA)                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1. generate_game_title(genre, ambiance, keywords)       │    │
│  │    → Génère le titre du jeu                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 2. generate_universe(titre, genre, ambiance)            │    │
│  │    → Génère description, style graphique, type monde    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 3. generate_scenario(titre, universe, genre)            │    │
│  │    → Génère les 3 actes + twist                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 4. generate_characters(titre, genre, count=3)           │    │
│  │    → Génère 3 personnages avec backgrounds              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 5. generate_locations(titre, universe, count=4)         │    │
│  │    → Génère 4 lieux emblématiques                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 6. generate_and_save_image(titre, genre, ambiance)      │    │
│  │    → Génère une image de concept art (optionnel)        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│  Chaque appel contacte : MISTRAL AI API                         │
│  (mistral-small-latest pour texte, mistral-medium pour images)  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MODELS.PY (Base de données)                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Game (titre, genre, ambiance, mots_cles, createur)      │    │
│  │   ↓                                                      │    │
│  │ Universe (description, style_graphique, type_monde)     │    │
│  │   ↓                                                      │    │
│  │ Scenario (acte_1, acte_2, acte_3, twist)                │    │
│  │   ↓                                                      │    │
│  │ Character × 3 (nom, classe, role, background)           │    │
│  │   ↓                                                      │    │
│  │ Location × 4 (nom, description)                         │    │
│  │   ↓                                                      │    │
│  │ ConceptArt (image, description, type_art)               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  + Favorite (user ↔ game) pour les likes                        │
│  + GenerationLimit (compteur quotidien par user)                │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SQLite Database (db.sqlite3)                  │
│  Stockage persistant de toutes les données                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              AFFICHAGE FINAL (game_detail.html)                  │
│  • Titre et métadonnées                                          │
│  • Description de l'univers                                      │
│  • Scénario complet                                              │
│  • Liste des personnages                                         │
│  • Liste des lieux                                               │
│  • Concept art (si généré)                                       │
│  • Bouton like/unlike                                            │
└─────────────────────────────────────────────────────────────────┘
```
 
### Flux détaillé d'une génération
 
1. **Requête utilisateur** → POST vers `/create-game/`
2. **Validation** → Vérification des limites quotidiennes (5/jour par défaut)
3. **Génération séquentielle** :
   ```python
   titre = ai_service.generate_game_title(...)          
   universe_data = ai_service.generate_universe(...)    
   scenario_data = ai_service.generate_scenario(...)    
   characters_data = ai_service.generate_characters(...)
   locations_data = ai_service.generate_locations(...)  
   image_result = ai_service.generate_and_save_image(...)
   ```
   **Temps total** : ~30-40 secondes avec image, ~20 secondes sans
4. **Sauvegarde** → Création des objets Django et relations en base
5. **Redirection** → Vers la page de détail du jeu créé
6. **Incrémentation** → Compteur de générations quotidiennes +1
 
---
 
## Modèles de données
 
### Diagramme de relations
 
```
┌─────────────────┐
│      User       │
│  (Django Auth)  │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────▼──────────────┐         ┌──────────────────┐
    │       Game        │◄────────│ GenerationLimit  │
    │                   │  1:1    │  (quotas)        │
    ├───────────────────┤         └──────────────────┘
    │ • titre           │
    │ • genre           │               1:1
    │ • ambiance        │         ┌──────▼───────────┐
    │ • mots_cles       │◄────────│    Universe      │
    │ • references      │         │                  │
    │ • est_public      │         │ • description    │
    │ • likes_count     │         │ • style_graphique│
    └───────┬───────────┘         │ • type_monde     │
            │                     └──────────────────┘
            │
            ├─────1:1────────►┌──────────────────┐
            │                 │    Scenario      │
            │                 │                  │
            │                 │ • acte_1         │
            │                 │ • acte_2         │
            │                 │ • acte_3         │
            │                 │ • twist          │
            │                 └──────────────────┘
            │
            ├─────1:N────────►┌──────────────────┐
            │                 │   Character      │
            │                 │                  │
            │                 │ • nom            │
            │                 │ • classe         │
            │                 │ • role           │
            │                 │ • background     │
            │                 │ • gameplay_desc  │
            │                 └──────────────────┘
            │
            ├─────1:N────────►┌──────────────────┐
            │                 │    Location      │
            │                 │                  │
            │                 │ • nom            │
            │                 │ • description    │
            │                 └──────────────────┘
            │
            ├─────1:N────────►┌──────────────────┐
            │                 │   ConceptArt     │
            │                 │                  │
            │                 │ • image          │
            │                 │ • description    │
            │                 │ • type_art       │
            │                 └──────────────────┘
            │
            └─────N:M────────►┌──────────────────┐
                 (via)        │    Favorite      │
                              │                  │
                              │ • user           │
                              │ • game           │
                              │ • date_added     │
                              └──────────────────┘
```
 
### Description des modèles
 
| Modèle | Type de relation | Champs principaux | Description |
|--------|------------------|-------------------|-------------|
| **Game** | Hub central | `titre`, `genre`, `ambiance`, `mots_cles`, `references`, `createur` (FK User), `est_public`, `likes_count` | Modèle principal représentant un jeu généré |
| **Universe** | OneToOne avec Game | `description`, `style_graphique`, `type_monde` | Décrit l'univers et l'esthétique du jeu |
| **Scenario** | OneToOne avec Game | `acte_1`, `acte_2`, `acte_3`, `twist` | Structure narrative en 3 actes + twist optionnel |
| **Character** | ForeignKey vers Game | `nom`, `classe`, `role`, `background`, `gameplay_description` | Personnages jouables ou PNJ importants (3 par jeu) |
| **Location** | ForeignKey vers Game | `nom`, `description` | Lieux emblématiques du jeu (4 par jeu) |
| **ConceptArt** | ForeignKey vers Game | `image` (ImageField), `description`, `type_art` | Images générées par l'IA (optionnel) |
| **Favorite** | ManyToMany User-Game | `user` (FK), `game` (FK), `date_added` | Système de likes/favoris |
| **GenerationLimit** | OneToOne avec User | `generations_today`, `daily_count`, `last_reset` | Gestion des quotas quotidiens (5 par défaut) |
 
### Choix de conception
 
- **OneToOne pour Universe et Scenario** : Un jeu ne peut avoir qu'un seul univers et scénario
- **ForeignKey pour Characters et Locations** : Permet d'avoir plusieurs éléments par jeu
- **ManyToMany pour Favorites** : Un user peut liker plusieurs jeux, un jeu peut être liké par plusieurs users
- **ImageField pour ConceptArt** : Utilise Pillow pour le stockage et la manipulation d'images
 
---
 
## Installation
 
### Prérequis
 
- **Python 3.10+** (développé avec Python 3.13)
- **pip** (gestionnaire de paquets Python)
- **Git** (pour cloner le dépôt)
 
### 1. Cloner le dépôt
 
```bash
git clone https://github.com/evadpe/Gameforge.git
cd Gameforge/Gameforge
```
 
### 2. Créer un environnement virtuel
 
**Sur macOS/Linux :**
```bash
python -m venv venv
# ou python3 -m venv venv
source venv/bin/activate
```
 
**Sur Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```
 
### 3. Installer les dépendances
 
```bash
pip install -r requirements.txt
```
 
**Dépendances installées :**
- `Django==5.2.7` - Framework web
- `mistralai>=1.0.0` - SDK Mistral AI
- `python-dotenv==1.0.0` - Gestion des variables d'environnement
- `Pillow>=10.0.0` - Traitement d'images
 
### 4. Configuration des variables d'environnement
 
Créez un fichier `.env` à la racine du dossier `Gameforge/` :
 
```env
# API Keys
MISTRAL_API_KEY=votre_cle_api_mistral_ici
HUGGINGFACE_API_KEY=votre_cle_api_huggingface_ici
 
# Django Settings (optionnel)
DEBUG=True
SECRET_KEY=votre_secret_key_django
```
 
> ** Obtenir une clé Mistral AI :**
> 1. Créez un compte sur [console.mistral.ai](https://console.mistral.ai/)
> 2. Allez dans "API Keys"
> 3. Créez une nouvelle clé
> 4. Copiez-la dans votre fichier `.env`
 
> ** Obtenir une clé Hugging Face :**
> 1. Créez un compte sur [huggingface.co](https://huggingface.co/join)
> 2. Allez dans Settings → Access Tokens
> 3. Créez un nouveau token (Read access suffit)
> 4. Copiez-le dans votre fichier `.env`
>
> **Note** : La clé Hugging Face est utilisée pour générer les concept arts avec FLUX.1-schnell
 
### 5. Créer la base de données
 
```bash
# Créer les migrations
python manage.py makemigrations
 
# Appliquer les migrations
python manage.py migrate
```
 
**Migrations appliquées :**
- `0001_initial.py` : Création des modèles initiaux
- `0002_alter_generationlimit_max_daily.py` : Modification du champ max_daily
- `0003_remove_generationlimit_max_daily_and_more.py` : Refactoring des limites
 
### 6. (Optionnel) Créer un super-utilisateur
 
Pour accéder à l'interface d'administration Django :
 
```bash
python manage.py createsuperuser
```
 
Renseignez :
- Username (ex: `admin`)
- Email (optionnel)
- Password (2 fois)
 
### 7. Lancer le serveur de développement
 
```bash
python manage.py runserver
```
 
L'application sera accessible sur **`http://127.0.0.1:8000/`**
 
**URLs importantes :**
- `/` - Page d'accueil
- `/register/` - Inscription
- `/login/` - Connexion
- `/dashboard/` - Tableau de bord
- `/create-game/` - Créer un jeu
- `/admin/` - Interface d'administration (nécessite un superuser)
 
 
 
## Technologies utilisées
 
### Backend
 
| Technologie | Version | Usage |
|-------------|---------|-------|
| **Python** | 3.13 | Langage principal |
| **Django** | 5.2.7 | Framework web MVC |
| **SQLite** | 3.x | Base de données (incluse avec Python) |
| **Mistral AI SDK** | 1.0+ | Génération de texte et images |
| **python-dotenv** | 1.0.0 | Gestion des variables d'environnement |
| **Pillow** | 10.0+ | Traitement d'images (ImageField) |
 
### Frontend
 
| Technologie | Usage |
|-------------|-------|
| **HTML5** | Structure des pages |
| **CSS3** | Stylisation |
| **Django Template Language** | Moteur de templates |
| **Bootstrap** (présumé) | Framework CSS responsive |
 
### Intelligence Artificielle
 
#### Modèles utilisés en production
 
| Service | Modèle | Usage | Performance |
|---------|--------|-------|-------------|
| **Mistral AI** | `mistral-small-latest` | Génération de texte (titre, univers, scénario, personnages, lieux) | Rapide (~2-5s/appel), cohérent, français natif |
| **Hugging Face** | `black-forest-labs/FLUX.1-schnell` | Génération d'images (concept arts) | Rapide (~5-10s), qualité correcte via API Inference |
 
**Choix du modèle d'image :**
- **FLUX.1-schnell** (Black Forest Labs) choisi car :
  - Modèle rapide optimisé pour l'inférence ("schnell" = rapide en allemand)
  - API Hugging Face Inference gratuite et accessible
  - Qualité d'image correcte pour des concept arts
  - Temps de génération acceptable (~5-10 secondes)
  - Pas besoin de télécharger le modèle localement
 
**Code utilisé :**
```python
# ai_service.py
model_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
 
response = requests.post(model_url, headers=headers, json={
    "inputs": prompt  
})
 
if response.status_code == 200:
    image_bytes = response.content
    
```
 
 
### Outils de développement
 
- **Git** - Gestion de versions
- **GitHub** - Hébergement du code
- **VS Code** - Éditeurs de code
 
---
 
## Screenshots
 
### Page d'accueil
 
### Tableau de bord utilisateur
 
 
### Formulaire de création
 
 
### Page de détail d'un jeu
 
 
---
 
## Bonus implémentés
 
### Fonctionnalités bonus réalisées
 
#### Système de "favoris" ou "like" **IMPLÉMENTÉ**
- Les utilisateurs peuvent liker/unliker des jeux
- Compteur de likes en temps réel affiché sur chaque jeu
- Page dédiée `/favorites/` pour consulter tous ses jeux favoris
- Relation ManyToMany avec modèle `Favorite` (table de liaison)
- Système d'unicité (un user ne peut liker qu'une fois le même jeu)
- **Code** :
  - Modèle `Favorite` dans `models.py`
  - Vue `toggle_favorite()` et `favorites()` dans `views.py`
  - Affichage du bouton ❤️ dans `game_detail.html`
 
#### Barre de recherche pour filtrer les jeux **IMPLÉMENTÉ**
- Barre de recherche sur la page d'accueil
- Filtres multi-critères : **nom du jeu**, **genre**, **mots-clés**
- Recherche insensible à la casse (utilisation de `__icontains`)
- Utilisation de Django Q objects pour requêtes complexes
- **Code** :
  ```python
  # views.py - fonction home()
  query = request.GET.get('q')
  if query:
      games = games.filter(
          Q(titre__icontains=query) |
          Q(genre__icontains=query) |
          Q(mots_cles__icontains=query)
      )
  ```
 
#### Pop-ups de chargement pendant la génération **IMPLÉMENTÉ**
- Messages Django affichés à chaque étape de génération
- Feedback utilisateur en temps réel :
  - "Génération en cours..." (début)
  - "Jeu créé avec succès!" (succès)
  - "Erreur lors de la génération: ..." (échec)
- Système de messages colorés (success, error, warning, info)
- **Code** :
  ```python
  from django.contrib import messages
  messages.success(request, f'Jeu "{titre}" créé avec succès!')
  messages.error(request, f'Erreur lors de la génération: {str(e)}')
  ```
 
---
 
### Fonctionnalités bonus partiellement implémentées
 
#### GDD complet (Game Design Document) **PARTIELLEMENT IMPLÉMENTÉ**
- **Ce qui est généré** :
  - Titre du jeu
  - Genre et ambiance
  - Univers détaillé (description, style graphique, type de monde)
  - Scénario en 3 actes + twist
  - 3 personnages avec backgrounds et gameplay
  - 4 lieux emblématiques
  - (Optionnel) Concept art
- **Ce qui manque pour un GDD complet** :
  - Mécaniques de gameplay détaillées
  - Système de progression
  - Économie du jeu
  - Arbre de compétences
  - UI/UX mockups
  - Feuille de route de développement
 
---
 
### Fonctionnalités bonus non implémentées
 
#### Système de narration dynamique **NON IMPLÉMENTÉ**
- **Objectif** : Le scénario devait pouvoir évoluer selon les choix de l'utilisateur
- **Pourquoi non fait** :
  - Nécessite un système de "jeu jouable" (pas juste un concept)
  - Implique une logique de branches narratives complexes
  - Aurait nécessité un moteur de choix interactif (type Twine/Ink)
  - Temps de développement trop important
- **Ce qui aurait été nécessaire** :
  ```python
  class Choice(models.Model):
      scenario = models.ForeignKey(Scenario)
      text = models.TextField()
      next_act = models.ForeignKey('self', null=True)
  
  class PlayerProgress(models.Model):
      user = models.ForeignKey(User)
      game = models.ForeignKey(Game)
      current_choice = models.ForeignKey(Choice)
  ```
 
#### Export PDF stylisé **NON IMPLÉMENTÉ**
- **Objectif** : Télécharger une fiche jeu auto-maquettée (style Steam/itch.io)
- **Pourquoi non fait** :
  - Complexité de la mise en page PDF avec Python
  - Nécessite des librairies lourdes (`reportlab`, `weasyprint`, `xhtml2pdf`)
  - Design graphique demande beaucoup de temps
  - Gestion des images dans le PDF compliquée
- **Ce qui aurait été nécessaire** :
  ```python
  from reportlab.lib.pagesizes import A4
  from reportlab.platypus import SimpleDocTemplate, Paragraph
  
  def export_game_pdf(request, game_id):
      game = Game.objects.get(id=game_id)
      buffer = io.BytesIO()
      doc = SimpleDocTemplate(buffer, pagesize=A4)
      return FileResponse(buffer, filename=f'{game.titre}.pdf')
  ```
 
#### Page de paramètres de compte **NON IMPLÉMENTÉ**
- **Objectif** : Permettre à l'utilisateur de modifier ses informations (email, mot de passe, préférences)
- **Pourquoi non fait** :
  - Manque de temps en fin de projet
  - Fonctionnalité "nice to have" mais pas critique
  - Django admin permet déjà ces modifications pour les superusers
- **Ce qui aurait été nécessaire** :
  ```python
  # views.py
  @login_required
  def profile_settings(request):
      if request.method == 'POST':
          form = UserSettingsForm(request.POST, instance=request.user)
          if form.is_valid():
              form.save()
              messages.success(request, 'Profil mis à jour!')
      else:
          form = UserSettingsForm(instance=request.user)
      return render(request, 'games/settings.html', {'form': form})
  ```
 
---
 
### Récapitulatif des bonus
 
| Bonus | Statut |
|-------|--------|
| Système de favoris/likes | **Fait** |
| Barre de recherche | **Fait** |
| Pop-ups de chargement | **Fait** |
| GDD complet | **Partiel** |
| Narration dynamique | **Non fait** |
| Export PDF | **Non fait** |
| Page paramètres | **Non fait** |
 
**Total implémenté** : 3/7 bonus complets + 1 partiel = **~55% des bonus**
 
---
 
## Tests & Expérimentations
 
### Tests de modèles d'IA
 
#### Hugging Face - Génération de texte
 
**Modèles testés :**
 
1. **GPT-2** (`gpt2`)
   - **Résultat** : Mauvaise qualité pour le français
   - **Problèmes** :
     - Texte incohérent et mal structuré
     - Mélange de langues (anglais/français)
     - Impossibilité de forcer un format JSON
   - **Code testé** :
     ```python
     from transformers import pipeline
     generator = pipeline('text-generation', model='gpt2')
     result = generator("Génère un titre de jeu RPG sombre:")
     ```
 
2. **Facebook OPT-1.3B** (`facebook/opt-1.3b`)
   - **Résultat** : Performances décevantes
   - **Problèmes** :
     - Temps de chargement très long (~5 minutes)
     - Réponses hors contexte
     - Pas de support natif du français
   - **Conclusion** : Modèle trop limité pour notre cas d'usage
 
**Pourquoi Mistral AI a été choisi :**
- Support natif du français
- API simple et rapide
- Possibilité de forcer des formats JSON
- Qualité de génération supérieure
- Documentation claire
 
#### Hugging Face - Génération d'images
 
**Modèles testés :**
 
1. **Stable Diffusion 2.1** (`stabilityai/stable-diffusion-2-1`)
   - **Problème majeur** : Téléchargement initial de 10-15 minutes
   - **Code testé** :
     ```python
     from diffusers import StableDiffusionPipeline
     import torch
    
     pipe = StableDiffusionPipeline.from_pretrained(
         "stabilityai/stable-diffusion-2-1",
         torch_dtype=torch.float16
     )
     pipe = pipe.to("cuda")
    
     image = pipe(
         "cyberpunk game concept art, neon lights, futuristic city",
         num_inference_steps=50
     ).images[0]
     ```
   - **Résultats** :
     - Images souvent noires ou corrompues
     - Nécessite CUDA/GPU (problème sur machines sans GPU)
     - Consommation RAM excessive (~8-12GB)
     - Temps de génération : ~30-60 secondes par image (avec GPU)
 
2. **Stable Diffusion v1-5** (`runwayml/stable-diffusion-v1-5`)
   - Problèmes similaires à SD 2.1
   - Instabilité des résultats
 
3. **Stable Diffusion v1-4** (`CompVis/stable-diffusion-v1-4`)
   - Version obsolète
   - Résultats de qualité inférieure
 
4. **API Hugging Face Inference (premiers tests)**
   - Code testé avec Stable Diffusion :
     ```python
     import requests
    
     API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
     headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
     response = requests.post(API_URL, headers=headers, json={
         "inputs": "cyberpunk game concept art"
     })
    
     image_bytes = response.content
     ```
   - **Problèmes** :
     - Rate limit gratuit très restrictif (10-20 images/jour)
     - Latence élevée (30-60s par image)
     - File d'attente si modèle "cold"
     - Quota rapidement épuisé en développement
 
5. **FLUX.1-schnell** (`black-forest-labs/FLUX.1-schnell`) **→ SOLUTION FINALE**
   - **Succès** : Modèle rapide et de qualité via API Hugging Face
   - **Code final utilisé** :
     ```python
     # ai_service.py
     def generate_and_save_image(self, titre, genre, ambiance, universe_desc):
         model_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
         headers = {"Authorization": f"Bearer {self.hf_api_key}"}
         
         prompt = f"Video game concept art: {titre}, {genre} genre, {ambiance} atmosphere, {universe_desc[:100]}, high quality, detailed"
         
         response = requests.post(model_url, headers=headers, json={
             "inputs": prompt
         })
         
         if response.status_code == 200:
             return {
                 'image_data': ContentFile(response.content),
                 'description': prompt
             }
     ```
   - **Avantages** :
     - Temps de génération rapide (~5-10 secondes)
     - Qualité d'image satisfaisante pour des concept arts
     - API gratuite Hugging Face (avec limits raisonnables)
     - Pas de téléchargement de modèle local nécessaire
     - Pas besoin de GPU
     - "schnell" = optimisé pour la vitesse (allemand)
   - **Limites** :
     - Rate limit API gratuite (~100 images/jour)
     - Qualité inférieure à FLUX.1-pro (version payante)
 
**Conclusion finale :**
- **Hugging Face local** : Trop lent et instable pour la production
- **Stable Diffusion API** : Limites trop restrictives
- **FLUX.1-schnell** : **Meilleur compromis** vitesse/qualité/gratuité
- **Mistral AI Agents** : Alternative testée mais fonctionnalité bêta instable
 
 
## Limites & Améliorations futures
 
### Fonctionnalités non implémentées
 
1. **Système de commentaires**
   - Pas de possibilité de commenter les créations
   - **Raison** : Temps insuffisant
   - **Solution future** : Modèle `Comment` avec ForeignKey vers `Game` et `User`
 
2. **Support multilingue**
   - Application uniquement en français
   - **Raison** : Django i18n non implémenté
   - **Solution future** : Utiliser `django.utils.translation` et fichiers `.po`
 
3. **Partage sur réseaux sociaux**
   - Pas de boutons "Partager sur Twitter/Facebook"
   - **Raison** : Nécessite meta tags Open Graph
   - **Solution future** : Ajouter `django-meta` et meta tags dynamiques
 
4. **Analytics & statistiques**
    - Pas de tableau de bord avec stats (jeux les plus likés, tendances, etc.)
    - **Raison** : Manque de temps
    - **Solution future** : Utiliser Django Aggregation (`Count`, `Avg`, etc.)
 
3. **Page de paramètres de compte**
    - Modifier ses informations (email, mot de passe, préférences)
    - **Raison** : Manque de temps, fonctionnalité "nice to have"
    - **Solution future** : Formulaire `UserSettingsForm` avec vue dédiée `/settings/`
 
### Bugs connus & limitations
 
1. **Performance sur génération longue**
   - L'utilisateur peut penser que le site est bloqué (30-40s sans feedback)
   - **Amélioration** : Ajouter une barre de progression (via AJAX/WebSockets) ou tâche asynchrone (Celery)
 
2. **Pas de validation de l'API key**
   - Si la clé Mistral est invalide, l'erreur n'apparaît qu'à la première génération
   - **Amélioration** : Vérifier la clé au démarrage de l'application (dans `apps.py`)
 
3. **Limite de caractères non gérée**
   - Les champs `TextField` n'ont pas de limite, peut causer des problèmes d'affichage
   - **Amélioration** : Ajouter `max_length` ou tronquer dans les templates
 
4. **Pas de pagination**
   - Si 1000+ jeux publics, la page d'accueil sera lente
   - **Amélioration** : Utiliser `django.core.paginator.Paginator`
 
 
### Améliorations futures prioritaires
 
1. **Génération asynchrone avec Celery**
   ```python
   # tasks.py
   from celery import shared_task
   
   @shared_task
   def generate_game_async(user_id, params):
       # Génération en arrière-plan
       # Notification par email ou WebSocket quand terminé
   ```
 
2. **Cache Redis**
   - Cache des résultats d'IA pour requêtes similaires
   - Réduction des coûts API
 
 
3. **API REST avec Django REST Framework**
   - Permettre aux développeurs tiers d'utiliser Gameforge
   - Endpoints : `/api/games/`, `/api/games/<id>/`, etc.
 
 
4. **Mode offline/démo**
   - Utiliser des modèles locaux plus petits (GPT-2 fine-tuné)
   - Pour les utilisateurs sans clé API
 
 
## Équipe
 
### Développeurs
 
- **Eva Depaepe**
- **Mathis Ponsson**
- **Romain Roche**
- **Emilie Delrue**
 
 
### Liens
 
- **GitHub** : [github.com/evadpe/Gameforge](https://github.com/evadpe/Gameforge)
 
---# Gameforge
