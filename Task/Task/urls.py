from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema


# Импортируйте ваши представления
from myapp.views import (
    RegisterView,
    UserDetailView,
    UserUpdateView,
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/user/', UserDetailView.as_view(), name='user_detail'),
    path('api/user/update/', UserUpdateView.as_view(), name='user_update'),
    path('api/tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('api/tasks/', TaskListView.as_view(), name='task_list'),
    path('api/tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('api/tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

    # Spectacular URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
