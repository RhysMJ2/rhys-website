from django.contrib import admin

# Register your models here.
from .models import Board, Topic, Post

# todo https://docs.djangoproject.com/en/3.0/ref/contrib/admin/actions/
# todo https://docs.djangoproject.com/en/3.0/ref/contrib/admin/

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
