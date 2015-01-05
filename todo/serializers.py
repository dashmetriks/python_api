from rest_framework import serializers
from todo.models import Todo, Game, Player, GameWeek, UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
#    games = serializers.HyperlinkedRelatedField(many=True, view_name='game-detail')
    class Meta:
        model = User
        #fields = ('username', 'email', 'groups')
        fields = ('username',)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'description','done') 

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','description','done') 

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id','game') 


class PlayerSerializer2(serializers.HyperlinkedModelSerializer):
    game = GameSerializer(source='game')
    class Meta:
        model = Player
        fields = ('id','game') 

class GamesPlayerSerializer(serializers.ModelSerializer):
    game = GameSerializer(source='game')
    users = UserSerializer(source='owner')
    class Meta:
        model = Player
        fields = ('game','users') 

class GameWeekSerializer(serializers.ModelSerializer):
    #users = UserSerializer(source='owner')
    class Meta:
        model = GameWeek
        fields = ('id', 'game','week', 'inorout') 

class GameWeekSerializer2(serializers.ModelSerializer):
    users = UserSerializer(source='owner')
    class Meta:
        model = GameWeek
        fields = ('id', 'game','week', 'inorout', 'users') 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('gender', 'city','phone') 
