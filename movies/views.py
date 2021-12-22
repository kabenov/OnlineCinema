from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from movies.forms import CreateUserForm
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
              'pic_src': 'movies/images/team_member-2.jpg'}]


class MoviesView(ListView):
    model = Movie
    template_name = 'movies/home_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posters'] = Posters.objects.filter(switch=True)
        context['title'] = "Rory"
        return context


class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'
    slug_url_kwarg = 'movie_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Movie.objects.get(url=self.kwargs['movie_slug']).title
        context['poster_check'] = True
        try:
            context['poster'] = Posters.objects.get(movie__title=Movie.objects.get(url=self.kwargs['movie_slug']).title)
            context['poster_check'] = False
        except:
            context['poster'] = "/media/carousel_posters/def_poster.png"

        return context


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
        return render(request, 'movies/search.html', {'searched': searched, 'search_movies': search_movies, 'title': searched})
    else:
        return render(request, 'movies/search.html', {'title': 'Rory'})


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


# ADMIN VIEWS


def admin_panel(request):
    actors = Actor.objects.all()
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    posters = Posters.objects.all()
    context = {'actors_list': actors, 'genres_list': genres, 'movies_list': movies, 'posters_list': posters, 'title': 'Rory'}

    return render(request, 'movies/admin_panel.html', context)


def create(request):
    if "addActor" in request.POST:
        actor_name = request.POST['name']
        actor_age = request.POST['age']
        actor = Actor.objects.create(name=actor_name, age=actor_age)
        actor.save()
        messages.success(request, actor_name + ' added successfully!')

    elif "addGenre" in request.POST:
        genre_name = request.POST['name']
        genre = Genre.objects.create(name=genre_name)
        genre.save()
        messages.success(request, genre_name + ' added successfully!')

    elif "addMovie" in request.POST:
        movie_title = request.POST['title']
        movie_poster = request.FILES['poster']
        movie_year = request.POST['year']
        movie_country = request.POST['country']
        movie_rating = request.POST['rating']
        movie_url = request.POST['url']
        movie_agerestriction = request.POST['agerestriction']
        movie_description = request.POST['description']
        film_link = request.POST['film_link']
        trailer_link = request.POST['trailer_link']
        movie = Movie.objects.create(title=movie_title, poster=movie_poster, year=movie_year,
                                     country=movie_country, rating=movie_rating, url=movie_url,
                                     agerestriction=movie_agerestriction, description=movie_description,
                                     film_link=film_link, trailer_link=trailer_link)

        actor_ids = request.POST.getlist('actor')
        genre_ids = request.POST.getlist('genre')
        for actor_id in actor_ids:
            movie.actors.add(actor_id)

        for genre_id in genre_ids:
            movie.genres.add(genre_id)

        movie.save()
        messages.success(request, movie_title + ' added successfully!')

    elif "addPoster" in request.POST:
        name = request.POST['name']
        movie_id = request.POST['movie_id']
        poster_switch = request.POST['switch'] == "on"
        poster_img = request.FILES.get("poster")
        poster = Posters.objects.create(name=name, img=poster_img, movie_id=movie_id, switch=poster_switch)
        poster.save()
        messages.success(request, 'Poster added successfully!')

    return redirect('admin_panel')


