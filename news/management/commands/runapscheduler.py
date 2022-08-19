import logging
import smtplib

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# импорты необходимые для запуска еженедельной рассылки
from news.models import Post, Category, PostCategory, CategorySubscriber
import datetime
from datetime import datetime, timedelta, timezone
from django.core.mail import EmailMultiAlternatives # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая представит наш html в виде строки



logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...

    class PostForEmail:
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
        d_from = datetime.now(tz=timezone.utc).date()
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
        posts_for_email = []
        for post in posts_list:
            posts_for_email.append(PostForEmail(post[0], post[1], post[2]))
        print('Cписок постов для рассылки  подготовлен')
        # print(f'С{d_to} по {d_from} такой список постов:')
        # for elem in posts_for_email:
        #     print(elem.pk, elem.header, elem.text)

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
                msg = EmailMultiAlternatives(
                    subject=f'Еженедельная рассылка новостей в твоей любимой категории: {cat.name_category}',
                    body=f'Еженедельная рассылка',
                    from_email='gizarir@mail.ru',
                    to=[subscriber[0], ],
                )
                msg.attach_alternative(html_content, "text/html")

                print(f'Отправка письма подписчику {subscriber[0]} категории {cat.name_category}...')
                try:
                    msg.send()
                except smtplib.SMTPRecipientsRefused:
                    print(f'Ошибка отправки письма по адресу: {subscriber[0]}')

    return print('Еженедельная рассылка завершена успешно.')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day="*/7"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            # для тестировани используй trigger=CronTrigger(second="*/10")
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job' - send mails to subscribers.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")