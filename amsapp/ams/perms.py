from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Đảm bảo người dùng đã được xác thực
        if not super().has_object_permission(request, view, obj):
            return False

        # Kiểm tra nếu người dùng là chủ sở hữu của obj
        # Giả sử obj có thuộc tính 'user' là người dùng chủ sở hữu
        return obj.user == request.user


class IsCommentAuthorOrPostAuthor(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # Allow the author of the comment or the author of the post to delete the comment
        return (self.has_permission(request, view) and
                (request.user == obj.user or request.user == obj.post.user))


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create surveys.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Survey creation restricted to admin users only.
        return request.user and request.user.is_staff