from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets

from .models import Task, Spectator, Actor, Game, Director
from .serializer import TaskSerializer, SpectatorSerializer, ActorSerializer, GameSerializer, DirectorSerializer, UserSerializer
from django.contrib.auth.models import User, Group

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import generics
import string
import random



# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

#für den Aufruf muss man authtifiziert sein
@authentication_classes([])
@permission_classes([])
class UserViewSet(viewsets.ModelViewSet):
    #Die ModelViewSet-Klasse enthält die Implementierungen für verschiedene Aktionen
    # Methoden list(), retrieve(), create(), update(), partial_update() und destroy() sind automatisch implementiert
    queryset = User.objects.all()
    serializer_class = UserSerializer

@authentication_classes([])
@permission_classes([])
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SpectatorViewSet(viewsets.ModelViewSet):
    queryset = Spectator.objects.all()
    serializer_class = SpectatorSerializer


@authentication_classes([])
@permission_classes([])
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    #lookup gibt die Eigenschaft an die beim Api aufruf mitgegeben wird
    #standardmäßig ist es die ID, hier wurde es auf NAME gesetzt
    lookup_field = 'name'

@authentication_classes([])
@permission_classes([])
class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

@authentication_classes([])
@permission_classes([])
class ActorList(generics.ListAPIView):
    serializer_class = ActorSerializer
    # Bei Abfrage der Liste wird es auf das mitgegeben game gefilter
    def get_queryset(self):
        queryset = Actor.objects.all()
        game = self.kwargs['game']
        if game is not None:
            queryset = queryset.filter(game=game)
            return queryset

