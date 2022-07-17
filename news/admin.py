from django.contrib import admin
from .models import Post, Category, PostCategory

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)



