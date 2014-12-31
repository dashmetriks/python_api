from datetime import datetime


# Django
from django.shortcuts import render
from django.contrib.auth.models import User

# REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Provider OAuth2
from provider.oauth2.models import Client

# Todo App
from todo.serializers import RegistrationSerializer
from todo.serializers import UserSerializer, TodoSerializer, GameSerializer,GamesPlayerSerializer , PlayerSerializer, PlayerSerializer2,GameWeekSerializer,GameWeekSerializer2
from todo.models import Todo, Game, Player, GameWeek


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistrationView(APIView):
    """ Allow registration of new users. """
    permission_classes = ()

    def post(self, request):
        serializer = RegistrationSerializer(data=request.DATA)

        # Check format and unique constraint
        if not serializer.is_valid():
            return Response(serializer.errors,\
                            status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        u = User.objects.create(username=data['username'])
        u.set_password(data['password'])
        u.save()

        # Create OAuth2 client
        name = u.username
        client = Client(user=u, name=name, url='' + name,\
                client_id=name, client_secret='', client_type=1)
        client.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TodosView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ Get all todos """
        todos = Todo.objects.filter(owner=request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Adding a new todo. """
        serializer = TodoSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            owner = request.user
            t = Todo(owner=owner, description=data['description'], done=False)
            t.save()
            request.DATA['id'] = t.pk # return id
            return Response(request.DATA, status=status.HTTP_201_CREATED)

    def put(self, request, todo_id):
        """ Update a todo """
        serializer = TodoSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            desc = data['description']
            done = data['done']
            t = Todo(id=todo_id, owner=request.user, description=desc,\
                     done=done, updated=datetime.now())
            t.save()
            return Response(status=status.HTTP_200_OK)


class GamesPlayerView(APIView):
    permission_classes = ()

    def get(self, request, game_id):
        """ Get all todos """
        todos = Player.objects.filter(game=game_id)
       # todos = Player.objects.filter(owner=game_id)
#        import pdb; pdb.set_trace()
        serializer = GamesPlayerSerializer(todos, many=True)
        return Response(serializer.data)

class GamesView(APIView):
    permission_classes = ()

    def get(self, request):
        """ Get all todos """
        todos = Game.objects.all()
        serializer = GameSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Adding a new todo. """
        serializer = GameSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            #owner = request.user
            t = Game( description=data['description'], done=False)
            t.save()
            request.DATA['id'] = t.pk # return id
            return Response(request.DATA, status=status.HTTP_201_CREATED)

    def put(self, request, todo_id):
        """ Update a todo """
        serializer = TodoSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            desc = data['description']
            done = data['done']
            t = Todo(id=todo_id, owner=request.user, description=desc,\
                     done=done, updated=datetime.now())
            t.save()
            return Response(status=status.HTTP_200_OK)

class PlayersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ Get all todos """
        players = Player.objects.filter(owner=request.user.id)
        serializer = PlayerSerializer2(players, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Adding a new todo. """
        serializer = PlayerSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            owner = request.user
            game1 = Game.objects.get(id=data['game'])
            t = Player(owner=owner, game=game1)
            t.save()
            request.DATA['id'] = t.pk # return id
            return Response(request.DATA, status=status.HTTP_201_CREATED)

class GameWeekView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ Get all todos """
        players = GameWeek.objects.all()
        #players = GameWeek.objects.filter(owner=request.user.id)
        serializer = GameWeekSerializer2(players, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Adding a new todo. """
        serializer = GameWeekSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors, status=
                status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            owner = request.user
            game1 = Game.objects.get(id=data['game'])
            week = data['week']
            inorout = data['inorout']
            t = GameWeek(owner=owner, game=game1,week=week,inorout=inorout)
            t.save()
            request.DATA['id'] = t.pk # return id
            return Response(request.DATA, status=status.HTTP_201_CREATED)
