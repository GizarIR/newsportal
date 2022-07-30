# from models import *
# from django.contrib.auth.models import User
# from django.db.models import Aggregate, Sum
#
# a1 = Author.objects.get(id=1)
# a2 = Author.objects.get(id=2)
#

# p1 = Post.objects.create(author_user=a1, post_type="AR", header_post="Заголовок", text_post="Текст для проверки пагинации")
# p1.category.set([Category.objects.get(id=1)])
from random import randrange

commands_lines = ''
for i in range(1, 10):
    str_p = f"p{i} = Post.objects.create(author_user=a{randrange(1, 3)}, post_type=\'AR\', header_post=\'Заголовок {i}\', text_post=\'Текст статьи {i} для проверки пагинации\'\n"
    str_c = f'p{i}.category.set([Category.objects.get(id={randrange(1, 5)})])\n'
    # print(str_p)
    # print(str_c)
    commands_lines += str_p
    commands_lines += str_c

print(commands_lines)
