import smtplib
from datetime import datetime, timedelta

from celery import shared_task


# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая представит наш html в виде строки

# группа импорта моделей
from .models import Post, Category, PostCategory


@shared_task
def send_mails_new_pub(post_pk, subject_email, subscriber, html_content):
    post = Post.objects.get(pk=post_pk)

    msg = EmailMultiAlternatives(
        subject=subject_email,
        body=post.text_post,
        from_email='gizarir@mail.ru',
        to=[subscriber[0], ],
    )
    msg.attach_alternative(html_content, "text/html")

    print(f'Отправка письма подписчику {subscriber[0]}...')

    msg.send()
    return

@shared_task
def send_news_week(cat, subscriber, html_content,):
    msg = EmailMultiAlternatives(
        subject=f'Еженедельная рассылка новостей в твоей любимой категории: {cat}',
        body=f'Еженедельная рассылка',
        from_email='gizarir@mail.ru',
        to=[subscriber[0], ],
    )
    msg.attach_alternative(html_content, "text/html")

    print(f'Отправка письма подписчику {subscriber[0]} категории {cat}...')
    try:
        msg.send()
    except smtplib.SMTPRecipientsRefused:
        print(f'Error: Ошибка отправки письма по адресу: {subscriber[0]}')
    return

@shared_task
def news_week():
    class PostForEmail:
        """Класс для создания объектов для передачи в шаблон  """
        def __init__(self, pk, header, text):
            self.pk = pk
            self.header = header
            self.text = text

    print('Запуск еженедельной рассылки новостей')
    # получим список категорий
    qs_cat_list = Category.objects.all()
    # для каждой категории создадим список рассылки, список публикаций и отправляем почту
    for cat in qs_cat_list:
        # готовим список рассылки
        mailing_list = []
        mailing_list = list(
            PostCategory.objects.filter(
                throughCategory=cat.pk
            ).select_related('category').values_list(
                'throughCategory__subscribers__email',
                'throughCategory__subscribers__username',
                'throughCategory__subscribers__first_name',
                'throughCategory__name_category',
            ).distinct()
        )
        print(f'Список рассылки mailing_list: {mailing_list} для категории {cat.name_category}')

        # Вычисляем даты для прошедшей недели
        # d_from = datetime.now(tz=timezone.utc).date()
        d_from = datetime.now().date()
        d_to = d_from - timedelta(days=7)

        # готовим список публикаций за указанные даты
        posts_list = list(
            PostCategory.objects.filter(
                throughCategory=cat.pk
            ).select_related('post').values_list(
                'throughPost__pk',
                'throughPost__header_post',
                'throughPost__text_post',
            ).filter(
                throughPost__create_date__range=(d_to, d_from)
            ).distinct()
        )
        # преобразуем в спсисок объектов для удобной передачи в шаблон
        posts_for_email = []
        for post in posts_list:
            posts_for_email.append(PostForEmail(post[0], post[1], post[2]))
        print('Список постов для рассылки  подготовлен')


        # отправляем почту
        for subscriber in mailing_list:
            if subscriber[0] is not None:
                html_content = render_to_string(
                    'posts_week.html',
                    {
                        'posts': posts_for_email,
                        'username': subscriber[2] if subscriber[2] else subscriber[1],
                    }
                )

                # отправляем каждое письмо в отдельном потоке
                send_news_week.delay(cat.name_category, [subscriber[0],], html_content)

                # msg = EmailMultiAlternatives(
                #     subject=f'Еженедельная рассылка новостей в твоей любимой категории: {cat.name_category}',
                #     body=f'Еженедельная рассылка',
                #     from_email='gizarir@mail.ru',
                #     to=[subscriber[0], ],
                # )
                # msg.attach_alternative(html_content, "text/html")
                #
                # print(f'Отправка письма подписчику {subscriber[0]} категории {cat.name_category}...')
                # try:
                #     msg.send()
                # except smtplib.SMTPRecipientsRefused:
                #     print(f'Ошибка отправки письма по адресу: {subscriber[0]}')

    return print('Еженедельная рассылка завершена успешно.')