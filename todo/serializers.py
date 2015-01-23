from rest_framework import serializers
from todo.models import Todo, Game, Player, GameUsers, UserProfile
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

class GameUsersSerializer(serializers.ModelSerializer):
  #  user = UserSerializer(source='owner')
    class Meta:
        model = GameUsers
        fields = ( 'gstatus' , 'id' , 'game_id') 

class GameUsersPutSerializer(serializers.ModelSerializer):
  #  user = UserSerializer(source='owner')
#    import pdb; pdb.set_trace()
    class Meta:
        model = GameUsers
        #fields = ( 'gstatus' , 'id') 
        fields = ( 'gstatus' , 'id', 'game_id' ) 

class GameUsersSerializer2(serializers.ModelSerializer):
    users = UserSerializer(source='user')
    class Meta:
        model = GameUsers
        fields = ('id', 'game_id','gstatus', 'user', 'users') 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('gender', 'city','phone') 
