from django.contrib import admin

from movies.models import *

# superuser login: admin email: dias.kabenovgo60@gmail.com pass: adildias

admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Movie)
admin.site.register(Posters)
