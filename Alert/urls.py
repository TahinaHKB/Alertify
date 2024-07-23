from django.urls import path
from . import views

urlpatterns = [
    path('scrap/<int:nb>', views.send, name='hello'),
]