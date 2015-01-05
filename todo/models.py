from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    owner = models.ForeignKey(User)
    description = models.CharField(max_length=30)
    done = models.BooleanField()
    updated = models.DateTimeField(auto_now_add=True)

class Game(models.Model):
    description = models.CharField(max_length=30)
    done = models.BooleanField()
    updated = models.DateTimeField(auto_now_add=True)
    def __unicode__(self): 
	return self.description

class Player(models.Model):
    owner = models.ForeignKey(User)
    game = models.ForeignKey(Game)
   
class GameWeek(models.Model):
    owner = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    week = models.CharField(max_length=30)
    inorout = models.CharField(max_length=30)
    #game = models.CharField(max_length=30)
#    description = models.CharField(max_length=30)
#    done = models.BooleanField()
#    updated = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
        GENDERS = (
            ('male', 'Male'),
            ('female', 'Female')
        )
        user = models.OneToOneField(User, unique=True)
        gender = models.CharField(max_length=20, null=True, blank=True,
                                  choices=GENDERS)
        city = models.CharField(max_length=250, null=True, blank=True)
        dob = models.DateField(blank=True, null=True)
        locale = models.CharField(max_length=10, blank=True, null=True)
        phone = models.CharField(max_length=20, blank=True, null=True)
        phone_choice = models.CharField(max_length=10, blank=True, null=True)
        email_choice = models.CharField(max_length=10, blank=True, null=True)
#        def __unicode__(self):
#            return u'%s profile' % self.user.username

