from django.urls import path
# Импортируем созданное нами представление
from .views import (
    PostsList, PostDetail, PostsListSearch, PostCreateArticle, PostCreateNew, PostUpdateNew, PostUpdateArticle,
    PostDelete, upgrade_me, add_subscribe, del_subscribe, index_test, IndexTrans, IndexTimezone
)

# Отключено поскольку регистрацию и аутентификацию по заданию необходимо реализовать через библиотеку allauth
# в данном случае была реализация через дженерики
from .views import ProfileUserUpdate

# группа импортов для организации кэширования
from django.views.decorators.cache import cache_page

# -----------Тестирование логирования____________
# import logging
#
# logger_dr = logging.getLogger('django.request')
# logger_cn = logging.getLogger('django')
#
# logger_dr.error("Hello! I'm error in your app. Enjoy:)")
# logger_cn.error("Hello! I'm error in your app. Enjoy:)")
# ----------КОНЕЦ тестирования логирования-----------

urlpatterns = [
    # path('test/', index_test, name='index_test'),
    # path('test/', IndexTrans.as_view(), name='index_test'),
    # path('test/', IndexTimezone.as_view(), name='index_test'),
    path('', cache_page (3 * 1) (PostsList.as_view()), name='home'),
    path('news/', cache_page (3 * 1) (PostsList.as_view()), name='home_news'),
    # path('<int:pk>', cache_page (60 * 5) (PostDetail.as_view()), name='post_detail'), # переключено на API cache
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/search/', PostsListSearch.as_view(), name='posts_list_search'),
    path('news/create/', PostCreateNew.as_view(), name='post_create_new'),
    path('news/<int:pk>/edit/', PostUpdateNew.as_view(), name='post_update_new'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete_new'),
    path('article/create/', PostCreateArticle.as_view(), name='post_create_article'),
    path('article/<int:pk>/edit/', PostUpdateArticle.as_view(), name='post_update_article'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete_article'),
    path('profile/<int:pk>/update/', ProfileUserUpdate.as_view(), name='profile_user_update'),
    path('upgrade/', upgrade_me, name='profile_user_upgrade'),
    path('add_subscribe/<int:pk>/', add_subscribe, name='add_subscribe'),
    path('del_subscribe/<int:pk>/', del_subscribe, name='del_subscribe'),
]
