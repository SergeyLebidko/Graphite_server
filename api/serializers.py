from rest_framework import serializers

from utils import to_hash, create_random_string
from .models import Account, Post, Comment, PostLike


class AccountSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = serializers.ModelSerializer.to_representation(self, instance)
        del result['login']
        del result['password']
        return result

    def create(self, validated_data):
        password = validated_data['password']
        validated_data['password'] = to_hash(password)
        return serializers.ModelSerializer.create(self, validated_data)

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar')
        if avatar:
            avatar.name = f'avatar_{instance.pk}_{create_random_string(5)}.jpg'
            instance.avatar.delete()
            instance.save()
        return serializers.ModelSerializer.update(self, instance, validated_data)

    class Meta:
        model = Account
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        comment_count = Comment.objects.filter(post=instance).count()
        like_count = PostLike.objects.filter(post=instance).count()
        result = serializers.ModelSerializer.to_representation(self, instance)
        result['comment_count'] = comment_count
        result['like_count'] = like_count
        return result

    class Meta:
        model = Post
        fields = '__all__'
