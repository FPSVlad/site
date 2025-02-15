# news/models.py
from django.db import models
from ckeditor.fields import RichTextField

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()  # Используем CKEditor для текстового поля
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)  # Поле для загрузки изображения
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, related_name='news', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
