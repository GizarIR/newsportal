from django.db import models
from django.contrib.auth.models import User
from django.db.models import Aggregate, Sum
from django.urls import reverse

# группа импортов для работы кэширования
from django.core.cache import cache


# группа импортов для работы переводов
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy # имопртируем ленивую функйию перевода

# Create your models here.

class Author(models.Model):
    """
    Модель Author - объекты всех авторов, поля:
        - cвязь «один к одному», с встроенной моделью пользователей User;
        - рейтинг пользователя.
    """
    author_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    ) #параметр on_delete м.б. SET_NULL
    rating_author = models.SmallIntegerField(default=0, verbose_name="Рэйтинг")

    def update_rating(self):
        """
        Обновляет рейтинг пользователя, переданный в аргумент этого метода.
        состоит из:
            - суммарный рейтинг каждой статьи автора умножается на 3;
            - суммарный рейтинг всех комментариев автора;
            - суммарный рейтинг всех комментариев к статьям автора.
        """
        post_rat = 0
        com_aut_rat = 0
        com_aut_art_rat = 0

        post_rat = 3 * Post.objects.filter(author_user=self.id).aggregate(Sum('rating_post'))['rating_post__sum']
        com_aut_rat = Comment.objects.filter(author_user=self.id).aggregate(Sum('rating_comment'))['rating_comment__sum']
        com_aut_art_rat = Comment.objects.filter(post__author_user=self.id).aggregate(Sum('rating_comment'))['rating_comment__sum']
        self.rating_author = post_rat + com_aut_rat + com_aut_art_rat
        self.save()

    def __str__(self):
        return f'{self.author_user.username}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    """
    Модель Category - темы, которые они отражают (спорт, политика, образование и т. д.), поля:
        - название категории, поле уникально
    """
    name_category = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_('Category'),
        help_text=_('Name of category - 64 characters'),
    )
    subscribers = models.ManyToManyField(
        User,
        through='CategorySubscriber',
        blank=True,
        verbose_name=_("Subscribers"),
    )

    def get_subscribers(self):
        """метод возвращает список подписчиков, добавлен для отображения категорий в админке"""
        return " ".join([s.username for s in self.subscribers.all()])

    get_subscribers.short_description = _("Subscribers")

    # переопределяя этот метод мы получаем красивое название объекта  в админ панели
    def __str__(self):
        return f"{self.name_category.title()}"

    # переопределяя этот класс мы получаем красивые названия классов в админ панели
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class CategorySubscriber(models.Model):
    throughCategory = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Category"),
    )
    throughSubscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=pgettext_lazy('Subscriber for article', 'Subscriber'),
    )

    class Meta:
        verbose_name = _('Connection Category-Subscriber')
        verbose_name_plural = _('Connections Categories-Subscribers')

class Post(models.Model):
    """
    Модель Post - статьи и новости, поля:
        - связь «один ко многим» с моделью Author;
        - поле с выбором — «статья» или «новость»;
        - автоматически добавляемая дата и время создания;
        - связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
        - заголовок статьи/новости;
        - текст статьи/новости;
        - рейтинг статьи/новости.
    """
    news = 'NW'
    article = 'AR'

    POST_TYPES =[
        (news, 'Новость'),
        (article, 'Статья'),
    ]

    author_user = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name=_("Author"))
    post_type = models.CharField(max_length=2,
                                  choices=POST_TYPES,
                                  default=article,
                                  verbose_name=_('Type of post'),
                                 )
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'),)
    category = models.ManyToManyField('Category', through='PostCategory', verbose_name=_('Category'))
    header_post = models.CharField(max_length=128, verbose_name=_('Title'))
    text_post = models.TextField(verbose_name=_('Text'))
    rating_post = models.SmallIntegerField(default=0, verbose_name=_('Rating'))
    is_created = models.BooleanField(default=True, verbose_name=_('Created')) # Редакция для обработки в signals.py - только создали или модифицируем

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[0:123]} ...'

    def __str__(self):
        # return f"{self.create_date:%Y-%m-%d %H:%M} --- {self.header_post}"
        return f"{self.header_post}"

    # Функция нужна для корректной работы формы создания публикации view PostCreate и форма PostForm, она возвращает
    # на страницу детализации после нажатия кнопки Сохранить, эта функция возвращает абсолютный адрес экземпляра
    # объекта (записи таблицы)
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])

    # группа функций необходимых чтобы при изменении публикации она обновлялась в кэше,
    # __str__ и get_absolute_url тоже нужны
    # для этого переопределяем метод save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

    def get_cat(self):
        """метод возвращает список категорий, добавлен для отображения категорий в админке"""
        return "\n".join([c.name_category for c in self.category.all()])

    get_cat.short_description = _('Categories')

    # переопределяя этот класс мы получаем красивые названия классов в админ панели
    class Meta:
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')
        # ordering = '-create_date'

class PostCategory(models.Model):
    """
    Модель PostCategory - промежуточная модель для связи «многие ко многим»:
        - связь «один ко многим» с моделью Post;
        - связь «один ко многим» с моделью Category.
    """
    throughPost = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name=_('Publication'))
    throughCategory = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'))

    # def __str__(self):
    #     return f"{Category.objects.get(postcategory__throughCategory=self.throughCategory).values('name_category')}"

    # переопределяя этот класс мы получаем красивые названия классов в админ панели
    class Meta:
        verbose_name = _('Connection Publication - Category')
        verbose_name_plural = _('Connections Publications - Categories')

class Comment(models.Model):
    """
    Модель Comment - под каждой новостью/статьёй можно оставлять комментарии, поля:
        - связь «один ко многим» с моделью Post;
        - связь «один ко многим» со встроенной моделью User (комментарии может оставить необязательно автор);
        - текст комментария;
        - дата и время создания комментария;
        - рейтинг комментария.
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name=_('Publication'))
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    text_comment = models.TextField(verbose_name=_('Comment'))
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date'))
    rating_comment = models.SmallIntegerField(default=0, verbose_name=_('Rating'))

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
