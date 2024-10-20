from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if the user needs to change their password
            if request.user.force_change_password and request.path != reverse('password_change'):
                return redirect('password_change')

        return self.get_response(request)

# pbkdf2_sha256$870000$zhREnfaAzAEdhKHHN50Qox$AET4ilnnPsoawdvcMni2c7JBYGkpuRKwnit+Epj+vBw=