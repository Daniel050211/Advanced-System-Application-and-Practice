from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # http://localhost:8000/inventory/
]