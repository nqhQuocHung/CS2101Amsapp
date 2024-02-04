from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.conf import settings


class User(AbstractUser):
    USER_TYPES = [
        ('alumni', 'Alumni'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin')
    ]
    role = models.CharField(max_length=20, choices=USER_TYPES, default='alumni')
    student_id = models.CharField(max_length=20, null=True, blank=True)
    avatar = CloudinaryField('avatar', null=True, blank=True)
    cover_image = CloudinaryField('cover_image', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.role == 'lecturer':  # Kiểm tra nếu là tài khoản mới và là giảng viên
            self.set_password(settings.PASSWORD_LECTURER_DEFAULT)  # Đặt mật khẩu mặc định
        super().save(*args, **kwargs)
        if self.role == 'alumni' and not self.student_id and not self.is_superuser:
            raise ValueError("Student ID is required for alumni")
        super().save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_comments_locked = models.BooleanField(default=False)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)  # Like, Haha, Heart, etc.


class Survey(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField()


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)


class Statistic(models.Model):
    metric = models.CharField(max_length=50)
    value = models.IntegerField()
    date = models.DateField()


class EmailQueue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_address = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    status = models.CharField(max_length=10)  # Pending, Sent, Failed
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
