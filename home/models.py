from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name="Юзер", on_delete=models.CASCADE)
    birthday = models.DateField()
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.user.username} {self.available}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.user.username}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to='media', blank=True)
    likes = models.ManyToManyField(Like, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return self.title

