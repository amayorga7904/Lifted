from django.contrib import admin
from .models import Post, Comment, Photo, Image

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Image)
