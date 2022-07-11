from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(User):
    """
    Модель Author - объекты всех авторов, поля:
    - cвязь «один к одному», с встроенной моделью пользователей User;
    - рейтинг пользователя.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)


class Category(models.Model):
    """
    Модель Category - nемы, которые они отражают (спорт, политика, образование и т. д.), поля:
    - название категории, поле уникально
    """
    name = models.CharFields(max_lenght=64, unique=True)


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

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    post_type = models.CharFields(max_length=2,
                                  choices=POST_TYPES,
                                  default=article)
    create_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    header = models.CharFields(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)


class PostCategory(models.Model):
    """
    Модель PostCategory - промежуточная модель для связи «многие ко многим»:
    - связь «один ко многим» с моделью Post;
    - связь «один ко многим» с моделью Category.
    """
    throughPost = models.ForeignKey('Post', on_delete=models.CASCADE)
    throughCategory = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Models):
    """
    Модель Comment - под каждой новостью/статьёй можно оставлять комментарии, поля:
    - связь «один ко многим» с моделью Post;
    - связь «один ко многим» со встроенной моделью User (комментарии может оставить необязательно автор);
    - текст комментария;
    - дата и время создания комментария;
    - рейтинг комментария.
    """
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

