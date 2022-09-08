from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    help = 'Команда postsdelete удаляет статьи и новости из соответствующей категории'
    missing_args_message = 'Недостаточно аргументов'
    #уведомлять ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)
    requires_migrations_checks = True

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        str_cat = " ".join(options['category'])
        self.stdout.readable()
        # спрашиваем пользователя действительно ли он хочет удалить все товары
        self.stdout.write(f'Вы действительно хотите удалить статьи и новости в категории(ях) {str_cat} ? yes/no')
        answer = input()  # считываем подтверждение

        if answer != 'yes':
            # в случае неправильного подтверждения, говорим что в доступе отказано
            self.stdout.write(self.style.ERROR('Операция не подтверждена'))
        else:
            # в случае подтверждения действительно удаляем все товары
            try:
                # Вариант 1
                # qs_cat_list_id=Category.objects.filter(name_category__in=options['category']).values('id')
                # Post.objects.filter(category__in=qs_cat_list_id).delete()
                # Вариант 2
                Post.objects.filter(category__name_category__in=options['category']).delete()
                self.stdout.write(self.style.SUCCESS(f'Публикации успешно удалены из категорий(ии) {str_cat}!'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f' Категории не найдены!'))
                # raise CommandError("При удалении публикаций произошла ошибка!")
        return


