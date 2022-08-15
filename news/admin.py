from django.contrib import admin
from .models import Post, Category, PostCategory, CategorySubscriber

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(CategorySubscriber)



