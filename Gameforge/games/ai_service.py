"""
Service d'IA pour générer du contenu de jeu vidéo
Utilise l'API Mistral AI pour le texte et les images
"""

import os
import json
import random
from typing import Dict, List, Optional
from mistralai import Mistral
from django.conf import settings
from django.core.files.base import ContentFile


class AIService:
    def __init__(self):
        # Méthode 1: Via les settings Django (recommandée)
        self.mistral_key = getattr(settings, 'MISTRAL_API_KEY', None)
        
        # Méthode 2: Fallback direct depuis les variables d'environnement
        if not self.mistral_key:
            self.mistral_key = os.getenv('MISTRAL_API_KEY')
        
        # Nettoyer la clé
        if self.mistral_key:
            self.mistral_key = self.mistral_key.strip().lstrip('=')
        
        # Initialiser le client Mistral
        self.client = None
        self.model = "mistral-small-latest"
        self.image_agent = None
        
        if self.mistral_key and len(self.mistral_key) > 10:  # Vérifier que la clé semble valide
            try:
                self.client = Mistral(api_key=self.mistral_key)
                print(f" Client Mistral initialisé avec la clé : {self.mistral_key[:8]}...")
                
                # Créer un agent pour la génération d'images
                try:
                    self.image_agent = self.client.beta.agents.create(
                        model="mistral-medium-latest",
                        name="Game Image Generator",
                        description="Agent spécialisé dans la génération d'images conceptuelles pour jeux vidéo",
                        instructions="Tu es un artiste conceptuel expert en jeux vidéo. Génère des images épiques et professionnelles qui capturent l'essence des univers de jeux.",
                        tools=[{"type": "image_generation"}],
                        completion_args={
                            "temperature": 0.7,
                            "top_p": 0.95,
                        }
                    )
                    print(f" Agent de génération d'images créé: {self.image_agent.id}")
                except Exception as e:
                    print(f"⚠️ Impossible de créer l'agent d'images (peut-être pas activé sur votre compte): {e}")
                    self.image_agent = None
                    
            except Exception as e:
                print(f" Erreur initialisation client Mistral: {e}")
                self.client = None
        else:
            print("⚠️ MISTRAL_API_KEY invalide ou manquante - mode démo activé")
            print(f"   Clé trouvée: '{self.mistral_key}'")
    
    def _call_api(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Appelle l'API Mistral pour la génération de texte
        """
        if not self.client:
            print("Mode démo - génération de contenu mock")
            return self._generate_mock_content(prompt)
        
        try:
            print(f"Appel Mistral API...")
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "Tu es un créateur de jeux vidéo expert. Réponds de manière concise et créative en français."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=max_tokens,
                top_p=0.95
            )
            
            result = chat_response.choices[0].message.content
            print(f" Réponse API reçue : {result[:100]}...")
            return result.strip()
            
        except Exception as e:
            print(f" Erreur Mistral API: {e}")
            return self._generate_mock_content(prompt)

    def _generate_mock_content(self, prompt: str) -> str:
        """
        Génère du contenu de démo sans API
        """
        if "titre" in prompt.lower():
            prefixes = ["Les Chroniques de", "La Légende de", "L'Aventure de", "Les Secrets de"]
            suffixes = ["l'Ombre", "la Lumière", "l'Éternité", "Azura", "Nexus"]
            return f"{random.choice(prefixes)} {random.choice(suffixes)}"
        return "Contenu généré en mode démo (configurez MISTRAL_API_KEY pour utiliser l'IA)"
    
    def generate_game_title(self, genre: str, ambiance: str, keywords: List[str]) -> str:
        """
        Génère un titre de jeu
        """
        keywords_str = ", ".join(keywords) if keywords else "aventure"
        
        prompt = f"""Génère UN SEUL titre original et captivant pour un jeu vidéo {genre} avec une ambiance {ambiance}.
Mots-clés: {keywords_str}

Réponds UNIQUEMENT avec le titre, sans guillemets, sans explication, sans introduction.

Titre:"""
        
        title = self._call_api(prompt, max_tokens=50)
        title = title.strip().strip('"').strip("'").strip()
        lines = title.split('\n')
        return lines[0] if lines else title
    
    def generate_universe(self, game_title: str, genre: str, ambiance: str, keywords: str) -> Dict[str, str]:
        """
        Génère la description de l'univers du jeu
        """
        prompt = f"""Décris l'univers d'un jeu vidéo intitulé "{game_title}".
Genre: {genre}
Ambiance: {ambiance}
Éléments clés: {keywords}

Écris 2-3 paragraphes décrivant l'univers, le contexte, et l'atmosphère du jeu.
Sois descriptif et immersif.

Description:"""
        
        description = self._call_api(prompt, max_tokens=400)
        
        return {
            'description': description.strip(),
            'style_graphique': self._suggest_art_style(genre, ambiance),
            'type_monde': self._suggest_world_type(genre)
        }
    
    def _suggest_art_style(self, genre: str, ambiance: str) -> str:
        """Suggère un style artistique basé sur le genre et l'ambiance"""
        mapping = {
            'horror': 'realiste',
            'sci-fi': 'realiste',
            'cyberpunk': 'realiste',
            'fantasy': 'anime',
            'rpg': 'anime',
        }
        return mapping.get(genre, 'realiste')
    
    def _suggest_world_type(self, genre: str) -> str:
        """Suggère un type de monde basé sur le genre"""
        mapping = {
            'rpg': 'open_world',
            'aventure': 'open_world',
            'action': 'lineaire',
            'horror': 'lineaire',
            'strategie': 'hub',
        }
        return mapping.get(genre, 'open_world')
    
    def generate_scenario(self, game_title: str, universe_description: str, genre: str) -> Dict[str, str]:
        """
        Génère un scénario en 3 actes
        """
        prompt = f"""Crée un scénario de jeu vidéo en 3 actes pour "{game_title}".
Genre: {genre}
Univers: {universe_description[:200]}

Structure (écris directement chaque acte, sans les labels):

1. ACTE 1 (Introduction): Un paragraphe

2. ACTE 2 (Développement): Un paragraphe

3. ACTE 3 (Climax): Un paragraphe

4. TWIST: Un retournement de situation inattendu

Scénario:"""
        
        scenario_text = self._call_api(prompt, max_tokens=600)
        
        # Parser le résultat
        paragraphs = [p.strip() for p in scenario_text.split('\n\n') if p.strip()]
        
        # Filtrer les labels si présents
        clean_paragraphs = []
        for p in paragraphs:
            # Enlever les numéros et labels en début
            p = p.lstrip('1234.- ')
            if not any(label in p[:30] for label in ['ACTE', 'TWIST', 'Introduction', 'Développement', 'Climax']):
                clean_paragraphs.append(p)
            else:
                # Garder ce qui est après le label
                for sep in [':', '-', '.']:
                    if sep in p:
                        clean_paragraphs.append(p.split(sep, 1)[1].strip())
                        break
        
        return {
            'acte_1': clean_paragraphs[0] if len(clean_paragraphs) > 0 else "Le héros découvre son destin.",
            'acte_2': clean_paragraphs[1] if len(clean_paragraphs) > 1 else "Le héros affronte des épreuves.",
            'acte_3': clean_paragraphs[2] if len(clean_paragraphs) > 2 else "Le héros triomphe du mal.",
            'twist': clean_paragraphs[3] if len(clean_paragraphs) > 3 else "Un secret est révélé."
        }

    def generate_characters(self, game_title: str, genre: str, num_characters: int = 3) -> List[Dict[str, str]]:
        """
        Génère des personnages détaillés pour le jeu
        """
        prompt = f"""Crée {num_characters} personnages pour le jeu "{game_title}" (genre: {genre}).

Pour CHAQUE personnage, utilise EXACTEMENT ce format:

NOM: [nom du personnage]
ROLE: [héros/antagoniste/allié/mentor]
CLASSE: [guerrier/mage/archer/voleur/etc]
PERSONNALITE: [3-4 traits de caractère]
BACKGROUND: [histoire en 2-3 phrases]
APPARENCE: [description physique]
COMPETENCES: [capacités principales]
GAMEPLAY: [comment on joue ce personnage]

---

Personnages:"""

        characters_text = self._call_api(prompt, max_tokens=800)
        
        characters = []
        char_blocks = characters_text.split('---')
        
        for block in char_blocks:
            if 'NOM:' in block:
                char = {}
                lines = block.strip().split('\n')
                
                current_field = None
                for line in lines:
                    line = line.strip()
                    if line.startswith('NOM:'):
                        char['nom'] = line.replace('NOM:', '').strip()
                        current_field = None
                    elif line.startswith('ROLE:') or line.startswith('RÔLE:'):
                        char['role'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif line.startswith('CLASSE:'):
                        char['classe'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif line.startswith('PERSONNALITE:') or line.startswith('PERSONNALITÉ:'):
                        char['personnalite'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif line.startswith('BACKGROUND:'):
                        char['background'] = line.split(':', 1)[1].strip()
                        current_field = 'background'
                    elif line.startswith('APPARENCE:'):
                        char['apparence'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif line.startswith('COMPETENCES:') or line.startswith('COMPÉTENCES:'):
                        char['competences'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif line.startswith('GAMEPLAY:'):
                        char['gameplay_description'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif current_field and line and not any(x in line for x in ['NOM:', 'ROLE:', 'CLASSE:', 'PERSONNALITE:', 'BACKGROUND:', 'APPARENCE:', 'COMPETENCES:', 'GAMEPLAY:']):
                        char[current_field] += ' ' + line
                
                if 'nom' in char and 'background' in char:
                    char.setdefault('role', 'allié')
                    char.setdefault('classe', 'guerrier')
                    char.setdefault('personnalite', 'Courageux et déterminé')
                    char.setdefault('apparence', 'Apparence héroïque')
                    char.setdefault('competences', 'Combat et leadership')
                    char.setdefault('gameplay_description', 'Personnage équilibré')
                    characters.append(char)
        
        # Fallback si parsing échoue
        if len(characters) < num_characters:
            default_chars = [
                {
                    'nom': 'Aelwyn',
                    'role': 'héros',
                    'classe': 'mage',
                    'personnalite': 'Curieux, intelligent, réservé',
                    'background': 'Jeune mage découvrant ses pouvoirs dans un monde en péril.',
                    'apparence': 'Jeune homme aux cheveux argentés et yeux perçants',
                    'competences': 'Magie élémentaire, télékinésie, barrières mystiques',
                    'gameplay_description': 'Mage polyvalent avec des sorts offensifs et défensifs.'
                },
                {
                    'nom': 'Kaelen',
                    'role': 'antagoniste',
                    'classe': 'guerrier',
                    'personnalite': 'Ambiteux, impitoyable, charismatique',
                    'background': 'Seigneur de guerre cherchant à dominer le royaume.',
                    'apparence': 'Guerrier en armure noire aux yeux ardents',
                    'competences': 'Combat à deux mains, intimidation, commandement',
                    'gameplay_description': 'Guerrier puissant avec des attaques dévastatrices.'
                },
                {
                    'nom': 'Lyra',
                    'role': 'allié',
                    'classe': 'archer',
                    'personnalite': 'Loyale, observatrice, sarcastique',
                    'background': 'Chasseresse expérimentée guidant le héros à travers les terres sauvages.',
                    'apparence': 'Jeune femme aux cheveux roux et tatouages tribaux',
                    'competences': 'Tir précis, pistage, furtivité',
                    'gameplay_description': 'Archer à distance avec une grande précision.'
                }
            ]
            while len(characters) < num_characters:
                characters.append(default_chars[len(characters) % len(default_chars)])
        
        return characters[:num_characters]

    def generate_game_image(self, game_title: str, genre: str, ambiance: str, universe_description: str) -> str:
        """
        Génère une description textuelle pour une image conceptuelle
        (utilisé comme fallback si la génération d'image réelle échoue)
        """
        prompt = f"""Crée une description détaillée pour une image conceptuelle de jeu vidéo intitulé "{game_title}".

Genre: {genre}
Ambiance: {ambiance}
Univers: {universe_description[:200]}

La description doit être visuelle et détaillée, incluant:
- Style artistique (ex: réaliste, anime, cartoon, peinture numérique)
- Éléments principaux (personnages, environnement, atmosphère)
- Couleurs dominantes
- Composition de l'image

Description conceptuelle:"""

        image_description = self._call_api(prompt, max_tokens=300)
        return image_description.strip()

    def generate_and_save_image(self, game_title: str, genre: str, ambiance: str, universe_description: str) -> Dict:
        """
        Génère une vraie image avec Mistral Agents API (FLUX)
        Retourne un dictionnaire avec la description et les données de l'image
        """
        if not self.client or not self.image_agent:
            print("⚠️ Mode démo - génération d'image désactivée")
            description = self.generate_game_image(game_title, genre, ambiance, universe_description)
            return {
                'description': description,
                'image_data': None,
                'image_url': None
            }
        
        # Créer un prompt optimisé pour FLUX
        prompt = f"""Génère une image de cover art professionnelle pour le jeu vidéo "{game_title}".

Style: Cover art AAA, qualité cinématographique
Genre: {genre}
Ambiance: {ambiance}
Univers: {universe_description[:250]}

L'image doit être épique, immersive et capturer visuellement l'essence du jeu. Style professionnel de jaquette de jeu vidéo."""
        
        try:
            print(f"Génération d'image pour '{game_title}'...")
            
            # Démarrer une conversation avec l'agent d'images
            response = self.client.beta.conversations.start(
                agent_id=self.image_agent.id,
                inputs=prompt
            )
            
            # Extraire le file_id de l'image générée
            file_id = None
            
            # Importer ToolFileChunk pour la vérification de type
            from mistralai.models import ToolFileChunk
            
            # Parcourir les outputs de la réponse
            if hasattr(response, 'outputs') and response.outputs:
                for output in response.outputs:
                    if hasattr(output, 'content'):
                        for chunk in output.content:
                            # Chercher le chunk de type ToolFileChunk
                            if isinstance(chunk, ToolFileChunk):
                                file_id = chunk.file_id
                                print(f" Image générée avec file_id: {file_id}")
                                break
                        if file_id:
                            break
            
            if file_id:
                # Télécharger l'image depuis Mistral
                print(f"⬇️ Téléchargement de l'image...")
                file_bytes = self.client.files.download(file_id=file_id).read()
                
                print(f" Image téléchargée ({len(file_bytes)} bytes)")
                
                return {
                    'description': prompt,
                    'image_data': ContentFile(file_bytes),
                    'image_url': None  # Mistral ne fournit pas d'URL publique
                }
            else:
                print(" Aucune image générée dans la réponse")
                print(f"   Structure de la réponse: {type(response)}")
                if hasattr(response, 'outputs'):
                    print(f"   Nombre d'outputs: {len(response.outputs)}")
                description = self.generate_game_image(game_title, genre, ambiance, universe_description)
                return {
                    'description': description,
                    'image_data': None,
                    'image_url': None
                }
                
        except Exception as e:
            print(f" Erreur lors de la génération d'image: {e}")
            import traceback
            traceback.print_exc()
            # Fallback sur la description textuelle
            description = self.generate_game_image(game_title, genre, ambiance, universe_description)
            return {
                'description': description,
                'image_data': None,
                'image_url': None
            }

    def generate_locations(self, game_title: str, universe: str, num_locations: int = 4) -> List[Dict[str, str]]:
        """
        Génère des lieux emblématiques avec plus de détails
        """
        prompt = f"""Crée {num_locations} lieux emblématiques pour le jeu "{game_title}".
Univers: {universe[:150]}

Pour chaque lieu, utilise EXACTEMENT ce format:

NOM: [nom du lieu]
TYPE: [ville/forêt/dongeon/temple/château/ruines/etc]
DESCRIPTION: [description en 2-3 phrases]
IMPORTANCE: [importance dans l'histoire]
DANGERS: [dangers ou énigmes présents]
TRESORS: [récompenses ou secrets à découvrir]

---

Lieux:"""

        locations_text = self._call_api(prompt, max_tokens=700)
        
        locations = []
        loc_blocks = locations_text.split('---')
        
        for block in loc_blocks:
            if 'NOM:' in block:
                loc = {}
                lines = block.strip().split('\n')
                
                current_field = None
                for line in lines:
                    line = line.strip()
                    if line.startswith('NOM:'):
                        loc['nom'] = line.replace('NOM:', '').strip()
                        current_field = None
                    elif line.startswith('TYPE:'):
                        loc['type'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif line.startswith('DESCRIPTION:'):
                        loc['description'] = line.split(':', 1)[1].strip()
                        current_field = 'description'
                    elif line.startswith('IMPORTANCE:'):
                        loc['importance'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif line.startswith('DANGERS:'):
                        loc['dangers'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif line.startswith('TRESORS:') or line.startswith('TRÉSORS:'):
                        loc['tresors'] = line.split(':', 1)[1].strip()
                        current_field = None
                    elif current_field and line and not any(x in line for x in ['NOM:', 'TYPE:', 'DESCRIPTION:', 'IMPORTANCE:', 'DANGERS:', 'TRESORS:']):
                        # Continuer le champ en cours
                        loc[current_field] += ' ' + line
                
                if 'nom' in loc and 'description' in loc:
                    loc.setdefault('type', 'zone mystérieuse')
                    loc.setdefault('importance', 'Lieu clé pour la quête principale')
                    loc.setdefault('dangers', 'Créatures hostiles et pièges anciens')
                    loc.setdefault('tresors', 'Artéfacts puissants et connaissances perdues')
                    locations.append(loc)
        
        # Fallback
        if len(locations) < num_locations:
            default_locs = [
                {
                    'nom': 'Cité Céleste d\'Aetheria',
                    'type': 'ville flottante',
                    'description': 'Ancienne cité suspendue dans les cieux, bâtie sur des fragments de cristal volants.',
                    'importance': 'Capitale du royaume et lieu de départ de la quête',
                    'dangers': 'Chutes mortelles et gardiens célestes',
                    'tresors': 'Cristaux de pouvoir et archives anciennes'
                },
                {
                    'nom': 'Forêt des Murmures',
                    'type': 'forêt enchantée',
                    'description': 'Forêt ancienne où les arbres parlent et la magie coule comme une rivière.',
                    'importance': 'Cache le sanctuaire des druides et des secrets anciens',
                    'dangers': 'Illusions trompeuses et créatures ensorcelées',
                    'tresors': 'Herbes rares et artefacts druidiques'
                },
                {
                    'nom': 'Abysses Oubliées',
                    'type': 'dongeon sous-marin',
                    'description': 'Cité engloutie au fond de l\'océan, habitée par des créatures des profondeurs.',
                    'importance': 'Contient le trident du roi des mers',
                    'dangers': 'Pression écrasante et prédateurs abyssaux',
                    'tresors': 'Perles légendaires et technologie ancienne'
                },
                {
                    'nom': 'Pic du Destin',
                    'type': 'montagne sacrée',
                    'description': 'Plus haute montagne du monde, où seuls les plus courageux osent s\'aventurer.',
                    'importance': 'Lieu du combat final contre le seigneur des ténèbres',
                    'dangers': 'Vents glacials et sentiers périlleux',
                    'tresors': 'Arme légendaire et vision du futur'
                }
            ]
            while len(locations) < num_locations:
                locations.append(default_locs[len(locations) % len(default_locs)])
        
        return locations[:num_locations]

    def generate_random_game_params(self) -> Dict[str, str]:
        """
        Génère des paramètres aléatoires pour un jeu
        """
        genres = ['rpg', 'action', 'aventure', 'strategie', 'horror', 'sci-fi', 'fantasy', 'cyberpunk']
        ambiances = ['sombre', 'joyeux', 'mysterieux', 'epique', 'humoristique']
        
        keywords_pool = [
            'magie', 'dragons', 'technologie', 'espace', 'zombies', 
            'pirates', 'ninjas', 'robots', 'vampires', 'aliens'
        ]
        
        return {
            'genre': random.choice(genres),
            'ambiance': random.choice(ambiances),
            'keywords': ', '.join(random.sample(keywords_pool, 3))
        }