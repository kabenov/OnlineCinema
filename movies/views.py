from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from movies.forms import CreateUserForm
from movies.models import *

data_members = [{'position': 'Team leader', 'name': 'Adil Gumarov', 'ph_num': '+7 (777) 129 57-47', 'ph_num_href': '+77771295747',
                 'off_hours': '08:00 - 16:00', 'pic_src': 'movies/images/adil.jpeg'},
                {'position': 'Developer', 'name': 'Dias Kabenov', 'ph_num': '+7 (708) 105 88-62', 'ph_num_href': '+77081058862',
                 'off_hours': '09:00 - 17:00', 'pic_src': 'movies/images/dias.jpeg'}
                ]

data_team = [{'name': 'Adil Gumarov', 'group': 'ITSE-1902', 'course': '3rd course', 'pic_src': 'movies/images/team_member-1.jpg'},
             {'name': 'Dias Kabenov', 'group': 'ITSE-1902', 'course': '3rd course', 'pic_src': 'movies/images/team_member-2.jpg'}]


class MoviesView(ListView):
    model = Movie
    template_name = 'movies/home_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posters'] = Posters.objects.filter(switch=True)
        return context


class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(Movie.objects.get(url=self.kwargs['movie_slug']).title)
        context['poster'] = Posters.objects.get(movie__title=Movie.objects.get(url=self.kwargs['movie_slug']).title)
        return context


# def sign_up(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         surname = request.POST['surname']
#         email = request.POST['e-mail']
#         password = request.POST['password']
#         re_password = request.POST['re-password']
#
#         if re_password == password:
#             if Users.objects.filter(email=email).exists():
#                 print('user with this email already exists!')
#             else:
#                 user = Users.objects.create(name=name, surname=surname, email=email, password=password, role_id=2)
#                 user.save()
#                 print('user registered')
#         else:
#             print('passwords are not matching!')
#
#         return redirect('/')
#
#     else:
#         return render(request, 'movies/sign_up.html')
#
#
# def sign_in(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#
#         if Users.objects.filter(email=email).exists():
#             user = Users.objects.get(email=email)
#             print(user.name, user.email, user.surname)
#             if password == user.password:
#                 return redirect('/')
#             else:
#                 print('password is not matching!')
#                 return redirect('sign_in?password_error/')
#         else:
#             print('user with this email is not exist!')
#     else:
#         return redirect('/')


def about_project(request):
    return render(request, 'movies/about_project.html', {'title': 'About project'})


def about_team(request):
    return render(request, 'movies/about_team.html', {'title': 'About team', 'members_data': data_team})


def dev_contacts(request):
    return render(request, 'movies/dev_contacts.html', {'title': 'Dev contacts', 'members_data': data_members})


def search(request):
    if request.method == 'GET':
        searched = request.GET['search']
        search_movies = Movie.objects.filter(title__icontains=searched)
        return render(request, 'movies/search.html', {'searched': searched, 'search_movies': search_movies})
    else:
        return render(request, 'movies/search.html', {})


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)

            return redirect('sign_in')

    context = {'form': form}
    return render(request, 'movies/sign_up.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect!')

    context = {}
    return render(request, 'movies/sign_in.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')
