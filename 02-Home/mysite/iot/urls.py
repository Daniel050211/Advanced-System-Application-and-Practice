from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('log', views.log, name='log'),
    path('info/', views.info),
]