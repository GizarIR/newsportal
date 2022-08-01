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

    #Создадим фильтр Категория
    for_category =  ModelChoiceFilter(
        field_name='postcategory__throughCategory',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='любой',
    )

    # Создадим на странице фильтр дат, для его отрисовки используем виджет
    create_date = DateFilter(
        label='Начиная с ',
        lookup_expr='gte',
        # виджеты - это такие поля, которые реализованы через отдельные классы и позволяют за счет настройки их атрибутов
        # получать визуализацию специфических полей фильтров без отдельной прорисовки их в html шаблонах
        widget=django.forms.DateInput(
            attrs={
                'type':'date',
                'format': '%d-%m-%Y',
            }
        )
    )


    class Meta:
        """Класс Meta позволяет определять порядок полей и регулярное выражение для поиска на странице
         Если нет других описаний полей поиска, то поля отрисуются автоматически"""
        model = Post
        fields = [
            'post__icontains',
            'create_date',
            'from_author',
            'for_category',
        ]
