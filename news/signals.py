# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст

# импорт моделей
from .models import *


def notify_subscribers_message():
    # Отправка уведомлений о новой новости
    email_recipients = []
    # получаем в виде QuerySet список id категорий поста
    # qs_cat_post_id = Post.objects.get(pk=post.id).category.values('id')
    qs_cat_post_id = post.category.pk
    # затем получаем список id подпсчиков для всех категорий поста
    qs_subs_list_id = CategorySubscriber.objects.filter(throughCategory__in=qs_cat_post_id).values(
        'throughSubscriber__id').distinct()
    # и наконец получаем список неповторяющихся емейлов подписчиков, values_list - выдает именно список list
    qs_email_recipients = User.objects.filter(id__in=qs_subs_list_id).values_list('email', flat=True).distinct()
    email_recipients = qs_email_recipients

    mailing_list = list(
        PostCategory.objects.filter(
            post_id=instance.id
        ).select_related('category').values_list(
            'cat__subscribers__username',
            'cat__subscribers__first_name',
            'cat__subscribers__email',
            'cat__name_category',
        )
    )
    print(f'Список для отправления писем: {mailing_list}')
    print(f'Список для отправления писем: {email_recipients}')

    html_content = render_to_string(
        'post_created.html',
        {
            'post': post,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Новая публикация в вашем любимом разделе.',
        body=post.text_post,
        from_email='gizarir@mail.ru',
        to=email_recipients,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()