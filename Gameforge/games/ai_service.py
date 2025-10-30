"""
Service d'IA pour générer du contenu de jeu vidéo
Utilise l'API Mistral AI pour le texte et les images
"""

import os
import json
import random
import re
import time
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
        
        # Configuration retry pour gérer les erreurs 429
        self.max_retries = 3
        self.retry_delay = 2  # secondes
        
        if self.mistral_key and len(self.mistral_key) > 10:
            try:
                self.client = Mistral(api_key=self.mistral_key)
                print(f"✅ Client Mistral initialisé avec la clé : {self.mistral_key[:8]}...")
                
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
                    print(f"✅ Agent de génération d'images créé: {self.image_agent.id}")
                except Exception as e:
                    print(f"⚠️ Impossible de créer l'agent d'images (peut-être pas activé sur votre compte): {e}")
                    self.image_agent = None
                    
            except Exception as e:
                print(f"❌ Erreur initialisation client Mistral: {e}")
                self.client = None
        else:
            print("⚠️ MISTRAL_API_KEY invalide ou manquante - mode démo activé")
            print(f"   Clé trouvée: '{self.mistral_key}'")
    
    def _clean_markdown(self, text: str) -> str:
        """
        Nettoie le markdown pour faciliter le parsing
        Enlève les astérisques, etc.
        """
        # Enlever les astérisques markdown (gras)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        return text
    
    def _call_api(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Appelle l'API Mistral pour la génération de texte avec retry automatique
        """
        if not self.client:
            print("⚠️ Mode démo - génération de contenu mock")
            return self._generate_mock_content(prompt)
        
        # Tentatives avec retry exponentiel
        for attempt in range(self.max_retries):
            try:
                print(f"📡 Appel Mistral API (tentative {attempt + 1}/{self.max_retries})...")
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
                print(f"✅ Réponse API reçue : {result[:100]}...")
                return result.strip()
                
            except Exception as e:
                error_str = str(e)
                
                # Détecter erreur 429 (rate limit)
                if "429" in error_str or "capacity exceeded" in error_str.lower():
                    if attempt < self.max_retries - 1:
                        wait_time = self.retry_delay * (2 ** attempt)  # Backoff exponentiel
                        print(f"⏳ Rate limit atteint (429). Attente de {wait_time}s avant nouvelle tentative...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"❌ Rate limit persistant après {self.max_retries} tentatives")
                        print("💡 Basculement vers le mode démo")
                        return self._generate_mock_content(prompt)
                
                # Autres erreurs
                print(f"❌ Erreur Mistral API: {e}")
                if attempt < self.max_retries - 1:
                    print(f"🔄 Nouvelle tentative dans {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return self._generate_mock_content(prompt)
        
        return self._generate_mock_content(prompt)

    def _generate_mock_content(self, prompt: str) -> str:
        """
        Génère du contenu de démo sans API - AMÉLIORÉ pour être plus varié
        """
        import hashlib
        
        # Créer un seed unique basé sur le prompt
        seed = hashlib.md5(prompt.encode()).hexdigest()
        hash_val = int(seed, 16)
        
        if "titre" in prompt.lower():
            prefixes = [
                "Les Chroniques de", "La Légende de", "L'Aventure de", "Les Secrets de",
                "Le Royaume de", "Les Gardiens de", "L'Éveil de", "La Quête de",
                "Les Ombres de", "Le Destin de", "Les Héros de", "L'Odyssée de"
            ]
            suffixes = [
                "l'Ombre", "la Lumière", "l'Éternité", "Azura", "Nexus",
                "Eldoria", "Véridian", "l'Aube", "Midnight", "Atheron",
                "Zephyria", "Obsidian", "Celestia", "Avalon", "Arcadia"
            ]
            prefix = prefixes[hash_val % len(prefixes)]
            suffix = suffixes[(hash_val // 13) % len(suffixes)]
            return f"{prefix} {suffix}"
        
        elif "personnage" in prompt.lower() or "NOM:" in prompt:
            # Mock de personnages avec format structuré et variation
            names = ["Aelric", "Zara", "Theron", "Lyssa", "Kael", "Nyx", "Orin", "Selene"]
            roles = ["héros", "antagoniste", "allié", "mentor"]
            classes = ["guerrier", "mage", "archer", "voleur", "paladin", "druide"]
            
            # Détecter l'ambiance dans le prompt
            ambiance_detected = "default"
            if "sombre" in prompt.lower():
                ambiance_detected = "sombre"
            elif "joyeux" in prompt.lower():
                ambiance_detected = "joyeux"
            elif "mysterieux" in prompt.lower():
                ambiance_detected = "mysterieux"
            
            backgrounds = {
                'sombre': "Hanté par un passé tragique, ce personnage cherche la rédemption dans les ombres. Son cœur porte les cicatrices de pertes indicibles.",
                'joyeux': "Optimiste et plein d'énergie, ce personnage apporte joie et espoir partout où il passe. Son rire est contagieux.",
                'mysterieux': "Les origines de ce personnage restent énigmatiques. Entouré de secrets, sa véritable nature reste inconnue.",
                'default': "Un personnage expérimenté dont les compétences sont reconnues. Déterminé à accomplir sa destinée."
            }
            
            name = names[hash_val % len(names)]
            role = roles[(hash_val // 7) % len(roles)]
            classe = classes[(hash_val // 11) % len(classes)]
            background = backgrounds.get(ambiance_detected, backgrounds['default'])
            
            return f"""NOM: {name}
ROLE: {role}
CLASSE: {classe}
PERSONNALITE: Courageux, loyal, mystérieux
BACKGROUND: {background}
APPARENCE: Allure noble avec une aura de puissance
COMPETENCES: Maîtrise du combat et des stratégies
GAMEPLAY: Personnage équilibré avec des capacités variées

---"""
        
        elif "lieu" in prompt.lower() or "TYPE:" in prompt:
            # Mock de lieux avec format structuré et variation
            places = ["Tour", "Cité", "Forêt", "Temple", "Montagne", "Ruines", "Grotte", "Château"]
            adjectives = ["Sombre", "Ancienne", "Mystérieuse", "Sacrée", "Oubliée", "Éternelle", "Maudite", "Céleste"]
            
            # Détecter l'ambiance dans le prompt
            ambiance_detected = "default"
            if "sombre" in prompt.lower() or "dark" in prompt.lower():
                ambiance_detected = "sombre"
            elif "joyeux" in prompt.lower() or "happy" in prompt.lower():
                ambiance_detected = "joyeux"
            elif "mysterieux" in prompt.lower() or "mysterious" in prompt.lower():
                ambiance_detected = "mysterieux"
            
            descriptions = {
                'sombre': "Un lieu désolé où règne une atmosphère oppressante. Les ombres semblent vivantes et peu osent s'y aventurer.",
                'joyeux': "Un lieu vibrant de vie et de couleurs éclatantes. L'atmosphère y est chaleureuse et accueillante.",
                'mysterieux': "Un lieu énigmatique dont les secrets restent bien gardés. Des phénomènes étranges y défient toute explication.",
                'default': "Un lieu légendaire rempli de mystères et de dangers anciens."
            }
            
            place = places[hash_val % len(places)]
            adj = adjectives[(hash_val // 7) % len(adjectives)]
            description = descriptions.get(ambiance_detected, descriptions['default'])
            
            return f"""NOM: {place} {adj}
TYPE: donjon
DESCRIPTION: {description}
IMPORTANCE: Point clé de la quête principale
DANGERS: Créatures hostiles et pièges mortels
TRESORS: Artefacts puissants et connaissances perdues

---"""
        
        elif "scénario" in prompt.lower() or "acte" in prompt.lower():
            return """Le héros découvre son destin dans un monde au bord du chaos.

Les forces obscures se rassemblent et le héros doit former une alliance improbable pour les affronter.

Dans une bataille épique finale, le héros révèle sa véritable nature et sauve le monde.

Un ancien secret révèle que le véritable ennemi était caché depuis le début."""
        
        return "Contenu généré en mode démo (API Mistral indisponible - rate limit atteint)"
    
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

    def generate_characters(self, game_title: str, genre: str, num_characters: int = 3, ambiance: str = None, mots_cles: str = None, universe_description: str = None) -> List[Dict[str, str]]:
        """
        Génère des personnages détaillés pour le jeu avec cohérence thématique
        """
        # Construire un prompt enrichi avec tous les thèmes
        context_parts = [f'Jeu: "{game_title}"', f'Genre: {genre}']
        
        if ambiance:
            context_parts.append(f'Ambiance: {ambiance}')
        if mots_cles:
            context_parts.append(f'Thèmes clés: {mots_cles}')
        if universe_description:
            context_parts.append(f'Univers: {universe_description[:150]}')
        
        context = '\n'.join(context_parts)
        
        prompt = f"""Crée {num_characters} personnages cohérents avec le contexte suivant:

{context}

IMPORTANT: Les personnages doivent refléter l'ambiance et les thèmes du jeu. Par exemple:
- Ambiance "sombre" → personnages torturés, moralement ambigus, avec des backstories tragiques
- Ambiance "joyeux" → personnages optimistes, colorés, avec des motivations positives
- Thèmes "magie, dragons" → classes et compétences liées à la magie et aux dragons
- Genre "cyberpunk" → noms futuristes, compétences technologiques, background urbain dystopique

Pour CHAQUE personnage, utilise EXACTEMENT ce format:

NOM: [nom adapté au thème et genre]
ROLE: [héros/antagoniste/allié/mentor]
CLASSE: [classe cohérente avec le genre et les thèmes]
PERSONNALITE: [traits reflétant l'ambiance]
BACKGROUND: [histoire en 2-3 phrases liée à l'univers]
APPARENCE: [description physique cohérente avec l'ambiance]
COMPETENCES: [capacités liées aux thèmes clés]
GAMEPLAY: [style de jeu adapté au genre]

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
        characters_text = self._clean_markdown(characters_text)
        print(f"📝 Texte nettoyé : {characters_text[:200]}...")
        
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
                    print(f"✅ Personnage parsé : {char['nom']}")
        
        # Génération aléatoire UNIQUE en cas d'échec
        if len(characters) < num_characters:
            print(f"⚠️ Seulement {len(characters)}/{num_characters} personnages parsés")
            print("🎲 Génération de personnages uniques...")
            
            import hashlib
            seed = f"{game_title}_{genre}_{ambiance}_{len(characters)}"
            
            roles = ['héros', 'antagoniste', 'allié', 'mentor', 'rival']
            classes = ['guerrier', 'mage', 'archer', 'voleur', 'paladin', 'druide', 'assassin', 'clerc']
            traits = ['courageux', 'rusé', 'loyal', 'mystérieux', 'impulsif', 'sage', 'sarcastique', 'noble']
            name_parts = ['Ae', 'Kal', 'Thy', 'Zar', 'Lyn', 'Mor', 'Syl', 'Rae', 'Dor', 'Vel']
            
            # Templates variés pour les backgrounds selon l'ambiance
            background_templates = {
                'sombre': [
                    "Hanté par un passé tragique, ce {classe} cherche la rédemption dans les ombres de {game_title}.",
                    "Ayant perdu tout ce qui lui était cher, ce {classe} {trait1} poursuit une quête désespérée.",
                    "Un {classe} tourmenté dont l'âme est aussi {trait1} que son destin est sombre."
                ],
                'joyeux': [
                    "Ce {classe} optimiste apporte joie et espoir partout où il passe dans {game_title}.",
                    "Un {classe} {trait1} qui croit fermement que chaque jour est une nouvelle aventure.",
                    "Avec un sourire éclatant, ce {classe} inspire courage et bonheur à ses compagnons."
                ],
                'mysterieux': [
                    "Les origines de ce {classe} restent énigmatiques, mais sa maîtrise est indéniable.",
                    "Un {classe} {trait1} entouré de secrets et de légendes oubliées.",
                    "Personne ne connaît vraiment ce {classe}, mais tous respectent ses capacités."
                ],
                'epique': [
                    "Destiné à accomplir de grandes choses, ce {classe} {trait1} est une légende vivante.",
                    "Un {classe} héroïque dont les exploits résonnent à travers tout {game_title}.",
                    "Ce {classe} porte sur ses épaules le poids du destin et l'espoir de tous."
                ],
                'default': [
                    "Un {classe} {trait1} dont les compétences sont reconnues dans tout {game_title}.",
                    "Ce {classe} possède un talent naturel et une détermination sans faille.",
                    "Un {classe} expérimenté dont le {trait2} en fait un allié précieux."
                ]
            }
            
            while len(characters) < num_characters:
                char_seed = f"{seed}_{len(characters)}"
                hash_val = int(hashlib.md5(char_seed.encode()).hexdigest(), 16)
                
                role = roles[hash_val % len(roles)]
                classe = classes[(hash_val // 10) % len(classes)]
                trait1 = traits[(hash_val // 100) % len(traits)]
                trait2 = traits[(hash_val // 1000) % len(traits)]
                name = name_parts[hash_val % len(name_parts)] + name_parts[(hash_val // 7) % len(name_parts)]
                
                # Choisir template selon l'ambiance
                amb_key = ambiance.lower() if ambiance and ambiance.lower() in background_templates else 'default'
                templates = background_templates[amb_key]
                template = templates[(hash_val // 50) % len(templates)]
                background = template.format(classe=classe, trait1=trait1, trait2=trait2, game_title=game_title)
                
                char = {
                    'nom': name,
                    'role': role,
                    'classe': classe,
                    'personnalite': f"{trait1.capitalize()}, {trait2}",
                    'background': background,
                    'apparence': f"{classe.capitalize()} à l'allure {trait1}",
                    'competences': f"Maîtrise du {classe} et {trait2}",
                    'gameplay_description': f"Personnage {role} jouable en {classe}"
                }
                characters.append(char)
                print(f"🎲 Personnage généré : {char['nom']}")
        
        return characters[:num_characters]

    def generate_locations(self, game_title: str, universe: str, num_locations: int = 4, genre: str = None, ambiance: str = None, mots_cles: str = None) -> List[Dict[str, str]]:
        """
        Génère des lieux emblématiques cohérents avec les thèmes
        """
        # Construire un contexte enrichi
        context_parts = [f'Jeu: "{game_title}"', f'Univers: {universe[:150]}']
        
        if genre:
            context_parts.append(f'Genre: {genre}')
        if ambiance:
            context_parts.append(f'Ambiance: {ambiance}')
        if mots_cles:
            context_parts.append(f'Thèmes: {mots_cles}')
        
        context = '\n'.join(context_parts)
        
        prompt = f"""Crée {num_locations} lieux emblématiques cohérents avec:

{context}

IMPORTANT: Les lieux doivent refléter l'ambiance et les thèmes:
- Ambiance "sombre" → lieux oppressants, ruines, cachots, zones désolées
- Ambiance "joyeux" → villages colorés, marchés animés, jardins enchantés
- Thèmes "magie" → tours de mages, bibliothèques mystiques, portails magiques
- Thèmes "technologie" → laboratoires, usines, bases high-tech
- Genre "horror" → lieux inquiétants avec atmosphère menaçante

Pour chaque lieu, utilise EXACTEMENT ce format:

NOM: [nom évocateur adapté aux thèmes]
TYPE: [type cohérent avec le genre et l'ambiance]
DESCRIPTION: [2-3 phrases reflétant l'ambiance]
IMPORTANCE: [rôle dans l'histoire lié aux thèmes]
DANGERS: [dangers cohérents avec le genre]
TRESORS: [récompenses liées aux thèmes clés]

NOM: [nom du lieu]
TYPE: [ville/forêt/dongeon/temple/château/ruines/etc]
DESCRIPTION: [description en 2-3 phrases]
IMPORTANCE: [importance dans l'histoire]
DANGERS: [dangers ou énigmes présents]
TRESORS: [récompenses ou secrets à découvrir]

---

Lieux:"""

        locations_text = self._call_api(prompt, max_tokens=700)
        locations_text = self._clean_markdown(locations_text)
        print(f"📝 Texte nettoyé : {locations_text[:200]}...")
        
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
                        loc[current_field] += ' ' + line
                
                if 'nom' in loc and 'description' in loc:
                    loc.setdefault('type', 'zone mystérieuse')
                    loc.setdefault('importance', 'Lieu clé pour la quête principale')
                    loc.setdefault('dangers', 'Créatures hostiles et pièges anciens')
                    loc.setdefault('tresors', 'Artéfacts puissants et connaissances perdues')
                    locations.append(loc)
                    print(f"✅ Lieu parsé : {loc['nom']}")
        
        # Génération aléatoire UNIQUE en cas d'échec
        if len(locations) < num_locations:
            print(f"⚠️ Seulement {len(locations)}/{num_locations} lieux parsés")
            print("🎲 Génération de lieux uniques...")
            
            import hashlib
            seed = f"{game_title}_{universe}_{genre}_{ambiance}_{len(locations)}"
            
            types = ['donjon', 'ville', 'forêt', 'montagne', 'temple', 'ruines', 'grotte', 'château']
            prefixes = ['Tour de', 'Cité de', 'Forêt des', 'Mont', 'Temple de', 'Ruines de', 'Grotte du', 'Château de']
            suffixes = ['Lumière', 'Ténèbres', 'Mystères', 'Sagesse', 'Perdition', 'Éternité', 'Silence', 'Tempête']
            
            # Templates variés pour les descriptions selon l'ambiance
            description_templates = {
                'sombre': [
                    "Un {type_loc} désolé où règne une atmosphère oppressante. Les ombres semblent vivantes et les échos du passé hantent chaque recoin.",
                    "Ce {type_loc} abandonné est imprégné de tristesse et de mystère. Peu osent s'aventurer dans ses profondeurs menaçantes.",
                    "Les ruines de ce {type_loc} racontent une histoire tragique. L'obscurité y est presque palpable."
                ],
                'joyeux': [
                    "Un {type_loc} vibrant de vie et de couleurs éclatantes. Les rires et la musique emplissent l'air de cette oasis de bonheur.",
                    "Ce {type_loc} enchanteur accueille les voyageurs avec chaleur. Son ambiance festive apporte réconfort et espoir.",
                    "Un {type_loc} lumineux où la joie est contagieuse. Chaque visiteur repart le cœur plus léger."
                ],
                'mysterieux': [
                    "Un {type_loc} énigmatique dont les secrets restent bien gardés. Des phénomènes étranges y défient toute explication.",
                    "Ce {type_loc} ancien cache des mystères insondables. Les légendes qui l'entourent sont aussi fascinantes qu'inquiétantes.",
                    "Un {type_loc} où le temps semble suspendu. Les mystères qui s'y cachent attirent les curieux et les aventuriers."
                ],
                'epique': [
                    "Un {type_loc} majestueux qui inspire respect et admiration. Son importance dans l'histoire est gravée dans chaque pierre.",
                    "Ce {type_loc} légendaire a été le théâtre de batailles épiques. Sa grandeur témoigne des héros qui y ont combattu.",
                    "Un {type_loc} imposant dont la magnificence coupe le souffle. C'est ici que le destin du monde se joue."
                ],
                'default': [
                    "Un {type_loc} remarquable qui joue un rôle crucial dans l'aventure. Son architecture unique attire l'attention.",
                    "Ce {type_loc} fascinant recèle bien des surprises pour les explorateurs audacieux.",
                    "Un {type_loc} important dont l'influence se fait sentir dans toute la région."
                ]
            }
            
            danger_templates = [
                "Créatures hostiles et pièges ancestraux",
                "Gardiens corrompus et énigmes mortelles",
                "Forces mystérieuses et embuscades dangereuses",
                "Entités anciennes et défenses magiques",
                "Pièges sophistiqués et ennemis redoutables"
            ]
            
            treasure_templates = [
                "Artéfacts légendaires et connaissances perdues",
                "Trésors cachés et secrets anciens",
                "Reliques puissantes et grimoires mystiques",
                "Richesses inestimables et pouvoirs oubliés",
                "Équipements rares et manuscrits précieux"
            ]
            
            while len(locations) < num_locations:
                loc_seed = f"{seed}_{len(locations)}"
                hash_val = int(hashlib.md5(loc_seed.encode()).hexdigest(), 16)
                
                type_loc = types[hash_val % len(types)]
                prefix = prefixes[hash_val % len(prefixes)]
                suffix = suffixes[(hash_val // 7) % len(suffixes)]
                
                # Choisir template selon l'ambiance
                amb_key = ambiance.lower() if ambiance and ambiance.lower() in description_templates else 'default'
                templates = description_templates[amb_key]
                template = templates[(hash_val // 50) % len(templates)]
                description = template.format(type_loc=type_loc)
                
                loc = {
                    'nom': f"{prefix} {suffix}",
                    'type': type_loc,
                    'description': description,
                    'importance': f"Lieu stratégique lié aux événements majeurs de {game_title}",
                    'dangers': danger_templates[(hash_val // 100) % len(danger_templates)],
                    'tresors': treasure_templates[(hash_val // 200) % len(treasure_templates)]
                }
                locations.append(loc)
                print(f"🎲 Lieu généré : {loc['nom']}")
        
        return locations[:num_locations]

    def generate_game_image(self, game_title: str, genre: str, ambiance: str, universe_description: str) -> str:
        """
        Génère une description textuelle pour une image conceptuelle
        """
        prompt = f"""Crée une description détaillée pour une image conceptuelle de jeu vidéo intitulé "{game_title}".

Genre: {genre}
Ambiance: {ambiance}
Univers: {universe_description[:200]}

La description doit être visuelle et détaillée, incluant:
- Style artistique
- Éléments principaux
- Couleurs dominantes
- Composition de l'image

Description conceptuelle:"""

        image_description = self._call_api(prompt, max_tokens=300)
        return image_description.strip()

    def generate_and_save_image(self, game_title: str, genre: str, ambiance: str, universe_description: str) -> Dict:
        """
        Génère une vraie image avec Mistral Agents API (FLUX)
        """
        if not self.client or not self.image_agent:
            print("⚠️ Mode démo - génération d'image désactivée")
            description = self.generate_game_image(game_title, genre, ambiance, universe_description)
            return {
                'description': description,
                'image_data': None,
                'image_url': None
            }
        
        prompt = f"""Génère une image de cover art professionnelle pour le jeu vidéo "{game_title}".

Style: Cover art AAA, qualité cinématographique
Genre: {genre}
Ambiance: {ambiance}
Univers: {universe_description[:250]}

L'image doit être épique, immersive et capturer visuellement l'essence du jeu."""
        
        try:
            print(f"🎨 Génération d'image pour '{game_title}'...")
            
            response = self.client.beta.conversations.start(
                agent_id=self.image_agent.id,
                inputs=prompt
            )
            
            file_id = None
            from mistralai.models import ToolFileChunk
            
            if hasattr(response, 'outputs') and response.outputs:
                for output in response.outputs:
                    if hasattr(output, 'content'):
                        for chunk in output.content:
                            if isinstance(chunk, ToolFileChunk):
                                file_id = chunk.file_id
                                print(f"✅ Image générée avec file_id: {file_id}")
                                break
                        if file_id:
                            break
            
            if file_id:
                print(f"⬇️ Téléchargement de l'image...")
                file_bytes = self.client.files.download(file_id=file_id).read()
                print(f"✅ Image téléchargée ({len(file_bytes)} bytes)")
                
                return {
                    'description': prompt,
                    'image_data': ContentFile(file_bytes),
                    'image_url': None
                }
            else:
                print("⚠️ Aucune image générée dans la réponse")
                description = self.generate_game_image(game_title, genre, ambiance, universe_description)
                return {
                    'description': description,
                    'image_data': None,
                    'image_url': None
                }
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération d'image: {e}")
            description = self.generate_game_image(game_title, genre, ambiance, universe_description)
            return {
                'description': description,
                'image_data': None,
                'image_url': None
            }

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
