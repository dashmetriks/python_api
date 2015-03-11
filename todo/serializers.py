from rest_framework import serializers
from todo.models import Todo, Game, Player, GameUsers, Profile, Content, MyPhoto
from django.contrib.auth.models import User
from PIL import Image

#class PhotoSerializer(serializers.HyperlinkedModelSerializer):

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('city','phone_choice','email_choice','profile_pic')
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
        
#        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        try:
          user_profile = Profile.objects.get(user=instance)
        except Profile.DoesNotExist:
             Profile.objects.create(user=instance, **profile_data)
       # if not instance.profile:
        instance.profile.city = profile_data.get('city', instance.profile.city)
#        import pdb; pdb.set_trace()
        instance.profile.phone_choice = profile_data.get('phone_choice', instance.profile.phone_choice)
        instance.profile.email_choice = profile_data.get('email_choice', instance.profile.email_choice)
        #instance.profile.city = validated_data.get('city', instance.profile.city)
#        import pdb; pdb.set_trace()
        instance.save()
        instance.profile.save()

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
    class Meta:
        model = GameUsers
        fields = ('email_choice', 'gstatus' , 'id', 'game_id' ) 

class GameEmailPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUsers
        fields = ('gstatus', 'email_choice' , 'id', 'game_id' ) 

class GameUsersSerializer2(serializers.ModelSerializer):
    users = UserSerializer(source='user')
    class Meta:
        model = GameUsers
        fields = ('id', 'game_id','gstatus', 'user', 'users','email_choice') 

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('gender', 'city','phone') 

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('verbiage','game_id') 


class Base64ImageFieldxx(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
                #decoded_file = base64.urlsafe_b64decode(data)
            except TypeError:
                import pdb; pdb.set_trace()
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class Base64ImageField(serializers.ImageField):
    """ Django-rest-framework field for base64 encoded image data. """
    def from_native(self, base64_data):
        import pdb; pdb.set_trace()
        if isinstance(base64_data, basestring):
            # Strip data header if it exists
            base64_data = re.sub(r"^data\:.+base64\,(.+)$", r"\1", base64_data)

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except TypeError:
                msg = "Please upload a valid image."
                raise serializers.ValidationError(msg)

            # Get the file name extension:
            extension = imghdr.what("file_name", decoded_file)
            if extension not in ("jpeg", "jpg", "png"):
                msg = "{0} is not a valid image type.".format(extension)
                raise serializers.ValidationError(msg)

            extension = "jpg" if extension == "jpeg" else extension
            file_name = ".".join([str(uuid.uuid4()), extension])
            data = ContentFile(decoded_file, name=file_name)

        return super(Base64ImageField, self).from_native(data)

class PhotoSerializerxx(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyPhoto
        fields = ('url', 'id', 'image')
#        owner = serializers.Field(source='owner.username')

class PhotoSerializer(serializers.ModelSerializer):
#    image = Base64ImageField(
##        max_length=None, use_url=True,
#    )
    class Meta:
        model = MyPhoto
      #  fields = ('image',)
        fields = ( 'id', 'image', 'verbiage')
        #owner = serializers.Field(source='owner.username')

