from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
from .models import Post
from pprint import pprint


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-create_date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'

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
