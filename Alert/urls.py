from django.urls import path
from . import views

urlpatterns = [
    path('scrap/', views.send, name='hello'),
]