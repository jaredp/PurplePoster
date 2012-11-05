from django.contrib import admin
from EventManager.models import PurplePoster
from EventManager.models import Movie
from EventManager.models import Actor
from EventManager.models import Producer
from EventManager.models import Poster
from EventManager.models import Image

admin.site.register(PurplePoster)
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Producer)
admin.site.register(Poster)
admin.site.register(Image)