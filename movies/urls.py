from django.urls import path
from .views import *


urlpatterns = [
    path('', MoviesView.as_view(), name='home'),
    path('categories/', CategoryView.as_view(), name='category'),
    path('<slug:movie_slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('<int:cat_pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('about_project', about_project, name='about_project'),
    path('about_team/', about_team, name='about_team'),
    path('dev_contacts/', dev_contacts, name='dev_contacts'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
]


