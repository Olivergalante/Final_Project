from django.contrib import admin
from .models import Post, Profile, Comment, Image


# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Image)
