from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostsListSearch, PostCreate


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон, наименование pk можно переопределить
    # через параметр pk_url_kwarg из родительского класса в файле views.py
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsListSearch.as_view(), name='posts_list_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
]
