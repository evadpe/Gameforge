from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime
from django.dispatch import receiver
from django.db.models.signals import post_save 

class Game(models.Model):
    """Modèle principal pour un jeu généré"""
    GENRE_CHOICES = [
        ('rpg', 'RPG'),
        ('action', 'Action'),
        ('aventure', 'Aventure'),
        ('strategie', 'Stratégie'),
        ('horror', 'Horreur'),
        ('sci-fi', 'Science-Fiction'),
        ('fantasy', 'Fantasy'),
        ('cyberpunk', 'Cyberpunk'),
    ]
    
    AMBIANCE_CHOICES = [
        ('sombre', 'Sombre'),
        ('joyeux', 'Joyeux'),
        ('mysterieux', 'Mystérieux'),
        ('epique', 'Épique'),
        ('humoristique', 'Humoristique'),
    ]
    
    titre = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    ambiance = models.CharField(max_length=50, choices=AMBIANCE_CHOICES)
    mots_cles = models.TextField(blank=True, help_text="Mots-clés séparés par des virgules")
    references = models.TextField(blank=True, help_text="Références culturelles")
    
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    est_public = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    
    # Compteurs
    likes_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        ordering = ['-date_creation']


class Universe(models.Model):
    """Modèle pour l'univers du jeu"""
    STYLE_CHOICES = [
        ('realiste', 'Réaliste'),
        ('cartoon', 'Cartoon'),
        ('pixel_art', 'Pixel Art'),
        ('anime', 'Anime'),
        ('low_poly', 'Low Poly'),
    ]
    
    TYPE_CHOICES = [
        ('open_world', 'Open World'),
        ('lineaire', 'Linéaire'),
        ('hub', 'Hub Central'),
        ('arene', 'Arène'),
    ]
    
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='universe')
    description = models.TextField()
    style_graphique = models.CharField(max_length=50, choices=STYLE_CHOICES, default='realiste')
    type_monde = models.CharField(max_length=50, choices=TYPE_CHOICES, default='open_world')
    
    def __str__(self):
        return f"Univers de {self.game.titre}"


class Scenario(models.Model):
    """Modèle pour le scénario en 3 actes"""
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='scenario')
    
    acte_1 = models.TextField(help_text="Introduction et mise en place")
    acte_2 = models.TextField(help_text="Développement et complications")
    acte_3 = models.TextField(help_text="Climax et résolution")
    twist = models.TextField(blank=True, help_text="Plot twist optionnel")
    
    def __str__(self):
        return f"Scénario de {self.game.titre}"


class Character(models.Model):
    """Modèle pour les personnages du jeu"""
    CLASSE_CHOICES = [
        ('guerrier', 'Guerrier'),
        ('mage', 'Mage'),
        ('voleur', 'Voleur'),
        ('archer', 'Archer'),
        ('healer', 'Soigneur'),
        ('tank', 'Tank'),
        ('support', 'Support'),
    ]
    
    ROLE_CHOICES = [
        ('heros', 'Héros Principal'),
        ('antagoniste', 'Antagoniste'),
        ('allie', 'Allié'),
        ('mentor', 'Mentor'),
        ('neutre', 'Neutre'),
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='characters')
    nom = models.CharField(max_length=100)
    classe = models.CharField(max_length=50, choices=CLASSE_CHOICES, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    background = models.TextField()
    gameplay_description = models.TextField(blank=True, help_text="Description du gameplay pour ce personnage")
    
    def __str__(self):
        return f"{self.nom} ({self.game.titre})"


class Location(models.Model):
    """Modèle pour les lieux emblématiques"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='locations')
    nom = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.nom} - {self.game.titre}"


class ConceptArt(models.Model):
    """Modèle pour les concept arts générés"""
    TYPE_CHOICES = [
        ('character', 'Personnage'),
        ('environment', 'Environnement'),
        ('item', 'Objet'),
        ('autre', 'Autre'),
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='concept_arts')
    image = models.ImageField(upload_to='concept_arts/')
    description = models.TextField()
    type_art = models.CharField(max_length=50, choices=TYPE_CHOICES, default='autre')
    date_creation = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Concept Art - {self.game.titre}"
    
    class Meta:
        ordering = ['-date_creation']


class Favorite(models.Model):
    """Modèle pour les favoris/likes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorited_by')
    date_added = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'game')
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.user.username} ♥ {self.game.titre}"

class Profile(models.Model):
    """Profil étendu de l'utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    default_visibility = models.CharField(
        max_length=10, 
        choices=[
            ('public', 'Public'), 
            ('private', 'Privé')
        ],
        default='public',
        verbose_name="Visibilité par défaut"
    )
    email_notifications = models.BooleanField(
        default=True,
        verbose_name="Notifications par email"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"
    
    def __str__(self):
        return f"Profil de {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil quand un utilisateur est créé"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil quand l'utilisateur est sauvegardé"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

class GenerationLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    generations_today = models.IntegerField(default=0)
    daily_count = models.IntegerField(default=5)  # Limite par défaut à 5
    last_reset = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # S'assurer que daily_count n'est jamais 0
        if self.daily_count <= 0:
            self.daily_count = 5
        super().save(*args, **kwargs)

    def can_generate(self):
        # Réinitialiser le compteur si c'est un nouveau jour
        if timezone.now().date() > self.last_reset:
            self.generations_today = 0
            self.last_reset = timezone.now().date()
            self.save()
        
        return self.generations_today < self.daily_count

    def increment(self):
        self.generations_today = models.F('generations_today') + 1
        self.save(update_fields=['generations_today'])

    def reset_limit(self):
        """Réinitialiser la limite manuellement"""
        self.generations_today = 0
        self.last_reset = timezone.now().date()
        self.save()

    def __str__(self):
        return f"Limite de {self.user.username}: {self.generations_today}/{self.daily_count}"
