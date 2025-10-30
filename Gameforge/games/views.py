from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Game, Universe, Scenario, Character, Location, ConceptArt, Favorite, GenerationLimit
from .forms import GameCreationForm
from .ai_service import AIService


def home(request):
    """Page d'accueil avec tous les jeux publics"""
    games = Game.objects.filter(est_public=True)
    
    # Recherche
    query = request.GET.get('q')
    if query:
        games = games.filter(
            Q(titre__icontains=query) | 
            Q(genre__icontains=query) |
            Q(mots_cles__icontains=query)
        )
    
    return render(request, 'games/home.html', {'games': games, 'query': query})


def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer les limites de génération pour ce nouvel utilisateur
            GenerationLimit.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Compte créé avec succès!')
            return redirect('games:home')
    else:
        form = UserCreationForm()
    return render(request, 'games/register.html', {'form': form})


def user_login(request):
    """Connexion utilisateur"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username}!')
                return redirect('games:home')
    else:
        form = AuthenticationForm()
    return render(request, 'games/login.html', {'form': form})


def user_logout(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, 'Déconnexion réussie.')
    return redirect('games:home')


@login_required
def dashboard(request):
    """Tableau de bord personnel"""
    my_games = Game.objects.filter(createur=request.user)
    return render(request, 'games/dashboard.html', {'my_games': my_games})

def game_detail(request, game_id):
    """Détails d'un jeu"""
    game = get_object_or_404(Game, id=game_id)
    
    # Vérifier si l'utilisateur a accès
    if not game.est_public and game.createur != request.user:
        messages.error(request, 'Ce jeu est privé.')
        return redirect('games:home')
    
    # Vérifier si l'utilisateur a liké ce jeu
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, game=game).exists()
    
    context = {
        'game': game,
        'is_favorited': is_favorited,
    }
    return render(request, 'games/game_detail.html', context)

@login_required
def create_game(request):
    """Créer un nouveau jeu avec l'IA"""
    # Vérifier les limites
    limit, created = GenerationLimit.objects.get_or_create(user=request.user)
    
    if not limit.can_generate():
        messages.error(request, f'Vous avez atteint la limite de {limit.daily_count} générations par jour. Réessayez demain!')  # ✅ Changé max_daily en daily_count
        return redirect('games:dashboard')
    
    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            genre = form.cleaned_data['genre']
            ambiance = form.cleaned_data['ambiance']
            mots_cles = form.cleaned_data['mots_cles']
            references = form.cleaned_data.get('references', '')
            est_public = form.cleaned_data['est_public']
            
            # Initialiser le service IA
            ai_service = AIService()
            
            try:
                # Générer le titre
                keywords_list = [k.strip() for k in mots_cles.split(',') if k.strip()]
                titre = ai_service.generate_game_title(genre, ambiance, keywords_list)
                
                # Créer le jeu
                game = Game.objects.create(
                    titre=titre,
                    genre=genre,
                    ambiance=ambiance,
                    mots_cles=mots_cles,
                    references=references,
                    createur=request.user,
                    est_public=est_public
                )
                
                # Générer l'univers
                universe_data = ai_service.generate_universe(titre, genre, ambiance, mots_cles)
                Universe.objects.create(
                    game=game,
                    description=universe_data['description'],
                    style_graphique=universe_data['style_graphique'],
                    type_monde=universe_data['type_monde']
                )
                
                # Générer le scénario
                scenario_data = ai_service.generate_scenario(titre, universe_data['description'], genre)
                Scenario.objects.create(
                    game=game,
                    acte_1=scenario_data['acte_1'],
                    acte_2=scenario_data['acte_2'],
                    acte_3=scenario_data['acte_3'],
                    twist=scenario_data['twist']
                )
                
                # Générer les personnages
                characters_data = ai_service.generate_characters(titre, genre, 3)
                for char_data in characters_data:
                    Character.objects.create(
                        game=game,
                        nom=char_data['nom'],
                        classe=char_data.get('classe', 'guerrier'),
                        role=char_data.get('role', 'allie'),
                        background=char_data['background'],
                        gameplay_description=char_data.get('gameplay_description', '')
                    )
                
                # Générer les lieux
                locations_data = ai_service.generate_locations(titre, universe_data['description'], 4)
                for loc_data in locations_data:
                    Location.objects.create(
                        game=game,
                        nom=loc_data['nom'],
                        description=loc_data['description']
                    )
                image_result = ai_service.generate_and_save_image(
                    titre, genre, ambiance, universe_data['description']
                )

                concept_art = ConceptArt.objects.create(
                    game=game,
                    description=image_result['description'],
                    type_art="cover"
                )

                # Sauvegarder l'image si elle a été générée
                if image_result.get('image_data'):
                    concept_art.image.save(f"{game.id}_cover.png", image_result['image_data'], save=True)
                    messages.success(request, f'Jeu "{titre}" créé avec image générée!')
                else:
                    messages.success(request, f'Jeu "{titre}" créé (image en mode démo)!')
                # Incrémenter le compteur
                limit.increment()
                
                messages.success(request, f'Jeu "{titre}" créé avec succès!')
                return redirect('games:game_detail', game_id=game.id)
                
            except Exception as e:
                messages.error(request, f'Erreur lors de la génération: {str(e)}')
                return redirect('games:create_game')
    else:
        form = GameCreationForm()
    
    context = {
        'form': form,
        'remaining_generations': limit.daily_count - limit.generations_today
    }
    return render(request, 'games/create_game.html', context)


