from django import template
import string


CENSOR_LIST = ['редиска', 'гад', 'дурак', 'урод', 'пиzдит']

register = template.Library()

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError("Цензура осуществляется только для объекта типа строка (str)")
    else:
        list_ = value.split(" ")
        for i in range(len(list_)):
            if list_[i].strip(string.punctuation).lower() in CENSOR_LIST:
                for j in range(1, len(list_[i])):
                    if list_[i][j] not in string.punctuation:
                        list_[i] = f"{list_[i][:j]}*{list_[i][j+1:]}"
        return f'{" ".join(list_)}'

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
