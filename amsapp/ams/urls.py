from django.urls import path
from .views import register_alumni, UserVerificationView, PostCreateView

urlpatterns = [
    path('api/register/alumni/', register_alumni, name='api_register_alumni'),
    path('api/user/verify/<int:pk>/', UserVerificationView.as_view(), name='user-verify'),
    path('api/posts/', PostCreateView.as_view(), name='create-post'),
]