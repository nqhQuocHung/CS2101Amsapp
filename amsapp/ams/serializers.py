from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'student_id', 'avatar', 'cover_image']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            student_id=validated_data.get('student_id'),
            avatar=validated_data.get('avatar'),
            cover_image=validated_data.get('cover_image')
        )
        user.role = 'alumni'
        user.save()
        return user


class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_verified']

    def update(self, instance, validated_data):
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'created_at', 'updated_at', 'is_comments_locked')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Tạo bài viết mới với người dùng đã xác thực
        user = self.context['request'].user
        post = Post.objects.create(user=user, **validated_data)
        return post