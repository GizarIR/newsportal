# группа импортов для работы сигналов
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая представит наш html в виде строки

# импорт моделей
from .models import Post, PostCategory, CategorySubscriber
from django.contrib.auth.models import User

# импорт задач celery
#  Также необходимо установить Celery, Redis и запустить 4 терминала
# 1 - общий для запуска сервера Redis
# 2 - терминал окружения проекта: python3 manage.py runserver
# 3 - терминал окружения проекта для запуска задач без расписания: celery -A NewsPortal worker -l INFO --concurrency=10
#  где --concurrency - количество процессов, которые могут на нём запускаться
# 4 - (опционально) терминал окружения проекта для запуска задач с расписанием: celery -A NewsPortal beat -l INFO
# где beat м.б. заменен на флаг -B после INFO
from .tasks import send_mails_new_pub


from django.utils.translation import gettext as _


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    """Уведомление подписчиков о выходе новой публикации в категории"""
    post = Post.objects.get(pk=instance.pk)

    if post.is_created:
        subject_email=_(f'A new post in your favorite category') # Новая публикация в вашей любимой категории
    else:
        subject_email = _(f'Changes in the publication {post.header_post} in your favorite category')  #Изменения в публикации {post.header_post} в вашей любимой категории

    # Вариант 2 отправка - писем подписчикам, вариант 1 см во views.py
    mailing_list = []
    mailing_list = list(
        PostCategory.objects.filter(
            throughPost=instance.pk
        ).select_related('category').values_list(
            'throughCategory__subscribers__email',
            'throughCategory__subscribers__username',
            'throughCategory__subscribers__first_name',
            'throughCategory__name_category',
        ).distinct()
    )
    print(_(f'The list for sending mailing_list emails has been prepared for Celery: {mailing_list}')) # Список для отправления писем mailing_list подготовлен для Celery: {mailing_list}

    for subscriber in mailing_list:
        if subscriber[0] is not None:
            html_content = render_to_string(
                'post_created.html',
                {
                    'post': post,
                    'username': subscriber[2] if subscriber[2] else subscriber[1],
                }
            )

            # запускаем асинхронно для каждого отправления
            send_mails_new_pub.delay(post.id, subject_email, [subscriber[0],], html_content)

            # Ниже код ("commented") перенесен в задачи tasks.py для усовершенствования и
            # отправки писем при помощи асинхронной модели с использованием Celery и Redis
            # msg = EmailMultiAlternatives(
            #     subject=subject_email,
            #     body=post.text_post,
            #     from_email='gizarir@mail.ru',
            #     to=[subscriber[0],],
            # )
            # msg.attach_alternative(html_content, "text/html")
            # print(f'Отправка письма подписчику {subscriber[0]}...')
            # msg.send()
    return