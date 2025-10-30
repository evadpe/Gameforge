from django.urls import path
from . import views
app_name = 'games'
urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Authentification
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # CRUD Jeux
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/create/', views.create_game, name='create_game'),
    path('game/random/', views.create_random_game, name='create_random_game'),
    path('game/<int:game_id>/delete/', views.delete_game, name='delete_game'),
    
    # Favoris
    path('game/<int:game_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    
    # Page principale des paramètres
    path('settings/', views.settings, name='settings'),
    
    # Mise à jour du profil (email, date de naissance)
    path('settings/profile/', views.update_profile, name='update_profile'),
    
    # Changement de mot de passe
    path('settings/password/', views.change_password, name='change_password'),
    
    # Mise à jour des préférences (visibilité, notifications)
    path('settings/preferences/', views.update_preferences, name='update_preferences'),
    
    # Suppression du compte
    path('settings/delete/', views.delete_account, name='delete_account'),

    # Export PDF
    path('game/<int:game_id>/export/pdf/', views.export_game_pdf, name='export_game_pdf'),

]


