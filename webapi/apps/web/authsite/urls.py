from django.urls import path
from apps.web.authsite import views

urlpatterns = [

  path("login/", views.login, name="authsite.login"),
  path("logout/", views.logout, name="authsite.logout"),

]
