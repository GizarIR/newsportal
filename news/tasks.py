from celery import shared_task


# группа импортов для реализации рассылки подписчикам
from django.core.mail import EmailMultiAlternatives # импортируем класс для создания объекта письма с html
# from django.template.loader import render_to_string # импортируем функцию, которая представит наш html в виде строки

# группа импорта моделей
from .models import Post

@shared_task
def send_mails_new_pub(post_pk, subject_email, subscriber, html_content):
    # time.sleep(10)
    # print("Hello, here we will send mails to subscribers!")
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