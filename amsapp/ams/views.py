
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Post
from .serializers import UserSerializer, PostSerializer
from oauth2_provider.views import TokenView
from django.views.decorators.debug import sensitive_post_parameters
import json
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse


class LoginView(TokenView):

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        user = authenticate(username=username, password=password)
        if user and user.role == role:
            request.POST = request.POST.copy()
            # pdb.set_trace()

            # Add application credientials
            request.POST.update({
                'grant_type': 'password',
                'username': username,
                'password': password,
                'client_id': settings.CLIENT_ID,
                'client_secret': settings.CLIENT_SECRET
            })
            return super().post(request)
        return HttpResponse(content="Khong tim thay tai khoan", status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cựu sinh viên đã đăng ký thành công!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Chỉ cho phép quản trị viên truy cập

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_verified=False)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        user = get_object_or_404(self.get_queryset(), pk=pk)
        user.is_verified = True
        user.save()
        return Response({"message": "Tài khoản đã được xác thực thành công."}, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Gán người dùng đăng nhập hiện tại là tác giả của bài viết