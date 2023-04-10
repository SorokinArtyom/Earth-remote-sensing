from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse


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



@api_view(['POST'])
def getJson(request):
    if request.data['password'] == "":
        return HttpResponse("{'status': 'error', 'error': 'password incorrect'}")
    user = User.objects.create_user(request.data['username'], request.data['email'], request.data['password'])
    user.save()
    refresh = RefreshToken.for_user(user)
    return HttpResponse(
        '{"refresh": "' + str(refresh) + '", "access": "' + str(refresh.access_token) + '"}')

# {
# "password":"2001",
# "email":"sorok40@list.ru",
# "username":"Artem"
# }



# Create your views here.
class Forest_Images_Views(viewsets.ModelViewSet):
    #queryset = Forest_Images.objects.all()
    serializer_class = Forest_Images_Serializer
    permission_classes = (IsAdminOrReadOnly,)

    # queryset = Forest_Images.objects.all()      #Если queryset закомментирован, следует добавить в router вызывающий
                                                  # это представление базовое имя basename. Так как в данном случае DJango
                                                  # не определит его как Teams самостоятельно.
    def get_queryset(self):                       #http://127.0.0.1:8000/Forest_Images/1/
        pk = self.kwargs.get("pk")
        if not pk:
            return Forest_Images.objects.all()[:3]
        try:
            return Forest_Images.objects.filter(pk=pk)
        except Forest_Images.DoesNotExist:
            return Response(Forest_Images_Serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail = True)    #http://127.0.0.1:8000/Forest_Images/1/Poisk/
    def Poisk (self, request, pk=None):         #дополнительный роутинг
        Image = Forest_Images.objects.get(pk=pk)
        return Response({'Image': Image.Image})




class Water_Images_Views(viewsets.ModelViewSet):
    #queryset = Water_Images.objects.all()
    serializer_class = Water_Images_Serializer
    permission_classes = (IsAdminOrReadOnly,)


    def get_queryset(self):                       #http://127.0.0.1:8000/Water_Images/1/
        pk = self.kwargs.get("pk")
        if not pk:
            return Water_Images.objects.all()[:3]
        try:
            return Water_Images.objects.filter(pk=pk)
        except Water_Images.DoesNotExist:
            return Response(Water_Images_Serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail = True)    #http://127.0.0.1:8000/Water_Images/1/Poisk/
    def Poisk (self, request, pk=None):         #дополнительный роутинг
        Image = Water_Images.objects.get(pk=pk)
        return Response({'Image': Image.Image})



class City_Images_Views(viewsets.ModelViewSet):
    #queryset = City_Images.objects.all()
    serializer_class = City_Images_Serializer
    permission_classes = (IsAdminOrReadOnly,)


    def get_queryset(self):                       #http://127.0.0.1:8000/City_Images/1/
        pk = self.kwargs.get("pk")
        if not pk:
            return City_Images.objects.all()[:3]
        try:
            return City_Images.objects.filter(pk=pk)
        except City_Images.DoesNotExist:
            return Response(City_Images_Serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail = True)    #http://127.0.0.1:8000/City_Images/1/Poisk/
    def Poisk (self, request, pk=None):         #дополнительный роутинг
        Image = City_Images.objects.get(pk=pk)
        return Response({'Image': Image.Image})


class Meadows_Images_Views(viewsets.ModelViewSet):
    #queryset = Meadows_Images.objects.all()
    serializer_class = Meadows_Images_Serializer
    permission_classes = (IsAdminOrReadOnly,)


    def get_queryset(self):                       #http://127.0.0.1:8000/Meadows_Images/1/
        pk = self.kwargs.get("pk")
        if not pk:
            return Meadows_Images.objects.all()[:3]
        try:
            return Meadows_Images.objects.filter(pk=pk)
        except Meadows_Images.DoesNotExist:
            return Response(Meadows_Images_Serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail = True)    #http://127.0.0.1:8000/Meadows_Images/1/Poisk/
    def Poisk (self, request, pk=None):         #дополнительный роутинг
        Image = Meadows_Images.objects.get(pk=pk)
        return Response({'Image': Image.Image})



