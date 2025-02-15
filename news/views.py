from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Topic, News
from sendfile import sendfile
from .forms import NewsForm

# Представление для обслуживания медиафайлов
def serve_media(request, path):
    # Это представление будет служить медиафайлы
    # Убедитесь, что в настройках Django правильно указан MEDIA_ROOT и MEDIA_URL
    media_file_path = settings.MEDIA_ROOT / path
    return sendfile(request, media_file_path)

# Представление для главной страницы
def home(request):
    topics = Topic.objects.all()  # Получаем все темы
    return render(request, 'news/home.html', {'topics': topics})

# Представление для списка всех тем
def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'news/topic_list.html', {'topics': topics})

# Представление для подробностей темы
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    news = News.objects.filter(topic=topic)
    return render(request, 'news/topic_detail.html', {'topic': topic, 'news': news})

# Представление для добавления новостей
@login_required  # Требует, чтобы пользователь был залогинен
def add_news(request, pk):
    # Проверяем, является ли пользователь администратором
    if not request.user.is_staff:  # Только администраторы могут добавлять новости
        return HttpResponseForbidden("You are not authorized to add news.")
    
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # Обрабатываем файлы (изображения)
        if form.is_valid():
            news = form.save(commit=False)
            news.topic = topic
            news.save()
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form, 'topic': topic})

# Представление для редактирования новостей
@login_required  # Требует, чтобы пользователь был залогинен
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    
    # Проверяем, является ли пользователь администратором
    if not request.user.is_staff:  # Только администраторы могут редактировать новости
        return HttpResponseForbidden("You are not authorized to edit news.")
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)  # Обрабатываем файлы (изображения)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', pk=news.topic.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/edit_news.html', {'form': form, 'news': news})

# Представление для удаления новостей
@login_required  # Требует, чтобы пользователь был залогинен
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    
    # Проверяем, является ли пользователь администратором
    if not request.user.is_staff:  # Только администраторы могут удалять новости
        return HttpResponseForbidden("You are not authorized to delete news.")
    
    news.delete()
    return redirect('topic_detail', pk=news.topic.pk)
