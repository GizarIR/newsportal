from django.utils.translation import gettext as _

from django.contrib import admin
from .models import Author, Post, Category, PostCategory, CategorySubscriber, Comment
# импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)
from modeltranslation.admin import TranslationAdmin


# Register your models here.
def nullfy_rating(modeladmin, request, queryset):
    """Функция обнуления рэйтинга публикации"""
    queryset.update(rating_post=0)
nullfy_rating.short_description = _('Zeroing the rating') # краткое описание указываем ВНЕ функции

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
        'get_subscribers', # 'дополнительно описанный метод в модели для отражения поля ManyToMany
        # 'subscribers',
    ]
    # list_filter = ['name_category', 'subscribers',]
    # search_fields = ['name_category', 'subscribers',]

class CategoryAdminTranslation(CategoryAdmin, TranslationAdmin):
    model = Category


class RatingListFilter(admin.SimpleListFilter):
    """Данный класс описан для отображения рейтинга.
    Полное описание тут: https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin"""
    title = _('Category of rating')
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        return (
            ('50s', _('less than 50 points')),
            ('100s',_('more than 100 points')),
        )
    def queryset(self, request, queryset):
        if self.value() == '50s':
            return queryset.filter(rating_post__gte=0,
                                   rating_post__lte=50)
        if self.value() == '100s':
            return queryset.filter(rating_post__gte=100)

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
    list_filter = ['author_user', 'post_type', 'create_date', 'category__name_category', RatingListFilter]
    search_fields = ['header_post', 'text_post']
    actions = [nullfy_rating]
    list_per_page = 10


class PostAdminTranslation(PostAdmin, TranslationAdmin):
    model = Post

class CommentAdmin(admin.ModelAdmin):
    # простой перечень полей (при помощи for) - работает если нет полей типа ManyToMany
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ['author_user', 'create_datetime', 'rating_comment']
    search_fields = ['text_comment', 'post', 'author_user']

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['throughPost', 'throughCategory']
    list_filter = ['throughCategory']
    search_fields = ['throughPost', 'throughCategory']

class CategorySubscriberAdmin(admin.ModelAdmin):
    list_display = ['throughCategory', 'throughSubscriber']
    list_filter = ['throughCategory']
    search_fields = ['throughSubscriber', 'throughCategory']



admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdminTranslation)
admin.site.register(Post, PostAdminTranslation)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(CategorySubscriber, CategorySubscriberAdmin)
# admin.site.unregister(CategorySubscriber) # модели можно разрегистрировать
admin.site.register(Comment, CommentAdmin)





