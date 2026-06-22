"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from random import random
from django.http import HttpResponse
from app_datetime.views import datetime_view, dynamic_datetime_view



def random_view(request):
    if request.method == "GET":
        data = random()
        return HttpResponse(data)


def dynamic_random_view(request):
    if request.method == "GET":
        script = '''
            <script>
                function updateNumber() {
                    let randomNum = Math.random();
                    document.getElementById("random").innerText = randomNum; // Заменяем предыдущее значение на новое в блоке с id="random"
                }
                setInterval(updateNumber, 1000); // Запускаем обновление каждую секунду
                window.onload = updateNumber; // Генерируем первое число при загрузке
            </script>
            <body>
                <h1>Случайное число: <span id="random">Загрузка...</span></h1>
            </body>
        '''
        return HttpResponse(script)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('random/', random_view),
    path('dynamic_random/', dynamic_random_view),
    path('datetime/', datetime_view),
    path('dynamic_datetime/', dynamic_datetime_view),
    path('', include('app_weather.urls')),
    path('', include('app_store.urls')),
    path('login/', include('app_login.urls')),
]
