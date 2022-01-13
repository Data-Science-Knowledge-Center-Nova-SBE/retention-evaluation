from django.urls import path
from . import views

urlpatterns = [

  path("", views.HistoryLogList.as_view()),

]
