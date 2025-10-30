from django.contrib import admin
from .models import Game, Universe, Scenario, Character, Location, ConceptArt, Favorite, GenerationLimit


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('titre', 'genre', 'ambiance', 'createur', 'est_public', 'likes_count', 'date_creation')
    list_filter = ('genre', 'ambiance', 'est_public', 'date_creation')
    search_fields = ('titre', 'mots_cles', 'createur__username')
    date_hierarchy = 'date_creation'


@admin.register(Universe)
class UniverseAdmin(admin.ModelAdmin):
    list_display = ('game', 'style_graphique', 'type_monde')
    list_filter = ('style_graphique', 'type_monde')


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('game',)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('nom', 'game', 'classe', 'role')
    list_filter = ('classe', 'role')
    search_fields = ('nom', 'game__titre')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'game')
    search_fields = ('nom', 'game__titre')


@admin.register(ConceptArt)
class ConceptArtAdmin(admin.ModelAdmin):
    list_display = ('game', 'type_art', 'date_creation')
    list_filter = ('type_art', 'date_creation')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'date_added')
    list_filter = ('date_added',)


@admin.register(GenerationLimit)
class GenerationLimitAdmin(admin.ModelAdmin):
    list_display = ['user', 'generations_today', 'daily_count', 'last_reset'] 
    list_filter = ['last_reset']
    search_fields = ['user__username']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')