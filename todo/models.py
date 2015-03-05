from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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
   
class GameUsers(models.Model):
    user = models.ForeignKey(User)
    game_id = models.ForeignKey(Game)
    gstatus = models.CharField(max_length=30)
    email_choice = models.CharField(max_length=10, blank=True, null=True)
    #game = models.CharField(max_length=30)
#    description = models.CharField(max_length=30)
#    done = models.BooleanField()
#    updated = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
        GENDERS = (
            ('male', 'Male'),
            ('female', 'Female')
        )
        user = models.OneToOneField(User)
        gender = models.CharField(max_length=20, null=True, blank=True,
                                  choices=GENDERS)
        city = models.CharField(max_length=250, null=True, blank=True)
        dob = models.DateField(blank=True, null=True)
        locale = models.CharField(max_length=10, blank=True, null=True)
        phone = models.CharField(max_length=20, blank=True, null=True)
        phone_choice = models.CharField(max_length=10, blank=True, null=True)
        email_choice = models.CharField(max_length=10, blank=True, null=True)
        profile_pic = models.ImageField(upload_to='uploads/', null=True)
        woot = models.FileField()
#        def __unicode__(self):
#            return u'%s profile' % self.user.username

class Content(models.Model):
        user = models.ForeignKey(User)
        content_pic = models.ImageField(upload_to='uploads/', null=True)
        game_id = models.ForeignKey(Game)
        verbiage = models.CharField(max_length=500)
        updated = models.DateTimeField(auto_now_add=True)


class Company(models.Model):
    name=models.CharField(max_length=256, default='')
    user=models.ForeignKey(User)
    logo=models.ImageField()

    def __unicode__(self):
        return unicode(self.name)

class CompanyX(models.Model):
    name=models.CharField(max_length=256, default='')
    user=models.ForeignKey(User)
    logo=models.ImageField()
    profile_pic = models.ImageField(upload_to='uploads/', null=True)

    def __unicode__(self):
        return unicode(self.name)

class MyPhoto(models.Model):
    #owner = models.ForeignKey('auth.User', related_name='image')
    owner = models.ForeignKey(User)
    image = models.ImageField(upload_to='/Users/toms/Downloads/django-todo-master-4/uploads/', max_length=254)
