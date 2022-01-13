from django.urls import path
from apps.web.management import views

urlpatterns = [

  path("", views.api, name="management.home"),

  path("api/", views.api, name="management.api"),

  # train
  path("train/", views.home, name="management.train"),

  # predict
  path("predict/<grade>/<int:k>/", views.predict, name="management.predict"),

  # settings
  path("reset/", views.reset, name="management.reset"),
  path("logs/", views.logs, name="management.logs"),

]
