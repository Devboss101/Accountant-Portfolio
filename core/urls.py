# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.portfolio, name='portfolio'),  # single route, one page
]