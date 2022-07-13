
# >>> from news.models import *
# >>> u1 = User.objects.create_user('user1')
# >>> u2 = User.objects.create_user('user2')
# >>> a1 = Author.objects.create(author_user=u1)
# >>> a2 = Author.objects.create(author_user=u2)
# >>> Author.objects.all()
# <QuerySet [<Author: Author object (1)>, <Author: Author object (2)>]>
# >>> Author.objects.all().values('author_user')
# <QuerySet [{'author_user': 2}, {'author_user': 3}]>
# >>> Author.objects.all().values('id')
# <QuerySet [{'id': 1}, {'id': 2}]>
# >>> User.objects.all().values('username')
# <QuerySet [{'username': 'admin'}, {'username': 'user1'}, {'username': 'user2'}]>
# >>> Category.objects.create(name_category='ИТ')
# <Category: Category object (1)>
# >>> Category.objects.create(name_category='Экономика')
# <Category: Category object (2)>
# >>> Category.objects.create(name_category='Спорт')
# <Category: Category object (3)>
# >>> Category.objects.create(name_category='Искусство')
# <Category: Category object (4)>
# >>> Category.objects.all()
# <QuerySet [<Category: Category object (1)>, <Category: Category object (2)>, <Category: Category object (3)>, <Category: Category object (4)>]>
# >>> Category.objects.all().values('name_category')
# <QuerySet [{'name_category': 'ИТ'}, {'name_category': 'Экономика'}, {'name_category': 'Спорт'}, {'name_category': 'Искусство'}]>
# >>> cat1 = Category.objects.get(id=1)
# >>> p_t1 = Post.article
# >>> p_t1
# 'AR'
#  p1 = Post.objects.create(author_user=a1, post_type=p_t1, header_post="Заголовок первой статьи", text_post="Здесь какой то текст первой статьи")                                                                                                                                                                      ^
# >>> p1.category.add(cat1)
# >>> p1.category.set([Category.objects.get(id=2)])
# >>> p1.category.set([Category.objects.get(id=1)])
# >>> p2 = Post.objects.create(author_user=a2, post_type='AR', header_post="Какой то заголовок второй статьи", text_post="Новый текст второй статьи")
# >>> p2.category.set([Category.objects.get(id=2)])
# >>> p3 = Post.objects.create(author_user=a1, post_type='NW', header_post="Заголовок новости", text_post="Текст простой новости")
# >>> p3.category.add(Category.objects.get(id=3))
# >>> PostCategory.objects.all().values()
# <QuerySet [{'id': 3, 'throughPost_id': 1, 'throughCategory_id': 1}, {'id': 4, 'throughPost_id': 2, 'throughCategory_id': 2}, {'id': 5, 'throughPost_id': 3, 'throughCategory_id': 3}]>
# >>> p3.category.add(Category.objects.get(id=4))
# >>> p3.category.all().values('name_category')
# <QuerySet [{'name_category': 'Спорт'}, {'name_category': 'Искусство'}]>
# >>> cat3=Category.objects.get(id=3)
# >>> cat3.post_set.all().values('header_post')
# <QuerySet [{'header_post': 'Заголовок новости'}]>
# >>> c1=Comment.objects.create(post=p1, author_user=u1, text_comment="Очень классная статья")
# >>> c2=Comment.objects.create(post=p2, author_user=u1, text_comment="Так себе пост")
# >>> c3=Comment.objects.create(post=p3, author_user=u2, text_comment="Автар жжет")
# >>> c4=Comment.objects.create(post=p3, author_user=u1, text_comment="Как же хорошо все выглядит, а на самом деле...")
# >>> Comment.objects.filter(author_user=u1).values('rating_comment')
# <QuerySet [{'rating_comment': 0}, {'rating_comment': 0}, {'rating_comment': 0}]>
# >>> u1.comment_set.all()
# <QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>, <Comment: Comment object (4)>]>
# >>> p1.like()
# >>> p1.rating_post
# 1
# >>> p1.like()
# >>> p1.rating_post
# 2
# >>> p2.rating_post
# 0
# >>> p2.dislike()
# >>> p2.rating_post
# -1
# >>> p2.dislike()
# >>> p2.dislike()
# >>> p2.rating_post
# -3
# >>> p3.like()
# >>> p3.like()
# >>> p3.like()
# >>> p3.like()
# >>> p3.rating_post
# 4
# >>> p1.preview()
# 'Здесь какой то текст первой статьи ...'
# >>> p2.preview()
# 'Новый текст второй статьи ...'
# >>> c1.like()
# >>> c1.like()
# >>> c1.like()
# >>> c1.like()
# >>> c1.rating_comment
# 4
# >>> c2.dislike()
# >>> c2.dislike()
# >>> c2.dislike()
# >>> c2.dislike()
# >>> c2.rating_comment
# -4
# >>> c3.like()
# >>> c3.like()
# >>> c4.dislike()
# >>> c4.dislike()
# >>> c4.rating_comment
# -2
# >>> c4.dislike()
# >>>
# >>> c5=Comment.objects.create(post=p1, author_user=User.objects.get(id=1), text_comment="А вот и комментарий и не от автора")
# >>> c5.like()
# >>> c5.like()
# >>> c5.like()
# >>> c5.like()
# >>> c5.like()