def edit(request):
    context = {}

    if "editActor" in request.POST:
        actor_id = request.POST['id']
        actor = Actor.objects.get(id=actor_id)
        context = {'actor': actor, 'data': 'actor', 'title': 'Rory Edit'}

    elif "editGenre" in request.POST:
        genre_id = request.POST['id']
        genre = Genre.objects.get(id=genre_id)
        context = {'genre': genre, 'data': 'genre', 'title': 'Rory Edit'}

    elif "editMovie" in request.POST:
        movie_id = request.POST['id']
        movie = Movie.objects.get(id=movie_id)
        actors = Actor.objects.all()
        genres = Genre.objects.all()
        selectedA = []
        selectedG = []
        for actor in actors:
            check = False
            for actor1 in movie.actors.all():
                if actor == actor1:
                    check = True
            if check:
                selectedA.append(True)
            else:
                selectedA.append(False)

        for genre in genres:
            check = False
            for genre1 in movie.genres.all():
                if genre == genre1:
                    check = True
            if check:
                selectedG.append(True)
            else:
                selectedG.append(False)

        selected_actors = zip(actors, selectedA)
        selected_genres = zip(genres, selectedG)

        context = {'movie': movie, 'data': 'movie', 'actors_list': actors, 'genres_list': genres,
                   'selected_actors': selected_actors, 'selected_genres': selected_genres, 'title': 'Rory Edit'}

    elif "editPoster" in request.POST:
        poster_id = request.POST['id']
        poster = Posters.objects.get(id=poster_id)
        movies = Movie.objects.all()
        context = {'poster': poster, 'data': 'poster', 'movies_list': movies, 'title': 'Rory Edit'}

    return render(request, 'movies/updateData.html', context)


def update(request):
    if "updateActor" in request.POST:
        actor_id = request.POST['id']
        actor = Actor.objects.get(id=actor_id)
        actor.name = request.POST['name']
        actor.age = request.POST['age']
        actor.save()
        messages.success(request, 'Actor changed successfully!')

    elif "updateGenre" in request.POST:
        genre_id = request.POST['id']
        genre = Genre.objects.get(id=genre_id)
        genre.name = request.POST['name']
        genre.save()
        messages.success(request, 'Genre changed successfully!')

    elif "updateMovie" in request.POST:
        movie_id = request.POST['id']
        movie = Movie.objects.get(id=movie_id)
        movie.title = request.POST['title']
        movie.poster = request.FILES['poster']
        movie.year = request.POST['year']
        movie.country = request.POST['country']
        movie.rating = request.POST['rating']
        movie.url = request.POST['url']
        movie.agerestriction = request.POST['agerestriction']
        movie.description = request.POST['description']
        movie.film_link = request.POST['film_link']
        movie.trailer_link = request.POST['trailer_link']

        actor_ids = request.POST.getlist('actor')
        genre_ids = request.POST.getlist('genre')
        movie.actors.clear()
        movie.genres.clear()
        for actor_id in actor_ids:
            movie.actors.add(actor_id)

        for genre_id in genre_ids:
            movie.genres.add(genre_id)

        movie.save()
        messages.success(request, 'Movie changed successfully!')

    elif "updatePoster" in request.POST:
        poster_id = request.POST['id']
        poster = Posters.objects.get(id=poster_id)
        poster.movie_id = request.POST['movie_id']
        poster.switch = request.POST['switch'] == "on"
        poster.img = request.FILES['postr']
        poster.save()
        messages.success(request, 'Poster changed successfully!')

    return redirect('admin_panel')


def delete(request):
    if "deleteActor" in request.POST:
        actor_id = request.POST['id']
        actor = Actor.objects.get(id=actor_id)
        actor_name = actor.name
        actor.delete()
        messages.success(request, actor_name + ' deleted successfully!')

    elif "deleteGenre" in request.POST:
        genre_id = request.POST['id']
        genre = Genre.objects.get(id=genre_id)
        genre_name = genre.name
        genre.delete()
        messages.success(request, genre_name + ' deleted successfully!')

    elif "deleteMovie" in request.POST:
        movie_id = request.POST['id']
        movie = Movie.objects.get(id=movie_id)
        movie_name = movie.name
        movie.delete()
        messages.success(request, movie_name + ' deleted successfully!')

    elif "deletePoster" in request.POST:
        poster_id = request.POST['id']
        poster = Posters.objects.get(id=poster_id)
        poster_name = poster.name
        poster.delete()
        messages.success(request, poster_name + ' deleted successfully!')

    return redirect('admin_panel')
