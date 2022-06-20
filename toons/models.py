from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/toon/category/{self.slug}'

class DisplayType(models.Model):
    name = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

def rep_thumbnail_path(instance, filename):
    return 'toon/{0}/thumbnail/{1}'.format(instance.title, filename)

def thumbnail_path(instance, filename):
    return 'toon/{0}/{1}/thumbnails/{2}'.format(instance.get_title(),instance.episode, filename)

def images_path(instance, filename):
    return 'toon/{0}/{1}/{2}'.format(instance.toon.get_title(), instance.get_episode(), filename)

class Work(models.Model):
    title = models.CharField(max_length=30, unique=True) # 제목
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    author = models.ForeignKey(User, default=0, on_delete=models.SET_DEFAULT)
    rep_thumbnail = models.ImageField(upload_to=rep_thumbnail_path)
    description = models.TextField()  # 설명글

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    display = models.ForeignKey(DisplayType, on_delete=models.SET_DEFAULT, default=0)

    def get_absolute_url(self):
        return f'/toon/{self.slug}/'

    def get_display_type(self):
        return f'{self.display.name}'

    def __str__(self):
        return f'[{self.category}]{self.title}::{self.author}'

class Toon(models.Model):
    episode = models.IntegerField(null=False)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    hook = models.CharField(max_length=150)

    thumbnail = models.ImageField(upload_to=thumbnail_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.work.title}::{self.episode}'

    def get_title(self):
        return self.work.title

    def get_previous_episode(self):
        return self.episode-1

    def get_next_episode(self):
        return self.episode+1

    def get_absolute_url(self):
        return f'/toon/{self.work.slug}/{self.episode}'

    def get_previous_url(self):
        return f'/toon/{self.work.slug}/{self.episode-1}'

    def get_next_url(self):
        return f'/toon/{self.work.slug}/{self.episode+1}'

class ToonImage(models.Model):

    toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
    images = models.FileField(upload_to=images_path)

    def __str__(self):
        return f'[{self.toon.get_title()}]{self.toon.episode}'

    def get_episode(self):
        return self.toon.episode

class Comment(models.Model):
    toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.content}'

    def get_absolute_url(self):
        return f'{self.toon.get_absolute_url()}#comment-{self.pk}'