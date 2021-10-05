"""ptown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from django.urls.conf import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'amenities', views.AmenitiesViewSet, basename='amenities')
router.register(r'services', views.ServicesViewSet, basename='services')
router.register(r'operation_hours', views.OperationHoursViewSet, basename='operation_hours')
router.register(r'comments', views.CommentsViewSet, basename='comments')
router.register(r'barbershop', views.BarbershopViewSet, basename='barbershop')
router.register(r'profile', views.ProfileViewSet, basename='profile')

schema_view = get_schema_view(
    openapi.Info(
        title="PTown API",
        default_version='v1',
        description="API for PTown",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(router.urls))
]
