import string

def censor(value):
    censor_list = ['редиска', 'гад', 'дурак']
    if not isinstance(value, str):
        raise TypeError("Цензурирование осуществляется только для объекта типа Str")
    else:
        list_ = value.split(" ")
        for i in range(len(list_)):
            if list_[i].strip(string.punctuation).lower() in censor_list:
                if len(list_[i].strip(string.punctuation)) != len(list_[i]):
                    list_[i] = f"{list_[i][0]}{(len(list_[i])-2) * '*'}{list_[i][-1]}"
                else:
                    list_[i] = f"{list_[i][0]}{(len(list_[i]) - 1) * '*'}"
        return f'{" ".join(list_)}'

print(censor('Привет Редиска, жаль что ты не дурак... Нехороший человек - редиска!'))
