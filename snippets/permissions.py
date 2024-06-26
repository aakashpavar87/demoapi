from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to delelte and update.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
