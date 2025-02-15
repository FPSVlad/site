
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Topic, News
from .forms import NewsForm

def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'news/topic_list.html', {'topics': topics})

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    news = News.objects.filter(topic=topic)
    return render(request, 'news/topic_detail.html', {'topic': topic, 'news': news})

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

@login_required  # Требует, чтобы пользователь был залогинен
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    
    # Проверяем, является ли пользователь администратором
    if not request.user.is_staff:  # Только администраторы могут удалять новости
        return HttpResponseForbidden("You are not authorized to delete news.")
    
    news.delete()
    return redirect('topic_detail', pk=news.topic.pk)
