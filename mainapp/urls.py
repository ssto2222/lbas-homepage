from django.urls import path
from mainapp import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]
