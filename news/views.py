# импорты django
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# группа импорта для реализации механизма добавления в группу пользователя через реадктирование профиля на портале
# с использованием библиотеки allauth
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


# импорты проекта
from .models import Post
from .filters import PostFilter
from .forms import PostFormArticle, PostFormNew
# Отключено поскольку регистрацию и аутентификацию по заданию необходимо реализовать через библиотеку allauth
from .forms import ProfileUserForm



class PostsList(ListView):
    """Представление возвращает список публикаций """
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

    # В шаблон передаем дополнительную информацию о том является ли пользователем участником группы author
    def get_context_data(self, **kwargs):
        """Данная функция добавлена при настройке allauth. Нужна для реализации механизма:
        пользователь который прошел регистрацию и залогинился, может быть включен
        в группу authors. Далее можно использовать данную переменную в любом шаблоне, например, posts.html """
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        # context['bg_color_mode'] = 3
        # pprint(context)
        return context

class PostDetail(DetailView):
    """Представление возвращает страницу с описанием публикации"""
    # Модель всё та же, но мы хотим получать информацию по отдельной статье
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Используем другое название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostsListSearch(LoginRequiredMixin, ListView):
    """Представление возвращает форму поиска со списком публикаций - результатом поиска"""
    model = Post
    ordering = '-create_date'
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


class PostCreateNew(LoginRequiredMixin, CreateView):
    """Представление возвращает форму создания новой новости"""
    form_class = PostFormNew
    model = Post
    template_name = 'post_edit_new.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type ='NW'
        return super().form_valid(form)


class PostCreateArticle(LoginRequiredMixin, CreateView):
    """Представление возвращает форму создания новой статьи"""
    form_class = PostFormArticle
    model = Post
    template_name = 'post_edit_article.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type ='AR'
        return super().form_valid(form)

class PostUpdateNew(LoginRequiredMixin, UpdateView):
    """Представление возвращает форму редактирования новости"""
    form_class = PostFormNew
    model = Post
    template_name = 'post_edit_new.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type ='NW'
        return super().form_valid(form)


class PostUpdateArticle(LoginRequiredMixin, UpdateView):
    """Представление возвращает форму редактирования статьи"""
    form_class = PostFormArticle
    model = Post
    template_name = 'post_edit_article.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type ='AR'
        return super().form_valid(form)

# # Вариант как в задании (html файлы тоже подготовлены)
# class PostDeleteNew(DeleteView):
#     model = Post
#     template_name = 'post_delete_new.html'
#     success_url = reverse_lazy('posts_list_search')
#
# class PostDeleteArticle(DeleteView):
#     model = Post
#     template_name = 'post_delete_article.html'
#     success_url = reverse_lazy('posts_list_search')

# удаление в задании можно сделать одним представлением, но с разной маршрутизацией, так на мой взгляд меньше кода
# и логичнее
class PostDelete(LoginRequiredMixin, DeleteView):
    """Представление возвращает форму удаления публикации"""
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list_search')

# Отключено поскольку регистрацию и аутентификацию по заданию необходимо реализовать через библиотеку allauth
class ProfileUserUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    model = User
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('home_news')

    # def get_context_data(self, **kwargs):
    #     """Данная функция добавлена при настройке allauth. Нужна для реализации механизма:
    #     пользователь который прошел регистрацию и залогинился, может быть включен
    #     в группу authors. Далее можно использовать данную переменную в любом шаблоне, например, редактирование профиля """
    #     context = super().get_context_data()
    #     context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
    #     return context

@login_required
def upgrade_me(request):
    """ Фукнкция добавлена при настройке allauth. Нужна для реализации механизма: пользователь который прошел регистрацию
        и залогинился, может быть включен в группу authors. Данная функция нужна для использования ее в urls.py"""
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('home_news')

