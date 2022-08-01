from django_filters import CharFilter, ModelChoiceFilter, ModelMultipleChoiceFilter
from django_filters import FilterSet
from .models import Post, PostCategory, Category


class PostFilter(FilterSet):
    post__icontains = CharFilter(
        field_name='header_post',
        lookup_expr='icontains',
        label='Заголовок содержит',
    )

    # #Категория если хотим выбирать только одну категорию
    # category = ModelChoiceFilter(
    #     field_name='postcategory__throughCategory',
    #     queryset=Category.objects.all(),
    #     label='Категория'
    #     empty_name = 'любая',
    # )

    #Категория если хотим выбирать несколько категорий
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__throughCategory',
        queryset=Category.objects.all(),
        label='Категория',
        conjoined=True,
    )


    class Meta:
        model = Post
        fields = {
            'text_post': ['icontains'],
        }

