from rest_framework import serializers
from .models import Spectator, Task, Actor, User, Director, Game, User


from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

class UserSerializer(serializers.ModelSerializer):
        class Meta:
                model = get_user_model()
                # fiels gibt die eigenschaft an die seriasiert werden müssen
                fields = ['id', 'username', 'is_staff', 'groups']
                extra_kwargs = {
                        'username': {
                                'validators': [UnicodeUsernameValidator()],
                        }
                }


class DirectorSerializer(serializers.ModelSerializer):
        # userserializser wird für das User feld benötigt
        user = UserSerializer(many=False)
        class Meta:
                model = Director
                fields = ['id', 'user']

        

class GameSerializer(serializers.ModelSerializer):
        director = DirectorSerializer(many=False)
        class Meta:
                model = Game
                fields = ['id', 'name', 'duration', 'director', 'status']
        
        #Create-Methode überschrieben bei Create Aufruf von Game
        def create(self, validated_data):
                director_data = validated_data.pop('director')
                user_data = director_data.pop('user')
                username = user_data.pop('username')
                user = User.objects.get(username=username)
                director = Director.objects.get(user=user)
                duration = validated_data.pop('duration')
                gamename = validated_data.pop('name')
                game = Game.objects.create(director=director, duration=duration, name=gamename)
                game.save()
                return game


class SpectatorSerializer(serializers.ModelSerializer):
        user = UserSerializer(many=False)
        game = GameSerializer(many=False)
        class Meta:
                model = Spectator
                fields = ['id', 'user', 'game']


class ActorSerializer(serializers.ModelSerializer):
        user = UserSerializer(many=False)
        game = GameSerializer(many=False)
        class Meta:
                model = Actor
                fields = ['id', 'user', 'game']

        # Update-Methode überschrieben wenn Actor das Game gesetzt bekommt
        def update(self, instance, validated_data):
                user_data = validated_data.pop('user')
                username = user_data.pop('username')
                user = User.objects.get(username=username)
                actor = Actor.objects.get(user=user)

                game_data = validated_data.pop('game')
                name = game_data.pop('name')
                game = Game.objects.get(name=name)


                actor.game = game
                actor.save()
                return actor

class TaskSerializer(serializers.ModelSerializer):
        #Da Objekte von anderen Models übergeben werden,
        #benötigt der TaskSerializer auch den Game-, User-
        #und ActorSerializer
        game = GameSerializer(many=False)
        writer = UserSerializer(many=False)
        actors = ActorSerializer(many=True, required=False)

        #Meta legt fest welche Felder mit im JSON mitgesendet werden
        class Meta:
                model = Task
                fields = ['id', 'text', 'status', 'game', 'writer', 'actors']
        #Create Methode wird überschrieben, da der Standardserializer
        #keine M:N Beziehung serializiert
        def create(self, validated_data):
                #aus dem JSON werden die einzelnen Eigenschaften geholt
                text = validated_data.pop('text')
                status = validated_data.pop('status')
                game_data = validated_data.pop('game')
                gamename = game_data.pop('name')
                #anhand der gamedaten wird das game objekt geholt
                game = Game.objects.get(name=gamename)

                writer_data = validated_data.pop('writer')
                username = writer_data.pop('username')
                #anhand der Writer wird der Uer geholt
                writer = User.objects.get(username=username)


                actors_data = validated_data.pop('actors')

                #mit den bisher serialisierten Daten wird die Aufgabe estellt.
                task = Task.objects.create(text=text, status=status, writer=writer, game=game)
                #da mehrere Actors bei einer Task eingetragen sein können
                #wird über die Actors_data interriert und jder Actor der Task hinzugefügt
                for actor_data in actors_data:
                        user_data = actor_data.pop('user')
                        username = user_data.pop('username')
                        user = User.objects.get(username=username)
                        actor = Actor.objects.get(user=user)
                        task.actors.add(actor)
                #Das Objekt wird gespeichert, erst dann bekommt die Task eine ID
                task.save()
                #und zurückgesendet
                return task

        # Update-Methode überschrieben wenn Task umgedatet wird
        def update(self, instance, validated_data):
                instance.text = validated_data.pop('text')
                instance.status = validated_data.pop('status')
                game_data = validated_data.pop('game')
                gamename = game_data.pop('name')
                game = Game.objects.get(name=gamename)
                instance.game=game

                writer_data = validated_data.pop('writer')
                username = writer_data.pop('username')
                writer = User.objects.get(username=username)
                instance.writer=writer
                actors_data = validated_data.pop('actors')
                for actor_data in actors_data:
                        user_data = actor_data.pop('user')
                        username = user_data.pop('username')
                        user = User.objects.get(username=username)
                        actor = Actor.objects.get(user=user)
                        instance.actors.add(actor)

                instance.save()
                return instance

