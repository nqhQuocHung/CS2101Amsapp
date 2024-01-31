from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


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
