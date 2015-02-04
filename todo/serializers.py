from rest_framework import serializers
from todo.models import Todo, Game, Player, GameUsers, Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('city',)
        #read_only_fields = ('city',)
#        exclude = ('user',)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
       model = User
       fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile' )
       #fields = ('id', 'username', 'first_name', 'last_name', 'email', )

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        
        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        if not instance.profile:
            Profile.objects.create(user=instance, **profile_data)
        instance.profile.city = profile_data.get('city', instance.profile.city)
        #instance.profile.city = validated_data.get('city', instance.profile.city)
        import pdb; pdb.set_trace()
        instance.save()
        profile.save()

        return instance


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
        model = Profile
        fields = ('gender', 'city','phone') 
