from django.contrib import admin
from django.urls import path, include  # подключаем include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # Подключаем urls из приложения news
]
