from django.db import models
from django.contrib.auth.models import User
from django.db.models import Aggregate, Sum

# Create your models here.


class Author(models.Model):
    """
    Модель Author - объекты всех авторов, поля:
        - cвязь «один к одному», с встроенной моделью пользователей User;
        - рейтинг пользователя.
    """
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.SmallIntegerField(default=0)

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

class Category(models.Model):
    """
    Модель Category - nемы, которые они отражают (спорт, политика, образование и т. д.), поля:
        - название категории, поле уникально
    """
    name_category = models.CharField(max_length=64, unique=True)


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

    author_user = models.ForeignKey('Author', on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,
                                  choices=POST_TYPES,
                                  default=article)
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    header_post = models.CharField(max_length=128)
    text_post = models.TextField()
    rating_post = models.SmallIntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[0:123]} ...'


class PostCategory(models.Model):
    """
    Модель PostCategory - промежуточная модель для связи «многие ко многим»:
        - связь «один ко многим» с моделью Post;
        - связь «один ко многим» с моделью Category.
    """
    throughPost = models.ForeignKey('Post', on_delete=models.CASCADE)
    throughCategory = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    """
    Модель Comment - под каждой новостью/статьёй можно оставлять комментарии, поля:
        - связь «один ко многим» с моделью Post;
        - связь «один ко многим» со встроенной моделью User (комментарии может оставить необязательно автор);
        - текст комментария;
        - дата и время создания комментария;
        - рейтинг комментария.
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    rating_comment = models.SmallIntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()
