# Реализация простого фильтра
from django import template
import string

forbidden_words = ['редиска', 'гад', 'дурак', 'урод', 'пиzдит']
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

# Пример описания middleWare
class MobileOrFullMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.mobile:
            prefix = "mobile/"
        else:
            prefix = "full/"
        response.template_name = prefix + response.template_name
        return response

if __name__ == "__main__":
    print(hide_forbidden('Вася редиска пошел дурак на гору и там пиzдит'))
    print(string.punctuation)
