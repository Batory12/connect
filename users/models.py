from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    followers = models.ManyToManyField("self")
    following = models.ManyToManyField("self")
    bio = models.TextField()
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

