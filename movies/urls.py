from django.urls import path
from .views import *


urlpatterns = [
    path('', about_project, name='about_project'),
    path('about_team/', about_team, name='about_team'),
    path('dev_contacts/', dev_contacts, name='dev_contacts'),
]