@login_required
def create_random_game(request):
    """Créer un jeu complètement aléatoire"""
    limit, created = GenerationLimit.objects.get_or_create(user=request.user)
    
    if not limit.can_generate():
        messages.error(request, f'Vous avez atteint la limite de {limit.daily_count} générations par jour. Réessayez demain!')  # ✅ Changé max_daily en daily_count
        return redirect('games:dashboard')
    
    ai_service = AIService()
    
    # Générer des paramètres aléatoires
    params = ai_service.generate_random_game_params()
    
    try:
        # Générer le jeu
        keywords_list = [k.strip() for k in params['keywords'].split(',')]
        titre = ai_service.generate_game_title(params['genre'], params['ambiance'], keywords_list)
        
        game = Game.objects.create(
            titre=titre,
            genre=params['genre'],
            ambiance=params['ambiance'],
            mots_cles=params['keywords'],
            createur=request.user,
            est_public=True
        )
        
        # Générer le contenu
        universe_data = ai_service.generate_universe(titre, params['genre'], params['ambiance'], params['keywords'])
        Universe.objects.create(
            game=game,
            description=universe_data['description'],
            style_graphique=universe_data['style_graphique'],
            type_monde=universe_data['type_monde']
        )
        
        scenario_data = ai_service.generate_scenario(titre, universe_data['description'], params['genre'])
        Scenario.objects.create(
            game=game,
            acte_1=scenario_data['acte_1'],
            acte_2=scenario_data['acte_2'],
            acte_3=scenario_data['acte_3'],
            twist=scenario_data['twist']
        )
        
        characters_data = ai_service.generate_characters(titre, params['genre'], 3)
        for char_data in characters_data:
            Character.objects.create(
                game=game,
                nom=char_data['nom'],
                classe=char_data.get('classe', 'guerrier'),
                role=char_data.get('role', 'allie'),
                background=char_data['background']
            )
        
        locations_data = ai_service.generate_locations(titre, universe_data['description'], 4)
        for loc_data in locations_data:
            Location.objects.create(
                game=game,
                nom=loc_data['nom'],
                description=loc_data['description']
            )
        
        limit.increment()
        
        messages.success(request, f'Jeu aléatoire "{titre}" créé!')
        return redirect('games:game_detail', game_id=game.id)
        
    except Exception as e:
        messages.error(request, f'Erreur: {str(e)}')
        return redirect('games:dashboard')


@login_required
def delete_game(request, game_id):
    """Supprimer un jeu (auteur uniquement)"""
    game = get_object_or_404(Game, id=game_id)
    
    if game.createur != request.user:
        messages.error(request, 'Vous ne pouvez pas supprimer ce jeu.')
        return redirect('games:game_detail', game_id=game_id)
    
    if request.method == 'POST':
        titre = game.titre
        game.delete()
        messages.success(request, f'Jeu "{titre}" supprimé.')
        return redirect('games:dashboard')
    
    return render(request, 'games/confirm_delete.html', {'game': game})


@login_required
def toggle_favorite(request, game_id):
    """Ajouter/retirer un jeu des favoris"""
    game = get_object_or_404(Game, id=game_id)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, game=game)
    
    if created:
        game.likes_count += 1
        game.save()
        messages.success(request, f'"{game.titre}" ajouté aux favoris!')
    else:
        favorite.delete()
        game.likes_count -= 1
        game.save()
        messages.info(request, f'"{game.titre}" retiré des favoris.')
    
    return redirect('games:game_detail', game_id=game_id)


@login_required
def favorites(request):
    """Liste des jeux favoris"""
    favorite_games = Game.objects.filter(favorited_by__user=request.user)
    return render(request, 'games/favorites.html', {'games': favorite_games})