from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from user.forms import SignUpForm, LoginForm

from user.logic.profile import create_profile


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            create_profile(user)
            login(request, user)
            return redirect('guest')
    else:
        form = SignUpForm()
    return render(request, 'user/reg.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('guest')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})
