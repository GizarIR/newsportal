from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

# Create your views here.
from .models import Post
from .filters import PostFilter
from .forms import PostForm
# from pprint import pprint


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    # строчка ниже эквивалент queryset = Post.objects.all(), те если нужно можно использовать фильтры
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-create_date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

    # переопределим на всякий случай чтобы не забыть что есть такая возможность вытаскивать в шаблон доп инфу
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['bg_color_mode'] = 3
        # pprint(context)
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной статье
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Используем другое название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostsListSearch(ListView):
    model = Post
    ordering = 'create_date'
    template_name = 'posts_search.html'
    context_object_name = 'finded_posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


