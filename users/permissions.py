from rest_framework import permissions


class IsResourceOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user == obj.user
        )
