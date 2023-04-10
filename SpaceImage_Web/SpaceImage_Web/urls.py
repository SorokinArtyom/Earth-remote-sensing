"""SpaceImage_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from Web_SpaceImage import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = routers.DefaultRouter()
# router.register(r'Forest_Images', views.Forest_Images_Views, basename = 'Forest')
# router.register(r'Water_Images', views.Water_Images_Views, basename = 'Water')
# router.register(r'City_Images', views.City_Images_Views, basename = 'City')
# router.register(r'Meadows_Images', views.Meadows_Images_Views, basename = 'Meadows')
router.register(r'Saved_Images', views.Saved_Images_Views, basename= 'Saved_Images')
router.register(r'ALL_Images', views.ALL_Images_Views, basename= 'ALL_Images')
router.register(r'user', views.UserViewSet)

# router.register(r'user', views.UserViewSet)
# router.register(r'StavkiALL', views.StavkiALL)

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# print(router.urls)

urlpatterns = [

path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# path('Saved_Image/Add/', views.Saved_Images_Add_Views.as_view({'post': 'create'})),
# path('Images/Forest', views.Forest_Images_Views.as_view()),
# path('Images/Water', views.Water_Images_Views.as_view()),
# path('Images/City', views.City_Images_Views.as_view()),
# path('Images/Meadows', views.Meadows_Images_Views.as_view()),

# path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
path('admin/', admin.site.urls),
# path('ALL_Images/', views.ALL_Images_Views.as_view()),


path ('', include(router.urls)),
# path('add_user', views.getJson, name='getJson'),

path('add_user/', views.getJson, name='getJson'),
path('login/', views.LoginAPIView.as_view()),
path('logout/', views.LogoutAPIView.as_view()),
path('get_user/', views.GetUserAPIView.as_view()),


path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
path ('redoc/',schema_view.with_ui('redoc', cache_timeout = 0),name ='schema-redoc'),


]
