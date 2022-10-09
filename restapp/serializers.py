from news.models import *
from rest_framework import serializers

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
        # many=True,
        queryset=Category.objects.all(),
        write_only = True
    )

    # categories =

    class Meta:
        model = Post
        fields = [
            'id',
            # 'author_user',
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
        category = validated_data.pop('category_id')
        post = Post.objects.create(category=category,**validated_data)
        return post

