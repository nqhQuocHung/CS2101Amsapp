from django.contrib.auth import get_user_model
from rest_framework import serializers
from.models import Post, Comment, Reaction, Survey, SurveyResponse, Notification, Group, GroupMember, Statistic, EmailQueue, Question, Choice

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
        user.save()
        return user


class UserVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_verified']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'post', 'user', 'type']
        read_only_fields = ('user',)


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    reactions = ReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'images', 'created_at', 'content', 'comments', 'reactions']

    def create(self, validated_data):
        # Thêm người dùng hiện tại vào dữ liệu đã xác thực trước khi tạo Post
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = '__all__'


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = '__all__'


class EmailQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailQueue
        fields = '__all__'


class PasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class StatsSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    quarter = serializers.IntegerField()
    user_count = serializers.IntegerField()
    post_count = serializers.IntegerField()