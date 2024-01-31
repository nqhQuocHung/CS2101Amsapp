from django.contrib import admin
from .models import User, Post, Comment, Reaction, Survey, SurveyResponse, Notification, Group, GroupMember, Statistic, EmailQueue

# Đăng ký mô hình User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_verified']
    search_fields = ['username', 'email', 'student_id']

# Đăng ký các mô hình khác
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Survey)
admin.site.register(SurveyResponse)
admin.site.register(Notification)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Statistic)
admin.site.register(EmailQueue)