class ALL_Images_Views(viewsets.ModelViewSet):
    # queryset = Water_Images.objects.all()
    serializer_class = ALL_Images_Serializer
    permission_classes = (IsAdminOrReadOnly,)


    def get_queryset(self):                       #http://127.0.0.1:8000/ALL_Images/1/
        pk = self.kwargs.get("pk")
        if not pk:
            return ALL_Images.objects.all()[:3]
        try:
            return ALL_Images.objects.filter(pk=pk)
        except ALL_Images.DoesNotExist:
            return Response(ALL_Images_Serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail = True)    #http://127.0.0.1:8000/Water_Images/1/Poisk/
    def Poisk (self, request, pk=None):         #дополнительный роутинг
        Image = ALL_Images.objects.get(pk=pk)
        return Response({'Image': Image.Image})








class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data["username"]  # допустим передали username и password
        password = request.data["password"]
        print (username, password)
        user = authenticate(request, username=username, password=password)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user is not None:
            random_key = str(uuid.uuid4())
            session_storage.set(random_key, username)
            session_storage.expire(random_key, 1200)
            # response = HttpResponse("{'status': 'ok'}")
            refresh = RefreshToken.for_user(user)
            response = HttpResponse('{"refresh": "' + str(refresh) + '", "access": "' + str(refresh.access_token) + '"}')
            response.set_cookie(key = "session_id", value = random_key, domain = '127.0.0.1', path = '/', max_age = 1200, httponly=False, secure=True, samesite = 'None')  # пусть ключем для куки будет session_id
            # response.headers["Set-Cookie"] = random_key
            print (str(response.headers))
            return response
        else:
            return HttpResponse("{'status': 'error', 'error': 'login failed'}")



class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        session_id = request.COOKIES.get('session_id')
        print (str(session_id))
        if session_id:
            session_storage.delete(session_id)
            response = Response({"status": "logout"}, status=status.HTTP_200_OK)
            response.delete_cookie('session_id')
            return response

        return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class GetUserAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UsersSerializer
    search_fields = ['username']
    queryset = User.objects.all()
    def post(self, request):
        # print (request.data)
        # session_id = request.data["session_id"]  # допустим передали username и password
        session_id = request.COOKIES.get('session_id')
        # session_id2 = request.COOKIES['session_id']
        for i in request.COOKIES: print('cookie: ' + i + '  ')
        print (str(session_id))
        if session_id is None:
            response = HttpResponse("{'status': 'error', 'error': 'User not found'}" + str(request.COOKIES.get('session_id')))
            print(response)
            return response
        # print (session_id)
        username = session_storage.get(session_id)
        # print (username)
        # print(type(username))
        s = username.decode('UTF-8')
        # print(s)
        user = User.objects.filter(username = s)
        # isStaff = str(user[0].is_staff)
        s = str(user[0].id)
        print(user[0].id)
        print (str(s))
        if user is not None:
            # response = HttpResponse(User[0])
            # response = HttpResponse('{ "id":'+s + ', "IsStaff":' +str(user[0].is_staff) + '}')
            # response = HttpResponse(thisUser)
            # response = HttpResponse('[{ "id":' +s+ ', "IsStaff":' +str(user[0].is_staff) + '}]')
            response = HttpResponse('{"id": "' + s + '", "IsStaff": "' + str(user[0].is_staff) + '"}')
            print(response)
            # response.set_cookie("username", user.email)
            # print (User.objects.all()[:3])
            # print (User.objects.filter(pk = 1))
            return response
            # return HttpResponse(User.username)
        else:
            return HttpResponse("{'status': 'error', 'error': 'User not found'}")




