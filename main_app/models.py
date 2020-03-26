from django.db import models
from django.contrib.auth.models import User


class Global(models.Model):
    name = models.CharField(max_length=100)
    infected = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    last_updated = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    infected = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-infected']


class Comment(models.Model):
    posted_at = models.DateTimeField()
    content = models.TextField(max_length=250)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.id} by {self.created_by.username}'

    class Meta:
        ordering = ['-posted_at']


class Province(models.Model):
    name = models.CharField(max_length=100)
    infected = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-infected']


class County(models.Model):
    name = models.CharField(max_length=100)
    infected = models.IntegerField()
    deaths = models.IntegerField()
    recovered = models.IntegerField()
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-infected']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.user.username}'s profile"
