from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name_category',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ( 'header_post', 'text_post',)
