
from django.contrib import admin
from django.urls import path, include 
from django.shortcuts import render
from icecream import ic


def home(request):
    return render(request,'home.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def dev_tools_detected(request):
    if request.method == "POST":
        ic("Developer tools were opened!")
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def log_activity(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        timestamp = data.get("timestamp")
        print(f"Action logged: {action} at {timestamp}")
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls', namespace='quiz')),
    path('academics/', include('academics.urls', namespace='academics')),
    path('log-activity', log_activity, name='log_activity'),
    path('dev-tools-detected', dev_tools_detected, name='dev_tools_detected'),
    path('', include('users.urls')),
]
