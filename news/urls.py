from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),  

    # Список всех тем
    path('topics/', views.topic_list, name='topic_list'),  

    # Подробности темы
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),  

    # Добавление новостей
    path('topics/<int:pk>/add_news/', views.add_news, name='add_news'),  

    # Редактирование новостей
    path('news/<int:pk>/edit/', views.edit_news, name='edit_news'),  

    # Удаление новостей
    path('news/<int:pk>/delete/', views.delete_news, name='delete_news'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Для обслуживания медиафайлов
