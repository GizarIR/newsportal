from django.contrib import admin
from .models import Author, Post, Category, PostCategory, CategorySubscriber, Comment

# Register your models here.
def nullfy_rating(modeladmin, request, queryset):
    """Функция обнуления рэйтинга публикации"""
    queryset.update(rating_post=0)
nullfy_rating.short_description = 'Обнуление рейтинга' # краткое описание указываем ВНЕ функции

# class Admin(admin.ModelAdmin):
#     list_display = ['', '', '', '', ]
#     list_filter = ['', '', '', '', ]
#     search_fields = ['', '', '', '', ]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_user', 'rating_author',]
    list_filter = ['author_user', 'rating_author',]
    search_fields = ['author_user', 'rating_author',]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name_category',
        'get_subscribers',
        # 'subscribers',
    ]
    # list_filter = ['name_category', 'subscribers',]
    # search_fields = ['name_category', 'subscribers',]

class PostAdmin(admin.ModelAdmin):
    """Наследуем класс Django, данное наследование позволяет настроить Админку для модели Post"""
    list_display = [
        'author_user',
        'post_type',
        'create_date',
        'get_cat', # 'category', #get_cat() - метод модели возвращающий категории модели, используем такак это поле ManyToMany
        'header_post',
        'text_post',
        'rating_post',
        'is_created',
    ]
    list_filter = ['author_user', 'post_type', 'create_date', 'category__name_category', 'rating_post']
    search_fields = ['header_post', 'text_post']
    actions = [nullfy_rating]



class CommentAdmin(admin.ModelAdmin):
    # простой перечень полей (при помощи for) - работает если нет полей типа ManyToMany
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ['author_user', 'create_datetime', 'rating_comment']
    search_fields = ['text_comment', 'post', 'author_user']



admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(CategorySubscriber)
# admin.site.unregister(CategorySubscriber) # модели можно разрегистрировать
admin.site.register(Comment, CommentAdmin)





