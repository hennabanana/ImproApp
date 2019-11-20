from django.db import models
from django.contrib.auth.models import User

import datetime

#Model Klasse definiert die Obejekte

#Director Model
class Director(models.Model):
    #Durch die 1:1 Beziehung gehört 1 director genau zu einem  user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
#Dict für die verschiedenen Statis
Game_State=(
    (1, 'OPEN'),
    (2, 'RUNNING'),
    (3, 'OVER'),
)
class Game(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    status = models.CharField(max_length = 7, choices=Game_State, default=1)

class Spectator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Actor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)

Task_State=(
    (1, 'OPEN'),
    (2, 'SENT'),
    (3, 'PLAYED'),
)
class Task(models.Model):
    text = models.CharField(max_length=300, blank=False) 
    # als status können noch Task_state genommen werde
    status = models.CharField(max_length = 6, choices=Task_State, default=1)
    game = models.ForeignKey(Game, on_delete=models.CASCADE) # 1:N Beziehung mit dem Spiel
    writer = models.ForeignKey(User, on_delete=models.CASCADE) # 1:N Beziehunng mit dem Verfasser
    actors = models.ManyToManyField(Actor)# N:M Beziehung mit der Schauspieler

class Rating(models.Model):
    text = models.CharField(max_length=300)
    stars = models.IntegerField()
    spectator = models.ForeignKey(Spectator, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)






