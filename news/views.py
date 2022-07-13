from django.shortcuts import render

# Create your views here.

# Code for debug models.py add-news. It can be remove.
# from news.models import *
# from django.contrib.auth.models import User
# from django.db.models import Aggregate, Sum
#
# admin = User.objects.get(id=1)
# u1 = User.objects.get(id=2)
# u2 = User.objects.get(id=3)
# a1 = Author.objects.get(id=1)
# a2 = Author.objects.get(id=2)
# p1 = Post.objects.get(id=1)
# p2 = Post.objects.get(id=2)
# p3 = Post.objects.get(id=3)
# c1 = Comment.objects.get(id=1)
# c2 = Comment.objects.get(id=2)
# c3 = Comment.objects.get(id=3)
# c4 = Comment.objects.get(id=4)
# c5 = Comment.objects.get(id=5)
# p1.like()
# p1.like()
# p1.rating_post
# p2.dislike()
# p2.dislike()
# p2.dislike()
# p2.rating_post
# p3.like()
# p3.like()
# p3.like()
# p3.like()
# p3.rating_post
# c1.like()
# c1.like()
# c1.like()
# c1.like()
# c1.rating_comment
# c2.dislike()
# c2.dislike()
# c2.dislike()
# c2.dislike()
# c2.rating_comment
# c3.like()
# c3.like()
# c4.dislike()
# c4.dislike()
# c4.dislike()
# c4.rating_comment
# c5.like()
# c5.like()
# c5.like()
# c5.like()
# c5.like()
# c5.rating_comment

Post.objects.filter(author_user=a1.id).aggregate(Sum('rating_post'))['rating_post__sum']
Comment.objects.filter(author_user=admin.id).aggregate(Sum('rating_comment'))['rating_comment__sum']
Comment.objects.filter(post__author_user=a1.id).aggregate(Sum('rating_comment'))['rating_comment__sum']

