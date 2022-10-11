from news.models import *
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            # '__all__',
            'id',
            'username',
        ]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    author_user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    class Meta():
        model = Author
        fields =[
            'id',
            'author_user',
            'user_id'
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name_category",
            # "subscribers",
        ]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only = True
    )

    author_user = AuthorSerializer(read_only=True)
    author_user_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only = True
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'author_user',
            'author_user_id',
            'post_type',
            'create_date',
            'category',
            'category_id',
            'header_post',
            'text_post',
            'rating_post',
            'is_created',
        ]

    def create(self, validated_data):
        category = validated_data.pop('category_id', None)
        author_user = validated_data.pop('author_user_id', None)
        post = Post.objects.create(author_user=author_user ,**validated_data)
        post.category.add(category.id)
        post.save()
        # post.category_set.set([categories])
        # student.course_set.set([course])
        # if categories:
        #     for cat in categories:
        #         new_cat, _ = Category.get_or_create(name_category=cat.get('name_category'))
        #         post.category.add(new_cat.id)
        # post.save()
        return post

