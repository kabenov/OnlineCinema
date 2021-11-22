from django.urls import path
from .views import *


urlpatterns = [
    path('', home_page, name='home'),
    path('about_project', about_project, name='about_project'),
    path('about_team/', about_team, name='about_team'),
    path('dev_contacts/', dev_contacts, name='dev_contacts'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
]