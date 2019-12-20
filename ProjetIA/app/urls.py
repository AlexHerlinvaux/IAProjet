from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('accueil/', views.dj_game_ini),
    path('accueil/<int:input_>/',views.dj_game),
]
