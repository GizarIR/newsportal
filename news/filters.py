from django_filters import CharFilter, ModelChoiceFilter, ModelMultipleChoiceFilter, DateFilter
from django_filters import FilterSet
from .models import Post, PostCategory, Category, Author
import django.forms

class PostFilter(FilterSet):
    post__icontains = CharFilter(
        field_name='header_post',
        lookup_expr='icontains',
        label='Заголовок',
    )
    # Автор
    from_author = ModelMultipleChoiceFilter(
        field_name='author_user',
        queryset=Author.objects.all(),
        label='Автор',
        conjoined=True,
    )

    #Категория если хотим выбирать несколько категорий
    for_category =  ModelChoiceFilter(
        field_name='postcategory__throughCategory',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='любой',
    )

    create_date = DateFilter(
        label='Начиная с ',
        lookup_expr='gte',
        widget=django.forms.DateInput(
            attrs={
                'type':'date',
            }
        )
    )

    class Meta:
        model = Post
        fields = [
            'post__icontains',
            'create_date',
            'from_author',
            'for_category',
        ]

