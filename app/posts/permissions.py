from rest_framework import permissions


class IsUserAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (obj.user == request.user or request.user.is_staff)