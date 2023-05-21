from rest_framework import permissions


from django.contrib.auth.models import User
from django.conf import settings
import redis

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission (self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        session_id = request.COOKIES.get("session_id")
        username = session_storage.get(session_id)
        print (username)

        if username is not None:
            s = username.decode("UTF-8")
            user = User.objects.filter(username=s)
        else: return (False)
        return bool (user[0].is_staff)

class IsAdminOrReadOnlyOwner (permissions.BasePermission):
    def has_object_permission (self, request, view, obj):
        print (obj.user.is_staff)

        if bool(obj.user.is_staff):
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user