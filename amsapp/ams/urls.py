from django.urls import path
from .views import register_alumni, VerifyAlumniAPIView

urlpatterns = [
    path('api/register/alumni/', register_alumni, name='api_register_alumni'),
    path('verify-alumni/<int:user_id>/', VerifyAlumniAPIView.as_view(), name='verify-alumni'),
]
