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
from .tasks import send_mails_new_pub


# @receiver(m2m_changed, sender=PostCategory)
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    # Ниже код ("commented") организации уведомления о новой публикации подписчиков, который был реализован
    # только на сигналах. В дальнейшем часть кода был перенесен в задачи tasks.py для усовершенствования и
    # отправки писем при помощи асинхронной модели

    post = Post.objects.get(pk=instance.pk)

    if post.is_created:
        subject_email=f'Новая публикация в вашей любимой категории'
    else:
        subject_email = f'Изменения в публикации {post.header_post} в вашей любимой категории'

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
    print(f'Список для отправления писем mailing_list подготовлен для Celery: {mailing_list}')

    for subscriber in mailing_list:
        if subscriber[0] is not None:
            html_content = render_to_string(
                'post_created.html',
                {
                    'post': post,
                    'username': subscriber[2] if subscriber[2] else subscriber[1],
                }
            )
            send_mails_new_pub.delay(post.id, subject_email, [subscriber[0],], html_content)

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