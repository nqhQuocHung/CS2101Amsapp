from datetime import datetime, timedelta
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class LecturerPasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user
        now_with_offset = timezone.now()
        # Kiểm tra người dùng đã đăng nhập, có vai trò là lecturer và chưa thay đổi mật khẩu
        if user.is_authenticated and hasattr(user, 'role') and user.role == 'lecturer' and not user.password_change:
            # Kiểm tra xem đã qua 24 giờ kể từ khi tài khoản được tạo chưa
            if user.created_at and now_with_offset - user.created_at > timedelta(hours=24):
                user.is_active = False
                user.save()
                # Trả về thông báo cho người dùng
                return HttpResponse("Tài khoản của bạn đã bị khóa do không thay đổi mật khẩu sau 24 giờ kể từ khi tạo tài khoản. "
                                    "Vui lòng liên hệ với quản trị viên để được hỗ trợ.")
        return response
