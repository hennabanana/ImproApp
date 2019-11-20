"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


from .api.views import index_view, TaskViewSet, ActorViewSet, DirectorViewSet, UserViewSet, ActorList, UserList, GameList, TaskList, GameViewSet, SpectatorViewSet, login, register, getUserByToken, createSpectator

#Viewsets werden registriert
router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('actors', ActorViewSet)
router.register('spectators', SpectatorViewSet)
router.register('games', GameViewSet)
router.register('directors', DirectorViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    #die oben genannten Router Urls werden eigebunden
    path('api/', include(router.urls)),
    #falls nur die URL ohne Ressourcen aufgerufen wird, wird index aufgerufen    
    path('', index_view, name='index'),
    #Egal ob Actor oder Director, die selbe Methode wird aufgerufen
    path('director/api/login', login),    
    path('actor/api/login', login),
    path('director/api/register', register),
    path('actor/api/register', register),
    #View Methode createSpectator und getUserByToken wird aufgerufen
    path('api/createSpectator', createSpectator),
    path('api/getUserByToken', getUserByToken),
    #Pfad zur Admin Seite von Django
    path('api/admin/', admin.site.urls),
    #<game> steht für eine Variable die übergeben wird bsp: api/actors/game/1
    path('api/actors/game/<game>', ActorList.as_view()),
    #<game> steht für eine Variable die übergeben wird bsp: api/tasks/game/1
    path('api/tasks/game/<game>', TaskList.as_view()),
    #Aufruf ohne Parameter
    path('api/user/', UserList.as_view()),
]