@authentication_classes([])
@permission_classes([])
class TaskList(generics.ListAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        #alle Aufgaben werden geholt
        queryset = Task.objects.all()
        #die uebergebene Variable wird ausgelesen
        game = self.kwargs['game']
        if game is not None:
            #die Aufgaben werden auf den Wert
            #in Game gefilter
            queryset = queryset.filter(game=game)
        return queryset

@authentication_classes([])
@permission_classes([])
class GameList(generics.ListAPIView):
    serializer_class = GameSerializer
    #auch hier werden die Listen auf den übergebenen Parameter gefiltert
    def get_queryset(self):
        queryset = Game.objects.all()
        if 'director' in self.kwargs:
            director = self.kwargs['director']
            return Game.objects.filter(director=director)[:1]

        if 'actor' in self.kwargs:
            actor = self.kwargs['actor']
            game = Actor.objects.filter(actor=actor).game
            return Game.objects.filter(actor=actor)[:1]
        
        return queryset

@authentication_classes([])
@permission_classes([])
class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

@authentication_classes([])
@permission_classes([])
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


@csrf_exempt
@api_view(["POST"])# akzeptiert nur POST
@permission_classes([])
# Methode um anhand des Tokens den User zu bekommen
def getUserByToken(request):
    #Token wird aus dem Request gezogen
    token_request = request.data.get("token")
    # token wird geholt
    token = Token.objects.get(key=token_request)
    # es wird geprüft ob es ein Director ist
    is_director = token.user.is_staff
    # es wird gesucht welcher Gruppe der user zugehörig ist
    if token.user.groups.filter(name = "directors").exists():
        #Director wird geholt
        director = Director.objects.get(user=token.user)
        # director wird serializsiert
        directorSerializer = DirectorSerializer(director, many=False)
        try:
            #game des directors wird geholt
            game = Game.objects.get(director=director.id, status=1)
            # game wird serializsiert
            gameSerializer = GameSerializer(game, many=False)
            # antwort wird mit Daten an Server gesendet 
            return Response({'group':'directors','token': token.key, 'director':directorSerializer.data, 'game':gameSerializer.data}, status=HTTP_200_OK)
        except:
            return Response({'group':'directors','token': token.key, 'director':directorSerializer.data}, status=HTTP_200_OK)
    if token.user.groups.filter(name = "actors").exists():
        actor = Actor.objects.get(user=token.user)
        actorSerializer = ActorSerializer(actor, many=False)
        return Response({'group':'actors','token': token.key, 'actor':actorSerializer.data}, status=HTTP_200_OK)

    if token.user.groups.filter(name = "spectators").exists():
        spectator = Spectator.objects.get(user=token.user)
        spectatorSerializer = SpectatorSerializer(spectator, many=False)
        return Response({'group':'spectators','token': token.key, 'spectator':spectatorSerializer.data}, status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)


@csrf_exempt#Cross Site Request Forgery protection¶
@api_view(["POST"])#Nur POST-Methoden erlaubt
@permission_classes((AllowAny,))#permission_class bestimmt ob nur eingeloggte User oder jeder die View aufrufen kann
def login(request):
    #user und password aus der Request geholt
    username = request.data.get("username")#
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    #user wird authentifiziert
    user = authenticate(username=username, password=password)
    # wenn user leer, authetifizierung fehlgeschlagen
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    #prüfung ob director
    is_director = user.is_staff
    #user wird serializiert
    userSerializer = UserSerializer(user, many=False)
    #wenn director gib director daten zurück
    if is_director:
        director = Director.objects.get(user=user)
        directorSerializer = DirectorSerializer(director, many=False)
        try:
            game = Game.objects.get(director=director.id, status=1)
            gameSerializer = GameSerializer(game, many=False)
            return Response({'is_director':is_director,'token': token.key, 'director':directorSerializer.data, 'game':gameSerializer.data}, status=HTTP_200_OK)
        except:
            return Response({'is_director':is_director,'token': token.key, 'director':directorSerializer.data}, status=HTTP_200_OK)

    else:
        actor = Actor.objects.get(user=user)
        actorSerializer = ActorSerializer(actor, many=False)
        return Response({'is_director':is_director,'token': token.key, 'actor':actorSerializer.data}, status=HTTP_200_OK)


#registieriung eines users
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    # variable ob es ein director ist oder nicht
    isdirector = request.data.get("register_director")
    if not username and not password:
        return Response({"message": "username, password is required to register a user"}, status=HTTP_400_BAD_REQUEST)
    if not isdirector:
        #wenn actor dann erstelle oder hole dir gruppe und füge hinzu
        actors, created = Group.objects.get_or_create(name='actors')
        new_user = User.objects.create_user(username=username, password=password, email="null")
        actor = Actor(user=new_user)
        actor.save()
        new_user.groups.add(actors)
        actors.save()
        new_user.save()
        #user wird zurück gegeben
        return Response({'is_director':False,'user':new_user.id}, status=HTTP_201_CREATED)
    else:
        directors, created = Group.objects.get_or_create(name='directors')
        new_user = User.objects.create_user(username=username, password=password, email="null", is_staff=True)
        director = Director(user=new_user)
        director.save()
        new_user.groups.add(directors)
        directors.save()
        new_user.save()
        return Response({'is_director':True,'user':new_user.id}, status=HTTP_201_CREATED)
    return Response(status=HTTP_400_BAD_REQUEST)

#methode wird für den zufallsnamen des zuschauers verwendet
def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
# Beim Spectator Login wird ein User erstellt, eingeloggt und einem Spiel hinzugefügt
# und der Token zurück gegeben
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def createSpectator(request):

    gameid = request.data.get("game")
    game = Game.objects.get(id=gameid)
    gameSerializer = GameSerializer(game, many=False)
    #random username und password wird generiert
    username=randomString()
    password=randomString()
    # spectator gruppe wird geholt oder erstellt
    spectators, created = Group.objects.get_or_create(name='spectators')
    new_user = User.objects.create_user(username=username, password=password)
    new_user.save()
    spectator = Spectator(user=new_user, game=game)
    spectator.save()
    new_user.groups.add(spectators)
    spectators.save()
    new_user.save()
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    userSerializer = UserSerializer(user, many=False)
    spectatorSerializer = SpectatorSerializer(spectator, many=False)
    try:
        return Response({'token': token.key, 'spectator':spectatorSerializer.data, 'game':gameSerializer.data}, status=HTTP_200_OK)
    except:
        return Response({'token': token.key, 'spectator':spectatorSerializer.data}, status=HTTP_200_OK)
    return Response(status=HTTP_200_OK)