class Saved_Images_Add_Views (mixins.CreateModelMixin, GenericViewSet):
    queryset = Saved_Images.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = Saved_Images_Serializer

    def create (self, request, format = None):
        session_id = self.request.COOKIES.get('session_id')
        print(session_id)
        if session_id is not None:
            username = session_storage.get(session_id)
            if username is not None:
                s = username.decode('UTF-8')
                print(s)
                user = User.objects.filter(username=s)
                print ("То что нашло в Redis: ", user[0].id, "  То что передается в запросе: ",request.data["user_id"])

                if int(user[0].id) == int(request.data["user_id"]):
                    print (request.data)
                    serializer = Saved_Images_Serializer(data = request.data)
                    print(serializer)
                    if serializer.is_valid():
                        print ("Ошибка возникла тут?")
                        serializer.save()
                        return Response(serializer.data, status = status.HTTP_201_CREATED)
                    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                return Response({"status": "You can not create rates for others!"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)




class Saved_Images_Views (mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    search_fields = ['Users']
    filter_backends = (filters.SearchFilter,)

    queryset = Saved_Images.objects.all()
    serializer_class = Saved_Images_Serializer

    permission_classes = (IsAdminOrReadOnlyOwner,)

    # def get_queryset(self):
    #     pk = self.kwargs.get("pk")
    #     session_id = self.request.COOKIES.get('session_id')
    #     if session_id is not None:
    #         username = session_storage.get(session_id)
    #         if username is not None:
    #             s = username.decode('UTF-8')
    #             user = User.objects.filter(username=s)
    #             if user[0].is_staff is True:
    #                 if pk is not None:
    #                     body = self.request.data
    #                     print (body)
    #                     serializer = Saved_Images_Serializer(data=body)
    #                     if serializer.is_valid():
    #                         serializer.save()
    #                     return Saved_Images.objects.filter(id=pk)
    #                 return Saved_Images.objects.all()
    #             if user[0] is not None:
    #                 if pk is not None:
    #                     body = self.request.data['Status']
    #                     print(self.request.data)
    #                     Image = Saved_Images.objects.filter(id=pk)
    #                     if ((Image[0].Status == 1) and (body == 2)):
    #                         serializer = Saved_Images_Serializer(data=body)
    #
    #                         if serializer.is_valid():
    #                             serializer.save()
    #                         return Saved_Images.objects.filter(id=pk)
    #                     return Saved_Images.objects.none()
    #                 return Saved_Images.objects.filter(user_id=user[0].id)
    #     return Saved_Images.objects.none()

    def create (self, request, format = None):
        session_id = self.request.COOKIES.get('session_id')
        print(session_id)
        if session_id is not None:
            username = session_storage.get(session_id)
            if username is not None:
                s = username.decode('UTF-8')
                user = User.objects.filter(username=s)
                print (request.data)
                serializer_ADD = ALL_Images_Serializer(data=request.data["Image"])
                print ("До сюда дошло?")
                print (serializer_ADD)
                if serializer_ADD.is_valid():
                    print ("А дальше?")
                    if user[0].is_staff is True:
                        serializer = Saved_Images_Serializer(data = request.data)
                        print (serializer)
                        print (request.data)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status = status.HTTP_201_CREATED)
                        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                    if user[0].id == request.data["Users"]:
                        print (request.data)
                        serializer = Saved_Images_Serializer(data = request.data)
                        print(serializer)
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data, status = status.HTTP_201_CREATED)
                        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
                    return Response({"status": "You can not create saved images for others!"}, status=status.HTTP_401_UNAUTHORIZED)
                return Response({"Status": "This ID_Image not exists"}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(['post'], detail = True)
    def delete(self, request, pk = None):
        try:
            instance = Saved_Images.objects.filter(pk = int(pk))
            instance.delete()
            return Response({'Deleted'})
        except:
            return Response({'Not Deleted'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UsersSerializer  # Сериализатор для модели
    permission_classes = [IsAdminOrReadOnlyOwner]


    def get_queryset(self):
        session_id = self.request.COOKIES.get('session_id')
        print (session_id)
        if session_id is not None:
            username = session_storage.get(session_id)
            s = username.decode('UTF-8')
            user = User.objects.filter(username = s)
            return User.objects.filter(id=user[0].id)
        print("Cookie not Found :(")
        return User.objects.none()





