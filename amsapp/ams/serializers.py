from django.contrib.auth import get_user_model
from rest_framework import serializers
from.models import Post

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)
    cover_image = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'student_id', 'avatar', 'cover_image', 'is_verified')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            student_id=validated_data['student_id'],
            avatar=validated_data['avatar'],
            cover_image=validated_data['cover_image'],
            is_verified=False  # Tùy vào logic xác thực của bạn
        )
        user.role = 'alumi'
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  # Hoặc liệt kê các trường cụ thể: ['id', 'user', 'content', 'created_at', 'updated_at', 'is_comments_locked']
        read_only_fields = ('user', 'created_at', 'updated_at')  # Những trường này không được thay đổi bởi người dùng
