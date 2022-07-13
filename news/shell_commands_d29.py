from news.models import *
from django.contrib.auth.models import User

# 1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).
admin = User.objects.get(id=1)
u1 = User.objects.create_user('Gizar')
u2 = User.objects.create_user('Stepan')

# 2. Создать два объекта модели Author, связанные с пользователями.
a1 = Author.objects.create(author_user=u1)
a2 = Author.objects.create(author_user=u2)

# 3. Добавить 4 категории в модель Category.
Category.objects.create(name_category='ИТ')
Category.objects.create(name_category='Экономика')
Category.objects.create(name_category='Спорт')
Category.objects.create(name_category='Искусство')

# 4. Добавить 2 статьи и 1 новость.
# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
p1 = Post.objects.create(author_user=a1, post_type="AR", header_post="Заголовок статьи которая первая", text_post="Обычно тут не было сложностей, но вот что то пошло не так")                                                                                                                                                                      ^
p1.category.set([Category.objects.get(id=1)])
p2 = Post.objects.create(author_user=a2, post_type='AR', header_post="Какой то заголовок второй статьи", text_post="Новый текст второй статьи")
p2.category.set([Category.objects.get(id=2)])
p3 = Post.objects.create(author_user=a1, post_type='NW', header_post="Заголовок новости", text_post="Текст простой новости")
p3.category.add(Category.objects.get(id=3))
p3.category.add(Category.objects.get(id=4))

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
c1 = Comment.objects.create(post=p1, author_user=u1, text_comment="Очень классная статья")
c2 = Comment.objects.create(post=p2, author_user=u1, text_comment="Так себе пост")
c3 = Comment.objects.create(post=p3, author_user=u2, text_comment="Автар жжет")
c4 = Comment.objects.create(post=p3, author_user=u1, text_comment="Как же хорошо все выглядит, а на самом деле...")
c5 = Comment.objects.create(post=p1, author_user=admin, text_comment="А вот и комментарий и не от автора")

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
p1.like()
p1.like()
p1.rating_post
p2.dislike()
p2.dislike()
p2.dislike()
p2.rating_post
p3.like()
p3.like()
p3.like()
p3.like()
p3.rating_post
c1.like()
c1.like()
c1.like()
c1.like()
c1.rating_comment
c2.dislike()
c2.dislike()
c2.dislike()
c2.dislike()
c2.rating_comment
c3.like()
c3.like()
c4.dislike()
c4.dislike()
c4.dislike()
c4.rating_comment
c5.like()
c5.like()
c5.like()
c5.like()
c5.like()
c5.rating_comment

# 8. Обновить рейтинги пользователей.
a1.update_rating()
a2.update_rating()
Author.objects.all().values()

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
# вариант 1:
top_a = Author.objects.order_by('-rating_author')[:1]
for i in top_a:
    i.rating_author
    i.author_user.username

# вариант 2:
f"""TOP author: {top_a[0].author_user.username} rating  {top_a[0].rating_author}"""

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье.
tp = Post.objects.order_by('-rating_post')[:1]
f"""{tp[0].create_date:%Y-%m-%d}, {Author.objects.get(id=tp[0].author_user.id).author_user.username}, {tp[0].rating_post}, {tp[0].header_post}, {tp[0].preview()}"""

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
ctp = Comment.objects.filter(post=tp[0].id)
for i in ctp:
    f"""{i.create_datetime}, {i.author_user}, {i.rating_comment}, {i.text_comment}"""

print('tasks comleted')
