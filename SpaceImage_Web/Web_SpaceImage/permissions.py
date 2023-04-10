from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission (self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool (request.user and request.user.is_staff)

class IsAdminOrReadOnlyOwner (permissions.BasePermission):
    def has_object_permission (self, request, view, obj):
        print (obj.user.is_staff)

        if bool(obj.user.is_staff):
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user