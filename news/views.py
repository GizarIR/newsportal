# импорты django
import time
import datetime
from datetime import datetime, timedelta, timezone
from django.http import HttpResponse

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy




# группа импорта для реализации механизма добавления в группу пользователя через реадктирование профиля на портале
# с использованием библиотеки allauth
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст


# импорты проекта
from .models import Post, Author, CategorySubscriber, Category, PostCategory
from django.contrib.auth.models import User
from .filters import PostFilter
from .forms import PostFormArticle, PostFormNew, ProfileUserForm
from django.db.models import Q

# импорты для реализации исключения при проверке количества постов в день
from django.core.exceptions import ValidationError

# группа импортов для работы с кэшем
from django.core.cache import cache

# включаем логирование
# import logging
# ниже можно в качестве параметра подставлять все описанные loggers если есть необходимость отлавливать
# сообщения из разных модулей тогда можно в качестве параметра использовать __name__ но при этом в settings.py.LOGGING
# нужно описать иерархию логеров и использовать propagate для исключения двойной обработки сообщений
# разными логерами находящимися в одной иерархии
# logger = logging.getLogger('file_general')
# logger = logging.getLogger('django')

# Настройки включения перевода
from django.utils.translation import gettext as _ # импортируем функцию перевода

# ограничение на количество публикаций в день для автора
LIMIT_POSTS = 20

# пример создания вьюшки через функцию - исключительно в целях тестирования реализации
def index_test(request):
    # отправим сообщение в файл лога
    # logger.debug("Hello! --------DEBUG--------Enjoy:)")
    # logger.info("Hello! --------INFO--------Enjoy:)")
    # logger.warning("Hello! --------WARNING--------Enjoy:)")
    # logger.error("Hello! --------ERROR--------Enjoy:)")
    # logger.critical("Hello! --------CRITICAL--------Enjoy:)")
    # # logger_django.error("Hello! --------DJANGO-ERROR--------Enjoy:)")
    return HttpResponse("<p> Сообщение для тестирования </p>")


# пример создания вьюшки через класс - исключительно в целях тестирования реализации
class IndexTrans(View):
    def get(self, request):
        string = _("Test string")
        return HttpResponse(string)


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

    # функция добавлена при более тонкой настройки работы кэша, чтобы при обновлении поста он обновлялся и вкэше
    # также внесены изменения в модель Post
    # переопределяем метод получения объекта,
    def get_object(self, *args, **kwargs):
        # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу,
        # если его нет, то забирает None.
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # получаем id текущей публикации
        id_post = self.kwargs.get('pk')
        # получаем в виде QuerySet список категорий на которые пользователь подписан
        # (их перечень можно посмотреть в профиле на портале)
        # строчка ниже отключена из-за включения перевода за ненадобностью
        # cat_user = Category.objects.filter(subscribers__username=self.request.user).values('name_category')

        # Получаем в виде QuerySet список категорий для предложения подписки, т.е. те категории на которые пользователь
        # не пописан, но они есть в списке категорий поста
        # qs_subscribe = Post.objects.filter(pk=id_post)[0].category.exclude(name_category__in=cat_user)
        # строчка выше перестала работать т.к. простой QuerySet на мультиязычный
        # а для данного типа запрос работал только для языка по умолчанию
        # пришлось переделать на строчку ниже
        qs_subscribe = Category.objects.filter(Q(post__pk=id_post) & ~Q(subscribers__username=self.request.user))

        # Получаем в виде QuerySet список категорий для предложения отписки, т.е. те категории на которые пользователь
        # подписан и они есть в списке категорий поста
        # qs_unsubscribe = Post.objects.filter(pk=id_post).category.filter(name_category__in=cat_user)
        # строчка выше перестала работать т.к. простой QuerySet на мультиязычный
        # а для данного типа запрос работал только для языка по умолчанию
        # пришлось переделать на строчку ниже (для тестирования удобно использовать новость 131 b 132)
        qs_unsubscribe = Category.objects.filter(Q(post__pk=id_post) & Q(subscribers__username=self.request.user))

        # передаем списки в контекст для отображения в шаблоне, id нужен для передачи в функции add/del_subscribe
        context['cat_for_subscribe'] = qs_subscribe.values('id','name_category')
        context['cat_for_unsubscribe'] = qs_unsubscribe.values('id','name_category')
        # для правильной отрисовки шаблона передаем в контекст информацию о том пустые ли списки
        context['offer_subscribe'] = qs_subscribe.exists()
        context['offer_unsubscribe'] = qs_unsubscribe.exists()
        return context


@login_required
def add_subscribe(request, **kwargs):
    pk_cat = kwargs.get('pk')
    # pk_cat = pk
    # print(f'Передается категория: {pk_cat}')
    # print('Пользователю', request.user, 'добавлена категория в подписку:', Category.objects.get(pk=pk_cat))
    Category.objects.get(pk=pk_cat).subscribers.add(request.user)
    return redirect('home_news')

@login_required
def del_subscribe(request, **kwargs):
    pk_cat = kwargs.get('pk')
    # print('Пользователь', request.user, 'отписан от подписок на категорию:', Category.objects.get(pk=pk_cat))
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
        # Ограничение на создание не более 3-х публикаций в день
        author = post.author_user
        d_from = datetime.now(tz=timezone.utc).date()
        # print(d_from)
        d_to = d_from + timedelta(days=1)
        # print(d_to)
        posts = Post.objects.filter(author_user=author, create_date__range=(d_from, d_to))
        # print(posts)
        if len(posts) > LIMIT_POSTS:
            # raise ValidationError('Вы превысили ограничение на количество постов в день > 3!')
            return HttpResponse(_("""<h3>You have exceeded the limit of 3 publications per day!</h3>
            <p><a href="/posts/">Return to the portal</a></p>"""))
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
        post.author_user = Author.objects.get(author_user=self.request.user)

        # Ограничение на создание не более 3-х публикаций в день
        author = post.author_user
        d_from = datetime.now(tz=timezone.utc).date()
        d_to = d_from + timedelta(days=1)
        posts = Post.objects.filter(author_user=author, create_date__range=(d_from, d_to))
        if len(posts) > LIMIT_POSTS:
            return HttpResponse(_("""<h3>You have exceeded the limit of 3 publications per day!</h3>
            <p><a href="/posts/">Return to the portal</a></p>"""))

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
        post.is_created = False
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
        post.is_created = False
        return super().form_valid(form)

class PostDelete(LoginRequiredMixin, DeleteView):
    """Представление возвращает форму удаления публикации"""
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list_search')


class ProfileUserUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
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
    """ Функция добавлена при настройке allauth. Нужна для реализации механизма: пользователь который прошел регистрацию
        и залогинился, может быть включен в группу authors. Данная функция нужна для использования ее в urls.py"""
    user = request.user
    author_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        # добавим в модель allauth
        author_group.user_set.add(user)
        # добавим также автора в нашу таблицу Author
        Author.objects.create(author_user=user)

    return redirect('home_news')



