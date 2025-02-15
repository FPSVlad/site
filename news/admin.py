from django.contrib import admin
from .models import Topic, News

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_at')
