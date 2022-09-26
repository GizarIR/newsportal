from django import forms
from django.core.exceptions import ValidationError

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.contrib.auth.models import User
from .models import Post

from django.utils.translation import gettext as _

class PostFormArticle(forms.ModelForm):
    header_post = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'author_user',
            # 'post_type',
            # 'create_date',
            'category',
            'header_post',
            'text_post',
            'rating_post',
        ]

    def clean(self):
        cleaned_data = super().clean()
        header_post = cleaned_data.get('header_post')
        text_post = cleaned_data.get('text_post')

        if header_post == text_post:
            raise ValidationError(
                _('The title of the article should not completely coincide with the text of the article.') # Заголовок статьи не должен полностью совпадать с текстом статьи.
            )

        return cleaned_data


class PostFormNew(forms.ModelForm):
    header_post = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            # 'author_user',
            # 'post_type',
            # 'create_date',
            'category',
            'header_post',
            'text_post',
            'rating_post',
        ]

    def clean_text_post(self):
        text_post = self.cleaned_data['text_post']
        if len(text_post) > 256:
            raise ValidationError(
                _('The text of the news can not be more than 256 characters.') # Текст новости не может быть больше 256 символов.
            )
        return text_post

    def clean(self):
        cleaned_data = super().clean()
        header_post = cleaned_data.get('header_post')
        text_post = cleaned_data.get('text_post')

        if header_post == text_post:
            raise ValidationError(
                _('The headline of the news should not completely coincide with the text of the news.') # Заголовок новости не должен полностью совпадать с текстом новости.
            )

        return cleaned_data

# Отключено поскольку регистрацию и аутентификацию по заданию необходимо реализовать через библиотеку allauth
class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            # 'password',
            'groups',

        ]


class CommonSignupForm(SignupForm):
    """Функция добавлена при настройке allauth, необходима для реализации механизма:
    при сохраниении зарегистрированного пользователя его автоматически определяют в группу common.
    Данная группа была создана в админке"""
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group=Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user

