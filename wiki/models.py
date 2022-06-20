from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from markdownx.models import MarkdownxField
from toons.models import Work

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True, unique=True)
    content = MarkdownxField()  # TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    # methods
    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/wiki/{self.pk}/'

    def get_markdown_content(self):
        return markdown(self.content)  # markdown의 markdown
