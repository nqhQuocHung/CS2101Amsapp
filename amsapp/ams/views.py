
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, viewsets, generics
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from .serializers import (UserSerializer, PostSerializer, PasswordSerializer, CommentSerializer
                            , ReactionSerializer, SurveySerializer, SurveyResponseSerializer,
                          QuestionSerializer, ChoiceSerializer, NotificationSerializer, GroupSerializer,GroupMemberSerializer, StatsSerializer)
from oauth2_provider.views import TokenView
from django.views.decorators.debug import sensitive_post_parameters
import json
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .models import User, Post, Comment, Reaction, Survey, SurveyResponse, Question, Choice, Notification, Group, GroupMember
from . import perms, paginators, signal
from django.db.models import Count
import datetime


class LoginView(TokenView):

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        user = authenticate(username=username, password=password)

        if user and user.role == role:
            # if user.role == 'lecturer' and not user.password_change:
            #     # Kiểm tra nếu user đã được tạo trong vòng 24 giờ
            #     if user.created_at and datetime.now() - user.created_at >= datetime.timedelta(hours=24):
            #         # Cập nhật trường is_active thành False
            #         user.is_active = False
            #         user.save()
            if role == 'alumni' and not user.is_verified:
                return HttpResponse(content="Tài khoản alumni chưa được xác thực", status=status.HTTP_401_UNAUTHORIZED)
            request.POST = request.POST.copy()
            # pdb.set_trace()
            if not user.is_active:
                return HttpResponse(content="Tài khoản của bạn bị khóa, vui lòng liên hệ quản trị viên để mở khóa!", status=status.HTTP_400_BAD_REQUEST)
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
    queryset = User.objects.filter(is_active=True).all()

    def get_permissions(self):
        if self.action == "change_password" or self.action == "add_post":
            return [permissions.IsAuthenticated()]
        if self.action == "verify" or self.action == "unverified_alumni":
            return [permissions.IsAdminUser()]
        if self.action == "create":
            # Lấy dữ liệu từ request.
            data = self.request.data

            # Tạo một instance của serializer với dữ liệu được cung cấp.
            serializer = self.get_serializer(data=data)

            # Kiểm tra dữ liệu có hợp lệ không.
            if serializer.is_valid(raise_exception=False):
                # Kiểm tra giá trị của role từ dữ liệu đã được validate.
                if serializer.validated_data.get('role') == "lecturer":
                    return [permissions.IsAdminUser()]
        return super().get_permissions()  # sử dụng permissions mặc định cho các action khác

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Đăng ký thành công!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def unverified_alumni(self, request):
        unverified_alumni = self.queryset.filter(role='alumni', is_verified=False)
        serializer = self.serializer_class(unverified_alumni, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def verify(self, request, pk=None):
        user = self.get_object()
        user.is_verified = True
        if user.save():
            signal.send_mail_confirmation()
        return Response({"message": "User has been verified successfully!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_post(self, request):
        # Lấy người dùng hiện tại từ request
        user = request.user

        # Tạo serializer với dữ liệu từ request và đặt người dùng hiện tại làm 'user' cho bài viết
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save(user=user)
            # Trả về response chứa dữ liệu của bài viết mới được tạo
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def list_posts(self, request):
        # Lấy người dùng hiện tại từ request (người dùng đang đăng nhập)
        user = request.user
        # Lọc các bài viết của người dùng hiện tại
        posts = Post.objects.filter(user=user)
        # Serialize danh sách bài viết
        serializer = PostSerializer(posts, many=True)
        # Trả về response chứa danh sách bài viết
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='current-user', url_name='current-user', detail=False)
    def current_user(self, request):
        if request.user.is_authenticated:  # Kiểm tra xem người dùng đã xác thực chưa
            return Response(self.get_serializer(request.user).data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=False)
    def change_password(self, request):
        user = request.user  # Lấy người dùng hiện tại từ request
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Kiểm tra mật khẩu cũ có chính xác không
            if not user.check_password(old_password):
                return Response({'old_password': ['Mật khẩu cũ không chính xác.']}, status=status.HTTP_400_BAD_REQUEST)

            # Đặt mật khẩu mới và lưu người dùng
            user.set_password(new_password)
            user.password_change = True
            user.save()

            return Response({'status': 'success', 'message': 'Mật khẩu đã được thay đổi thành công.'},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.UpdateAPIView,
                  generics.RetrieveAPIView,
                  generics.DestroyAPIView):
    queryset = Post.objects.filter(active=True).all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated()]
    pagination_class = paginators.PostPaginator

    def get_permissions(self):
        if self.action in ['update', 'block_comments_post']:
            return [perms.IsOwner()]
        if self.action.__eq__('destroy'):
            return [perms.IsOwner(), permissions.IsAdminUser()]
        if self.action == "create" or self.action == "add_comment":
            return [permissions.IsAuthenticated()]
        return self.permission_classes

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"Tạo thành công!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='block_comment')
    def block_comments_post(self, request, pk):
        post = self.get_object()
        post.is_comments_locked = not post.comment_blocked
        post.save()

        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        post = self.get_object()

        # Kiểm tra xem bài viết có bị khóa bình luận hay không
        if post.is_comments_locked:
            return Response({"message": "Comments are locked for this post"}, status=status.HTTP_403_FORBIDDEN)

        # Tiếp tục tạo bình luận nếu bài viết không bị khóa bình luận
        c = Comment.objects.create(user=request.user, post=post, content=request.data.get('content'))
        return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True)
    def list_comments(self, request, pk):
        comments = self.get_object().comment_set.filter(active=True)

        return Response(CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    from rest_framework import status

    @action(methods=['post'], detail=True)
    def delete_comment(self, request, pk):
        post = self.get_object()
        comment_id = request.data.get('comment_id')

        if not comment_id:
            return Response({"message": "Vui lòng cung cấp ID của bình luận."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = post.comment_set.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "Bình luận không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == post.user or request.user == comment.user:
            comment.active = False
            comment.save()
            return Response({"message": "Bình luận đã được xóa."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Bạn không có quyền xóa bình luận này."}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=True)
    def list_reactions(self, request, pk):
        reactions = self.get_object().reaction_set.filter(active=True)
        return Response(ReactionSerializer(reactions, many=True).data,
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_reaction(self, request, pk=None):
        post = self.get_object()
        serializer = ReactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Kiểm tra xem người dùng đã thêm phản ứng cho bài viết này chưa
            existing_reaction = Reaction.objects.filter(post=post, user=request.user,
                                                        type=serializer.validated_data['type'])
            if existing_reaction.exists():
                return Response({"message": "Bạn đã thêm phản ứng này rồi."}, status=status.HTTP_400_BAD_REQUEST)

            # Thêm phản ứng mới
            Reaction.objects.create(post=post, user=request.user, type=serializer.validated_data['type'])
            return Response({"message": "Phản ứng đã được thêm."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet,
                     generics.UpdateAPIView,
                     generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True).all()
    serializer_class = CommentSerializer
    permission_classes = [perms.IsOwner]

    def get_permissions(self):
        if self.action == 'destroy':
            return [perms.IsCommentAuthorOrPostAuthor()]
        return self.permission_classes


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [perms.IsAdminUserOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Tạo thành công!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, url_path='add-question')
    def add_question(self, request, pk=None):
        survey = self.get_object()
        data = request.data
        question = Question.objects.create(survey=survey, content=data.get('content'))
        choices_data = data.get('choices', [])
        for choice_data in choices_data:
            Choice.objects.create(question=question, content=choice_data)
        return Response({"message": "Question added successfully."})


class SurveyResponseViewSet(viewsets.ViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer

    @action(methods=['post'], detail=False, url_path='submit-response')
    def submit_response(self, request):
        data = request.data
        user = request.user
        survey = data.get('survey')
        responses = data.get('responses', [])
        for response in responses:
            question = response.get('question')
            choice = response.get('choice')
            SurveyResponse.objects.create(survey=survey, user=user, question=question, choice=choice)
        return Response({"message": "Survey response submitted successfully."})


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]  # Chỉ cho phép admin

    def create_and_send(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()
            # Gửi email tới tất cả thành viên trong nhóm
            group_id = request.data.get('group_id')
            if group_id:
                members = GroupMember.objects.filter(group_id=group_id).select_related('user')
                emails = [member.user.email for member in members if member.user.email]
                send_mail(
                    'Thông Báo Mới',
                    notification.content,
                    'hungmt2426@gmail.com',
                    emails,
                    fail_silently=False,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        return super(GroupViewSet, self).create(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def add_member(self, request, pk=None):
        group = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "Người dùng không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra xem người dùng đã là thành viên của nhóm chưa
        if GroupMember.objects.filter(group=group, user=user).exists():
            return Response({"error": "Người dùng đã là thành viên của nhóm."}, status=status.HTTP_400_BAD_REQUEST)

        # Thêm người dùng vào nhóm
        group_member = GroupMember.objects.create(group=group, user=user)
        return Response(GroupMemberSerializer(group_member).data, status=status.HTTP_201_CREATED)


class StatsViewSet(viewsets.ViewSet):

    def list(self, request):
        stats_data = self.get_stats_data()
        serializer = StatsSerializer(stats_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_stats_data(self):
        # Lấy dữ liệu thống kê từ cơ sở dữ liệu
        # Ví dụ: Đếm số lượng người dùng và bài viết theo năm, tháng hoặc quý
        current_year = datetime.datetime.now().year
        stats_data = []

        # Thống kê số lượng người dùng và bài viết theo năm
        for year in range(current_year - 4, current_year + 1):  # Thống kê 5 năm gần đây
            user_count = User.objects.filter(created_at__year=year).count()
            post_count = Post.objects.filter(created_at__year=year).count()
            stats_data.append({
                'year': year,
                'user_count': user_count,
                'post_count': post_count
            })

        return stats_data


