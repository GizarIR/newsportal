from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions

from .serializers import *
from news.models import *

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAuthenticatedOrReadOnly

# Create your views here.

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS # кортеж методов GET HEAD OPTIONS



from rest_framework.decorators import action
from rest_framework.response import Response
# Для тестирования поведения разных реализация
# class PostViewset(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     # def get_permissions(self):
#     #     """
#     #     Instantiates and returns the list of permissions that this view requires.
#     #     """
#     #     if self.action in ('list', 'retrieve'):
#     #         permission_classes = []
#     #     elif self.action in ('create', 'update', 'partial_update', 'destroy'):
#     #         permission_classes = [IsAuthenticated]
#     #     else:
#     #         permission_classes = [IsAuthenticated]
#     #     return [permission() for permission in permission_classes]
#     @action(detail=False, methods=['get'],  permission_classes=[IsAuthenticated])
#     def get_list (self, request):
#         recent_posts = Post.objects.all()
#         page = self.paginate_queryset(recent_posts)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(recent_posts, many=True)
#         return Response(serializer.data)

class NewsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().filter(post_type='NW')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated|ReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all().filter(post_type='NW')
        category_id = self.request.query_params.get('category_id', None)
        author_user_id = self.request.query_params.get('author_user_id', None)
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)
        if author_user_id is not None:
            queryset = queryset.filter(author_user_id=author_user_id)
        return queryset


class ArticleViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all().filter(post_type='AR')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all().filter(post_type='AR')
        category_id = self.request.query_params.get('category_id', None)
        author_user_id = self.request.query_params.get('author_user_id', None)
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)
        if author_user_id is not None:
            queryset = queryset.filter(author_user_id=author_user_id)
        return queryset

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated | ReadOnly]

class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

