from django.conf.urls import patterns, include, url
from todo import views
from rest_framework import viewsets, routers


urlpatterns = patterns('',
    # Registration of new users
    url(r'^register/$', views.RegistrationView.as_view()),

    # Todos endpoint

    url(r'^imageUpload', views.FileUploadView.as_view()),
    url(r'^api/photo/$', views.PhotoList.as_view(), name='myphoto-list'),
    url(r'^api/photo/(?P<pk>[0-9]+)/$', views.PhotoDetail.as_view(), name='myphoto-detail'),
    url(r'^mygames/$', views.PlayersView.as_view()),
    url(r'^games/$', views.GamesView.as_view()),
    #url(r'^gameweek/$', views.GameUsersView.as_view()),
    url(r'^gameweek/(?P<game_id>[0-9]*)$', views.GameUsersView.as_view()),
    url(r'^content/(?P<game_id>[0-9]*)$', views.ContentView.as_view()),
    #url(r'^gamemail/(?P<game_id>[0-9]*)$', views.GameEmailView.as_view()),
    url(r'^gamestatus/(?P<gstatus_id>[0-9]*)$', views.GameStatusView.as_view()),
    url(r'^gamemail/(?P<gstatus_id>[0-9]*)$', views.GameEmailView.as_view()),
    url(r'^ugamestatus/(?P<game_id>[0-9]*)$', views.UserGameStatusView.as_view()),
#    url(r'^todos/$', views.TodosView.as_view()),
   # url(r'^user/$', views.UserProfileView.as_view()),
    url(r'^currentuser/$', views.CurrentUserView.as_view()),
    url(r'^currentuser2/$', views.UserView.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    #url(r'^user/$', views.UserView.as_view()),
#    url(r'^todos/(?P<todo_id>[0-9]*)$', views.TodosView.as_view()),
    url(r'^games/(?P<game_id>[0-9]*)$', views.GamesPlayerView.as_view()),

    # API authentication
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^api-auth/', include('rest_framework.urls',\
        namespace='rest_framework')),
)

