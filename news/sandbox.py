# Реализация простого фильтра
from django import template
import string

forbidden_words = ['редиска', 'гад', 'дурак', 'урод', 'пиппит']
register = template.Library()
@register.filter
def hide_forbidden(value: str) -> str:
    result = []
    words = value.split()
    for word in words:
        if word in forbidden_words:
            result.append(f'{word[0]}{"*" * (len(word) - 2)}{word[-1]}')
        else:
            result.append(word)

    return " ".join(result)
#  Тестирование см. ниже в разделе после if __name__

# Пример описания middleWare
# Задание 13.3.1
# Представьте, что у вас есть приложение, которое оптимизировано как для ПК, так и для мобильных устройств.
# Шаблоны для этих версий хранятся в каталогах full/ и mobile/. Гарантируется, что состав шаблонов идентичен,
# отличается лишь содержание.
# Создайте простой middleware, который будет отправлять пользователю соответствующую версию.
# Для включения слоя в ваш проект необходимо вставить этот код в любой .py файл в произвольном месте.
# Вместе с тем этот путь необходимо прописать в файле settings.py в переменной MIDDLEWARE,
# где уже присутствует изначальный список.
# Путь должен оканчиваться именем класса, реализующим ваш промежуточный слой
class MobileOrFullMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # полное описание тут: https://stackoverflow.com/questions/42273319/detect-mobile-devices-with-django-and-python-3
        if request.user_agent.is_mobile:
            prefix = "mobile/"
        else:
            prefix = "full/"
        response.template_name = prefix + response.template_name
        return response




if __name__ == "__main__":
    print(hide_forbidden('Вася редиска пошел дурак на гору и там пиппит'))
    print(string.punctuation)

    context_pre ={
        'key1':'val1',
        'key2': 'val2',
    }

    context_after ={
        'key3':'val3',
        'key4':'val4',
    }

    print(context_pre.items())
    print(dict(list(context_pre.items())))
    print(dict(list(context_pre.items()) + list(context_after.items())))
