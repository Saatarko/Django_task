from django.core.cache import cache
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import Task
from .serializers import UserSerializer, UserUpdateSerializer, TaskSerializer
from rest_framework.pagination import PageNumberPagination

from .models import Task

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


# для глобального исопльзования пермишенов пользуеемся  settings. Но объявленные permission_classes - используются в первыую чоередь


class TaskPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'  # позовляет api делать запрос чреез url  на колво элемнетво на странице
    max_page_size = 10000  # влияет только на page_size_query_param


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60 * 5))  # Кэширование на 5 минут
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        super().perform_update(serializer)
        # Очистка кэша после обновления пользователя
        cache_key = f'user_{self.request.user.id}'
        cache.delete(cache_key)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60 * 5))  # Кэширование на 5 минут
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        super().perform_update(serializer)
        # Очистка кэша после обновления задачи
        cache_key = f'tasks_{self.request.user.id}'
        cache.delete(cache_key)


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        # Очистка кэша после удаления задачи
        cache_key = f'tasks_{self.request.user.id}'
        cache.delete(cache_key)
