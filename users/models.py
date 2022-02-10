from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    
class ArtistData(models.Model):
    image = CloudinaryField('image',null=True) 
    name = models.CharField(max_length=1255,null=True)
    spotify = models.CharField(max_length=10255,null=True)
    applemusic = models.CharField(max_length=10255,null=True)
    youtube = models.CharField(max_length=10255,null=True)
    tiktok = models.CharField(max_length=10255,null=True)
    def __str__(self):
        return self.name 
    
    def save_artist(self):
        self.save()