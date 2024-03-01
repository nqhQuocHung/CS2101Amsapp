from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, LoginView, PostViewSet, CommentViewSet, SurveyViewSet, SurveyResponseViewSet,StatsViewSet
                        ,NotificationViewSet, GroupViewSet)
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'surveys', SurveyViewSet, basename='surveys')
router.register(r'survey-responses', SurveyResponseViewSet, basename='survey-responses')
router.register(r'notifications', NotificationViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'stats', StatsViewSet, basename='stats')
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
