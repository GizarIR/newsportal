from django.urls import path
# Импортируем созданное нами представление
from .views import (
    PostsList, PostDetail, PostsListSearch, PostCreateArticle, PostCreateNew, PostUpdateNew, PostUpdateArticle,
    PostDelete, upgrade_me
)

# Отключено поскольку регистрацию и аутентификацию по заданию необходимо реализовать через библиотеку allauth
# в данном случае была реализация через дженерики
from .views import ProfileUserUpdate


urlpatterns = [
    path('', PostsList.as_view(), name='home'),
    path('news/',PostsList.as_view(), name='home_news'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/search/', PostsListSearch.as_view(), name='posts_list_search'),
    path('news/create/', PostCreateNew.as_view(), name='post_create_new'),
    path('news/<int:pk>/edit/', PostUpdateNew.as_view(), name='post_update_new'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete_new'),
    path('article/create/', PostCreateArticle.as_view(), name='post_create_article'),
    path('article/<int:pk>/edit/', PostUpdateArticle.as_view(), name='post_update_article'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete_article'),
    path('profile/<int:pk>/update/', ProfileUserUpdate.as_view(), name='profile_user_update'),
    path('upgrade/', upgrade_me, name='profile_user_upgrade')
]
