
from django.contrib import admin
from django.urls import path, include 
from django.shortcuts import render


def home(request):
    return render(request,'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('quiz/', include('quiz.urls', namespace='quiz')),
]
