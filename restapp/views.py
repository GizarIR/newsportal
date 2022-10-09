from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *
from news.models import *

# Create your views here.

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer