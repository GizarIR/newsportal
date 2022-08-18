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
from django.contrib.auth.mixins import PermissionRequiredMixin

# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст


# импорты проекта
from .models import Post, Author, CategorySubscriber, Category, PostCategory
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # получаем id текущей публикации
        id_post = self.kwargs.get('pk')
        # получаем в виде QuerySet список категорий на которые пользователь подписан
        # (их перечень можно посмотреть в профиле на портале)
        cat_user = Category.objects.filter(subscribers__username=self.request.user).values('name_category')
        # получаем в виде QuerySet список категорий для предложения подписки, т.е. те категории на которые пользователь
        # не пописан, но они есть в списке категорий поста
        qs_subscride = Post.objects.get(pk=id_post).category.exclude(name_category__in=cat_user)
        # получаем в виде QuerySet список категорий для предложения отписки, т.е. те категории на которые пользователь
        # подписан и они есть в списке категорий поста
        qs_unsubscribe = Post.objects.get(pk=id_post).category.filter(name_category__in=cat_user)
        # передаем списки в контекст для отображения в шаблоне, id нужен для передачи в функции add/del_subscribe
        context['cat_for_subscribe'] = qs_subscride.values('id','name_category')
        context['cat_for_unsubscribe'] = qs_unsubscribe.values('id','name_category')
        # для правильной отрисовки шаблона передаем в контекст информацию о том пустые ли списки
        context['offer_subscribe'] = qs_subscride.exists()
        context['offer_unsubscribe'] = qs_unsubscribe.exists()
        return context

@login_required
def add_subscribe(request, **kwargs):
    pk_cat = kwargs.get('pk')
    # pk_cat = pk
    # print(f'Передается категория: {pk_cat}')
    print('Пользователю', request.user, 'добавлена категория в подписку:', Category.objects.get(pk=pk_cat))
    Category.objects.get(pk=pk_cat).subscribers.add(request.user)
    return redirect('home_news')

@login_required
def del_subscribe(request, **kwargs):
    pk_cat = kwargs.get('pk')
    print('Пользователь', request.user, 'отписан от подписок на категорию:', Category.objects.get(pk=pk_cat))
    Category.objects.get(pk=pk_cat).subscribers.remove(request.user)
    return redirect('home_news')


class PostsListSearch(LoginRequiredMixin, ListView):
    """Представление возвращает форму поиска со списком публикаций - результатом поиска"""
    model = Post
    ordering = '-create_date'
    template_name = 'posts_search.html'
    context_object_name = 'finded_posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class PostCreateNew(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление возвращает форму создания новой новости"""
    permission_required = ('news.add_post')
    form_class = PostFormNew
    model = Post
    template_name = 'post_edit_new.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type ='NW'
        post.author_user = Author.objects.get(author_user=self.request.user)
        #
        # Код ниже - Вариант 1 Отправки уведомлений о новой новости подписчикам реализован при помощи сигналов, поэтому здесь
        # # отключен, но оставлен исключительно в обучающем ключе как вариант работающей реализации
        # (его также можно использовать в signals.py там испольщован вариант 2)
        #
        # email_recipients = []
        # # получаем в виде QuerySet список id категорий поста
        # # print(form.cleaned_data['category'].values_list('id', flat=True))
        # qs_cat_post_id = form.cleaned_data['category'].values_list('id', flat=True)
        # # затем получаем список id подписчиков для всех категорий поста
        # qs_subs_list_id = CategorySubscriber.objects.filter(throughCategory__in=qs_cat_post_id).values('throughSubscriber__id').distinct()
        # # и наконец получаем список неповторяющихся емейлов подписчиков, values_list - выдает именно список list
        # qs_email_recipients = User.objects.filter(id__in=qs_subs_list_id).values_list('email', flat=True).distinct()
        # email_recipients = qs_email_recipients
        #
        # print(f'Список для отправления писем: {email_recipients}')
        #
        # html_content = render_to_string(
        #     'post_created.html',
        #     {
        #         'post': post,
        #     }
        # )
        # msg = EmailMultiAlternatives(
        #     subject=f'Новая публикация в вашем любимом разделе.',
        #     body=post.text_post,
        #     from_email='gizarir@mail.ru',
        #     to=email_recipients,
        # )
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
        return super().form_valid(form)


class PostCreateArticle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Представление возвращает форму создания новой статьи"""
    permission_required = ('news.add_post')
    form_class = PostFormArticle
    model = Post
    template_name = 'post_edit_article.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type ='AR'
        return super().form_valid(form)

class PostUpdateNew(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление возвращает форму редактирования новости"""
    permission_required = ('news.change_post')
    form_class = PostFormNew
    model = Post
    template_name = 'post_edit_new.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type ='NW'
        return super().form_valid(form)


class PostUpdateArticle(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Представление возвращает форму редактирования статьи"""
    permission_required = ('news.change_post')
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

# Редактирование профиля пользователя
class ProfileUserUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    model = User
    template_name = 'profile_edit.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('home_news')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.user.pk)
        context['subscribes']=Category.objects.filter(subscribers__username=self.request.user).values('name_category')
        return context

@login_required
def upgrade_me(request):
    """ Фукнкция добавлена при настройке allauth. Нужна для реализации механизма: пользователь который прошел регистрацию
        и залогинился, может быть включен в группу authors. Данная функция нужна для использования ее в urls.py"""
    user = request.user
    author_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        # добавим в модель allauth
        author_group.user_set.add(user)
        # добавим также автора в нашу таблицу Author
        Author.objects.create(author_user=user)

    return redirect('home_news')



