from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic import View

from movies.models import *

data_members = [
    {'position': 'Team leader', 'name': 'Adil Gumarov', 'ph_num': '+7 (777) 129 57-47', 'ph_num_href': '+77771295747',
     'off_hours': '08:00 - 16:00', 'pic_src': 'movies/images/adil.jpeg'},
    {'position': 'Developer', 'name': 'Dias Kabenov', 'ph_num': '+7 (708) 105 88-62', 'ph_num_href': '+77081058862',
     'off_hours': '09:00 - 17:00', 'pic_src': 'movies/images/dias.jpeg'}
    ]

data_team = [{'name': 'Adil Gumarov', 'group': 'ITSE-1902', 'course': '3rd course',
              'pic_src': 'movies/images/team_member-1.jpg'},
             {'name': 'Dias Kabenov', 'group': 'ITSE-1902', 'course': '3rd course',
              'pic_src': 'movies/images/team_member-2.jpg'}
             ]


class MoviesView(ListView):
    model = Category
    template_name = 'movies/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(MoviesView, self).get_context_data(**kwargs)
        context['movie_list'] = Movie.objects.all()
        return context


class CategoryView(ListView):
    model = Category
    template_name = 'movies/category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['movie_list'] = Movie.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    slug_url_kwarg = 'cat_pk'
    template_name = 'movies/category_detail.html'


class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'
    slug_url_kwarg = 'movie_slug'


def sign_up(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['e-mail']
        password = request.POST['password']
        re_password = request.POST['re-password']

        if re_password == password:
            if Users.objects.filter(email=email).exists():
                print('user with this email already exists!')
            else:
                user = Users.objects.create(name=name, surname=surname, email=email, password=password, role_id=2)
                user.save()
                print('user registered')
        else:
            print('passwords are not matching!')

        return redirect(MoviesView.as_view)

    else:
        return render(request, 'movies/sign_up.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if Users.objects.filter(email=email).exists():
            user = Users.objects.get(email=email)
            print(user.name, user.email, user.surname)
            if password == user.password:
                return redirect(MoviesView.as_view)
            else:
                print('password is not matching!')
                return redirect('sign_in?password_error/')
        else:
            print('user with this email is not exist!')
    else:
        return render(request, 'movies/sign_in.html')


def about_project(request):
    return render(request, 'movies/about_project.html', {'title': 'About project'})


def about_team(request):
    return render(request, 'movies/about_team.html', {'title': 'About team', 'members_data': data_team})


def dev_contacts(request):
    return render(request, 'movies/dev_contacts.html', {'title': 'Dev contacts', 'members_data': data_members})
