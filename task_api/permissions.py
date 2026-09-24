from rest_framework.permissions import BasePermission


class IsTaskOwner(BasePermission):
    """
    Allows access only to the owner of a task.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Allows read-only access to everyone.
    Only admin/staff users can modify data.
    """

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )