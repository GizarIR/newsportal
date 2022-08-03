from django import forms
from django.core.exceptions import ValidationError

from .models import Post

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
                'Заголовок статьи не должен полностью совпадать с текстом статьи.'
            )

        return cleaned_data


class PostFormNew(forms.ModelForm):
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

    def clean_text_post(self):
        text_post = self.cleaned_data['text_post']
        if len(text_post) > 256:
            raise ValidationError(
                'Текст новости не может быть больше 256 символов.'
            )
        return text_post

    def clean(self):
        cleaned_data = super().clean()
        header_post = cleaned_data.get('header_post')
        text_post = cleaned_data.get('text_post')

        if header_post == text_post:
            raise ValidationError(
                'Заголовок новости не должен полностью совпадать с текстом новости.'
            )

        return cleaned_data
