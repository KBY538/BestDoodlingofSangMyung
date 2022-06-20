from django.db import models

# Create your models here.
class GeneratedPicture(models.Model):
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'self.title'