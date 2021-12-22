from django.db import models

# Create your models here.
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField("Genre", max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Actor(models.Model):
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"


class Movie(models.Model):
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description", max_length=250, default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Assumenda voluptatem similique sed consequatur dolorem ad.")
    poster = models.ImageField("Poster", upload_to='movie_posters/')
    year = models.PositiveSmallIntegerField("Year", default=2021)
    country = models.CharField("Country", max_length=30)
    actors = models.ManyToManyField(Actor, verbose_name="actor", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="genre")
    rating = models.FloatField("Rating", default=0)
    agerestriction = models.IntegerField("agerestriction", default=16)
    trailer_link = models.CharField("Trailer", max_length=1000, default="https://www.youtube.com/embed/6z4tdTbIjJA")
    film_link = models.CharField("Film", max_length=1000, default="https://www.youtube.com/embed/6z4tdTbIjJA")
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'movie_slug': self.url})

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class Roles(models.Model):
    name = models.CharField("name", max_length=150)


class Users(models.Model):
    name = models.CharField("name", max_length=100)
    surname = models.CharField("surname", max_length=100)
    email = models.EmailField()
    password = models.CharField("password", max_length=10)
    role = models.ForeignKey(Roles, verbose_name="Role", on_delete=models.CASCADE)


class Posters(models.Model):
    img = models.ImageField("Poster", upload_to='carousel_posters/')
    movie = models.ForeignKey(Movie, verbose_name="movie", on_delete=models.CASCADE)
    switch = models.BooleanField(default=True, verbose_name="switch")
    name = models.CharField("name", max_length=100)

    class Meta:
        verbose_name = "Poster"
        verbose_name_plural = "Posters"
