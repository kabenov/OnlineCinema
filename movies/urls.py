from django.conf.urls import url
from django.urls import path
from .views import *


urlpatterns = [
    path('', MoviesView.as_view(), name='home'),
    path('about_project', about_project, name='about_project'),
    path('about_team/', about_team, name='about_team'),
    path('dev_contacts/', dev_contacts, name='dev_contacts'),
    path('sign_up/', registerPage, name='sign_up'),
    path('sign_in/', loginPage, name='sign_in'),
    path('log_out/', logoutPage, name='log_out'),
    path('search/', search, name='search'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('create/', create, name='create'),
    path('edit/', edit, name='edit'),
    path('update/', update, name='update'),
    path('delete/', delete, name='delete'),
    path('<slug:movie_slug>/', MovieDetailView.as_view(), name='movie_detail'),
]


