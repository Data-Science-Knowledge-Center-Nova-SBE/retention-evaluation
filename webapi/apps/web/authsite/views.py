from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import logout as django_logout

from apps.web.authsite.forms import AuthenticationForm


def login(request):
  assert isinstance(request, HttpRequest)
  context = {}

  if request.method == 'POST':
    form = AuthenticationForm(request.POST)

    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']

      user = authenticate(username=username, password=password)

      if user != None:
        auth.login(request, user)
        return redirect('management.home')


    context["failedLogin"] = True
    return render(request, 'authsite/login.html', context);

  elif request.method == 'GET':
    if request.user.is_authenticated:
      if request.user.is_superuser:
        return redirect('gestao.home')
      else:
        return redirect('api.docs')

    return render(request, 'authsite/login.html', context);


def logout(request):
  assert isinstance(request, HttpRequest)
  django_logout(request)

  return redirect('authsite.login')


