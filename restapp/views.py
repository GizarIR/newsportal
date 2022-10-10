from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *
from news.models import *

# Create your views here.

class NewsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().filter(post_type='NW')
    serializer_class = PostSerializer

class ArticleViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().filter(post_type='AR')
    serializer_class = PostSerializer

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

