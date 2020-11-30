from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Likes)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Comment)
admin.site.register(Screenshot)
admin.site.register(Rating)

