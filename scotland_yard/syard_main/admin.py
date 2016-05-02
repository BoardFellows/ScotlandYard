from django.contrib import admin
from .models import UserProfile, Game, Round

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Round)
