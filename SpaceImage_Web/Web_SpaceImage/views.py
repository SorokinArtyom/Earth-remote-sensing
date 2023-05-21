from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework import generics, status, viewsets, mixins, filters
from rest_framework.views import Response, APIView
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet


import uuid
import redis


from .serializers import *
from .permissions import *


# Connect to our Redis instance
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


@api_view(["POST"])
def getJson(request):
    if request.data["password"] == "":
        return HttpResponse("{'status': 'error', 'error': 'password incorrect'}")
    user = User.objects.create_user(
        request.data["username"], request.data["email"], request.data["password"]
    )
    user.save()
    refresh = RefreshToken.for_user(user)
    return HttpResponse(
        '{"refresh": "'
        + str(refresh)
        + '", "access": "'
        + str(refresh.access_token)
        + '"}'
    )

class ALL_Images_Views(viewsets.ModelViewSet):
    # queryset = Water_Images.objects.all()
    serializer_class = ALL_Images_Serializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):  # http://127.0.0.1:8000/ALL_Images/1/
        pk = self.kwargs.get("pk")
        if not pk:
            return ALL_Images.objects.all()
        try:
            return ALL_Images.objects.filter(pk=pk)
        except ALL_Images.DoesNotExist:
            return Response(
                ALL_Images_Serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        print(username, password)
        user = authenticate(request, username=username, password=password)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user is not None:
            random_key = str(uuid.uuid4())
            session_storage.set(random_key, username)
            session_storage.expire(random_key, 1200)
            refresh = RefreshToken.for_user(user)
            response_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "session_id": str(random_key),
            }
            response = JsonResponse(response_data)
            print(str(response.headers))
            return response
        else:
            return JsonResponse(
                {"status": "error", "error": "login failed"}, status=401
            )
class LogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_id = request.COOKIES.get("session_id")
        print(str(session_id))
        if session_id:
            session_storage.delete(session_id)
            response = Response({"status": "logout"}, status=status.HTTP_200_OK)
            response.delete_cookie("session_id")
            return response

        return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class GetUserAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UsersSerializer
    search_fields = ["username"]
    queryset = User.objects.all()

    def post(self, request):
        session_id = request.data["session_id"]
        for i in request.COOKIES:
            print("cookie: " + i + "  ")
        print(str(session_id))
        if session_id is None:
            response = HttpResponse(
                "{'status': 'error', 'error': 'User not found'}"
                + str(request.COOKIES.get("session_id"))
            )
            print(response)
            return response
        username = session_storage.get(session_id)
        s = username.decode("UTF-8")
        user = User.objects.filter(username=s)
        s = str(user[0].id)
        print(user[0].id)
        print(str(s))
        if user is not None:
            response = HttpResponse(
                '{"user": "'
                + user[0].username
                + '", "IsStaff": "'
                + str(user[0].is_staff)
                + '"}'
            )
            print(response)

            return response
        else:
            return HttpResponse("{'status': 'error', 'error': 'User not found'}")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UsersSerializer  # Сериализатор для модели
    permission_classes = [IsAdminOrReadOnlyOwner]

    def get_queryset(self):
        session_id = self.request.COOKIES.get("session_id")
        print(session_id)
        if session_id is not None:
            username = session_storage.get(session_id)
            s = username.decode("UTF-8")
            user = User.objects.filter(username=s)
            return User.objects.filter(id=user[0].id)
        print("Cookie not Found :(")
        return User.objects.none()
