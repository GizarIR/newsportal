# файл нужен только для тестирования вариантов кода и может быть удален
import string

def censor(value):
    censor_list = ['редиска', 'гад', 'дурак']
    if not isinstance(value, str):
        raise TypeError("Цензурирование осуществляется только для объекта типа Str")
    else:
        list_ = value.split(" ")
        for i in range(len(list_)):
            if list_[i].strip(string.punctuation).lower() in censor_list:
                for j in range(1, len(list_[i])):
                    if list_[i][j] not in string.punctuation:
                        list_[i] = f"{list_[i][:j]}*{list_[i][j+1:]}"
        return f'{" ".join(list_)}'

print(censor('Привет Редиска, жаль что ты не дурак... Нехороший человек - редиска!'))
