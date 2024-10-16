from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'users/auth/login.html'
    success_url = reverse_lazy('home')
    
    
    
class HomeView(TemplateView):
    template_name = 'users/home.html'


    
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', 'home')  # Get the 'next' URL from the query string
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next') or next_url  # Retrieve the 'next' URL from the POST data if available
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else: 
            return render(request, 'users/auth/login.html', {'error': 'Invalid credentials'})
    else:
        return render(
            request,
            'users/auth/login.html',
            {'next_url': next_url}
        )


def user_logout(request):
    logout(request)
    return redirect('login')